"""Tutor: prompt de sistema, memoria de conversación, RAG y salida estructurada."""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from db import obtener_cliente
from schemas import RespuestaTutor
from services.rag_service import buscar_apuntes, formatear_contexto

load_dotenv()

MAX_MENSAJES_MEMORIA = 10  # cuántos mensajes previos se reenvían al modelo

# ETAPA 2: prompt de sistema (rol + nivel)
PROMPT_BASE = """Eres un tutor de programación básica en Python, paciente y amable.
Ayudas a estudiantes con variables, condicionales, bucles y funciones.

Reglas:
- Responde siempre en español, con explicaciones claras y sin tecnicismos innecesarios.
- Incluye un ejemplo corto de código cuando ayude a entender.
- Si el alumno parece confundido, ofrece una analogía sencilla.
- Si la pregunta no es de programación básica, responde brevemente y redirige al tema.
- No hagas la tarea completa del alumno: guíalo con pistas y explicaciones.
"""

NIVELES = {
    "principiante": "El alumno es PRINCIPIANTE: usa lenguaje muy simple, ejemplos de 2 a 4 líneas y evita vocabulario avanzado.",
    "intermedio": "El alumno es INTERMEDIO: puedes usar vocabulario técnico, ejemplos más completos y mencionar buenas prácticas.",
}

_llm = None


def obtener_llm():
    """Crea una sola vez el modelo con salida estructurada (ETAPA 5)."""
    global _llm
    if _llm is None:
        modelo = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
        _llm = modelo.with_structured_output(RespuestaTutor)
    return _llm


def construir_prompt_sistema(nivel, contexto):
    """Arma el prompt de sistema con el nivel y los apuntes (si hay)."""
    texto = PROMPT_BASE + "\n" + NIVELES.get(nivel, NIVELES["principiante"])
    if contexto:
        texto += (
            "\n\nAPUNTES DE LA CLASE (úsalos como base de tu respuesta cuando "
            "sean relevantes y marca uso_apuntes=true si te apoyaste en ellos):\n"
            + contexto
        )
    else:
        texto += "\n\nNo hay apuntes relevantes para esta pregunta: marca uso_apuntes=false."
    return texto


# ETAPA 3: memoria de conversación guardada en Supabase
def cargar_historial(sesion_id, limite=MAX_MENSAJES_MEMORIA):
    """Devuelve los últimos mensajes de la sesión, del más viejo al más nuevo."""
    resultado = (
        obtener_cliente()
        .table("mensajes")
        .select("rol, contenido")
        .eq("sesion_id", sesion_id)
        .order("id", desc=True)
        .limit(limite)
        .execute()
    )
    return list(reversed(resultado.data or []))


def guardar_mensaje(sesion_id, rol, contenido, tema=None, dificultad=None, uso_apuntes=None):
    obtener_cliente().table("mensajes").insert(
        {
            "sesion_id": sesion_id,
            "rol": rol,
            "contenido": contenido,
            "tema": tema,
            "dificultad": dificultad,
            "uso_apuntes": uso_apuntes,
        }
    ).execute()


def borrar_historial(sesion_id):
    obtener_cliente().table("mensajes").delete().eq("sesion_id", sesion_id).execute()


def responder(sesion_id, pregunta, nivel="principiante", usar_memoria=True):
    """Responde una pregunta del alumno. Devuelve un dict con la RespuestaTutor."""
    # ETAPA 4: RAG
    fragmentos = buscar_apuntes(pregunta)
    contexto = formatear_contexto(fragmentos)

    mensajes = [SystemMessage(content=construir_prompt_sistema(nivel, contexto))]

    if usar_memoria:
        for m in cargar_historial(sesion_id):
            clase = HumanMessage if m["rol"] == "user" else AIMessage
            mensajes.append(clase(content=m["contenido"]))

    mensajes.append(HumanMessage(content=pregunta))

    respuesta = obtener_llm().invoke(mensajes)
    # Garantiza coherencia: si no hubo fragmentos, no pudo usar apuntes
    if not fragmentos:
        respuesta.uso_apuntes = False

    if usar_memoria:
        guardar_mensaje(sesion_id, "user", pregunta)
        guardar_mensaje(
            sesion_id, "assistant", respuesta.respuesta,
            respuesta.tema, respuesta.dificultad, respuesta.uso_apuntes,
        )

    datos = respuesta.model_dump()
    datos["fuentes"] = sorted({f["archivo"] for f in fragmentos})
    return datos
