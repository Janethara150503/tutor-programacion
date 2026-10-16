import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

_cliente = None


def obtener_cliente():
    """Devuelve un único cliente de Supabase (se crea la primera vez)."""
    global _cliente
    if _cliente is None:
        _cliente = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    return _cliente
