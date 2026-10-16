from typing import Literal
from pydantic import BaseModel, Field


class RespuestaTutor(BaseModel):
    """Forma de la respuesta del tutor (structured output)."""

    respuesta: str = Field(description="Explicación clara para el alumno, en español, con un ejemplo corto de código si ayuda.")
    tema: Literal["variables", "condicionales", "bucles", "funciones", "otro"] = Field(
        description="Tema principal de la pregunta."
    )
    dificultad: Literal["basica", "intermedia", "avanzada"] = Field(
        description="Dificultad de la pregunta del alumno."
    )
    uso_apuntes: bool = Field(
        default=False, description="True si la respuesta se apoyó en los apuntes de la clase."
    )
