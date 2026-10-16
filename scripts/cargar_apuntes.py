"""Sube los apuntes de la carpeta apuntes/ a Supabase con sus embeddings.

Uso (desde la raíz del proyecto, con el entorno activo):
    python -m scripts.cargar_apuntes
"""
from pathlib import Path

from db import obtener_cliente
from services.rag_service import obtener_embeddings

CARPETA = Path(__file__).resolve().parent.parent / "apuntes"


def dividir_en_fragmentos(texto):
    """Divide un apunte por secciones (## ...) para tener fragmentos con sentido."""
    fragmentos, actual = [], []
    for linea in texto.splitlines():
        if linea.startswith("## ") and actual:
            fragmentos.append("\n".join(actual).strip())
            actual = []
        actual.append(linea)
    if actual:
        fragmentos.append("\n".join(actual).strip())
    return [f for f in fragmentos if len(f) > 40]


def main():
    cliente = obtener_cliente()
    embeddings = obtener_embeddings()
    archivos = sorted(CARPETA.glob("*.md"))
    if not archivos:
        print("No hay archivos .md en la carpeta apuntes/")
        return

    total = 0
    for archivo in archivos:
        texto = archivo.read_text(encoding="utf-8")
        # Título del apunte como contexto de cada fragmento
        titulo = texto.splitlines()[0].lstrip("# ").strip()
        fragmentos = dividir_en_fragmentos(texto)
        vectores = embeddings.embed_documents(fragmentos)

        # Evita duplicados si se vuelve a ejecutar el script
        cliente.table("apuntes").delete().eq("archivo", archivo.name).execute()
        filas = [
            {"archivo": archivo.name, "contenido": f"{titulo}. {frag}", "embedding": vec}
            for frag, vec in zip(fragmentos, vectores)
        ]
        cliente.table("apuntes").insert(filas).execute()
        total += len(filas)
        print(f"{archivo.name}: {len(filas)} fragmentos cargados")

    print(f"Listo. Total de fragmentos: {total}")


if __name__ == "__main__":
    main()
