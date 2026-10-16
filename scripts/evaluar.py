"""Evaluación de la calidad del tutor (ETAPA 6).

Uso (desde la raíz del proyecto, con el entorno activo):
    python -m scripts.evaluar

Para cada pregunta de prueba revisa: tema correcto, palabras clave esperadas,
uso de apuntes, y una calificación de 1 a 5 dada por un modelo juez con rúbrica.
"""
import os
import uuid
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

from services.tutor_service import responder, borrar_historial

load_dotenv()

# (pregunta, tema esperado, palabras clave que deberían aparecer)
PREGUNTAS = [
    ("¿Qué es una variable en Python?", "variables", ["valor", "nombre"]),
    ("¿Cuál es la diferencia entre = y == ?", "condicionales", ["asign", "compar"]),
    ("¿Cómo funciona un if y un else?", "condicionales", ["if", "else"]),
    ("¿Para qué sirve range() en un for?", "bucles", ["range", "for"]),
    ("¿Por qué mi while nunca termina?", "bucles", ["condici", "while"]),
    ("¿Qué diferencia hay entre print y return?", "funciones", ["return", "print"]),
    ("¿Qué es un parámetro de una función?", "funciones", ["parámetro", "def"]),
    ("¿Quién ganó el mundial de 2010?", "otro", []),
]

RUBRICA = """Califica la respuesta de un tutor de programación básica de 1 a 5:
5 = correcta, clara, adaptada a un estudiante y con ejemplo útil.
4 = correcta y clara, pero le falta ejemplo o precisión menor.
3 = parcialmente correcta o confusa.
2 = con errores importantes.
1 = incorrecta o irrelevante.
Si la pregunta no es de programación, lo correcto es responder breve y redirigir al tema."""


class Calificacion(BaseModel):
    puntaje: int = Field(ge=1, le=5, description="Calificación de 1 a 5.")
    motivo: str = Field(description="Motivo breve de la calificación.")


def juez():
    modelo = ChatOpenAI(model=os.getenv("OPENAI_MODEL"))
    return modelo.with_structured_output(Calificacion)


def main():
    calificador = juez()
    resultados = []

    for pregunta, tema_esperado, claves in PREGUNTAS:
        sesion = f"eval-{uuid.uuid4()}"
        try:
            r = responder(sesion, pregunta, "principiante", usar_memoria=False)
        except Exception as error:
            print(f"✗ {pregunta}\n   ERROR: {error}\n")
            resultados.append((pregunta, False, False, 0))
            continue
        finally:
            borrar_historial(sesion)

        texto = r["respuesta"].lower()
        tema_ok = r["tema"] == tema_esperado
        claves_ok = all(c.lower() in texto for c in claves)
        nota = calificador.invoke(
            f"{RUBRICA}\n\nPregunta: {pregunta}\n\nRespuesta del tutor:\n{r['respuesta']}"
        )
        resultados.append((pregunta, tema_ok, claves_ok, nota.puntaje))

        print(f"Pregunta: {pregunta}")
        print(f"  Tema: {r['tema']} (esperado: {tema_esperado}) -> {'OK' if tema_ok else 'REVISAR'}")
        print(f"  Palabras clave: {'OK' if claves_ok else 'REVISAR'} | Usó apuntes: {r['uso_apuntes']}")
        print(f"  Juez: {nota.puntaje}/5 - {nota.motivo}\n")

    n = len(resultados)
    temas = sum(1 for _, t, _, _ in resultados if t)
    claves = sum(1 for _, _, c, _ in resultados if c)
    promedio = sum(p for *_, p in resultados) / n
    print("=" * 50)
    print(f"Tema correcto:      {temas}/{n}")
    print(f"Palabras clave:     {claves}/{n}")
    print(f"Promedio del juez:  {promedio:.2f}/5")


if __name__ == "__main__":
    main()
