"""RAG: busca en los apuntes los fragmentos más parecidos a la pregunta."""
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

from db import obtener_cliente

load_dotenv()

MODELO_EMBEDDINGS = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

_embeddings = None


def obtener_embeddings():
    """Crea una sola vez el generador de embeddings."""
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(model=MODELO_EMBEDDINGS)
    return _embeddings


def buscar_apuntes(pregunta, cantidad=3):
    """Devuelve una lista de fragmentos (dict) relacionados con la pregunta.

    Si algo falla (tabla vacía, error de red), devuelve [] para que el tutor
    siga respondiendo sin apuntes.
    """
    try:
        vector = obtener_embeddings().embed_query(pregunta)
        resultado = obtener_cliente().rpc(
            "match_apuntes",
            {"query_embedding": vector, "match_count": cantidad},
        ).execute()
        return resultado.data or []
    except Exception as error:
        print(f"[rag] No se pudo buscar en los apuntes: {error}")
        return []


def formatear_contexto(fragmentos):
    """Convierte los fragmentos en un texto para el prompt del modelo."""
    if not fragmentos:
        return ""
    partes = [f"[{f['archivo']}] {f['contenido']}" for f in fragmentos]
    return "\n\n".join(partes)
