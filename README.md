# Tutor de Programación Básica con IA

Chatbot web que responde dudas de variables, condicionales, bucles y funciones.

**Stack:** Python · Flask · Supabase (Postgres + pgvector) · OpenAI con LangChain · Render

## Qué incluye (etapas)

| Etapa | Qué hace | Archivo principal |
|---|---|---|
| 1 | Página web, conexión a Supabase y llamada a OpenAI | `app.py`, `db.py` |
| 2 | Prompt de sistema con rol y nivel (principiante / intermedio) | `services/tutor_service.py` |
| 3 | Memoria de conversación guardada en Supabase | `services/tutor_service.py`, tabla `mensajes` |
| 4 | RAG: búsqueda por significado en los apuntes con pgvector | `services/rag_service.py`, `scripts/cargar_apuntes.py` |
| 5 | Salida estructurada: respuesta, tema, dificultad, uso de apuntes | `schemas.py` |
| 6 | Evaluación con preguntas de prueba y modelo juez | `scripts/evaluar.py` |

## Ejecutar en local

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
cp .env.example .env            # y llena tus valores (nunca se sube a GitHub)
```

1. En Supabase: **SQL Editor → New query**, pega el contenido de `sql/schema.sql` y ejecuta **Run**.
2. Carga los apuntes: `python -m scripts.cargar_apuntes`
3. Inicia la app: `python app.py` y abre http://127.0.0.1:5000
4. Evalúa al tutor: `python -m scripts.evaluar`

## Desplegar en Render

1. Sube el proyecto a GitHub (ver commits sugeridos abajo).
2. En render.com: **New → Web Service** y conecta tu repositorio.
3. Configuración (si no detecta `render.yaml`):
   - Runtime: **Python 3**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
4. En **Environment** agrega las 5 variables: `OPENAI_API_KEY`, `OPENAI_MODEL`, `SUPABASE_URL`, `SUPABASE_KEY`, `FLASK_SECRET_KEY`.
5. **Create Web Service**. Al terminar, abre la URL `https://<tu-servicio>.onrender.com`.

> En el plan Free, Render duerme la app tras un rato sin visitas: la primera carga puede tardar ~1 minuto. Ábrela antes de entregar.

## Commits sugeridos (uno por etapa)

```bash
git add .gitignore requirements.txt && git commit -m "Etapa 0: entorno y .gitignore"
git add .env.example sql/ apuntes/ db.py app.py templates/ && git commit -m "Etapa 1: base Flask + Supabase + OpenAI"
git add services/tutor_service.py && git commit -m "Etapa 2 y 3: prompt de sistema y memoria"
git add services/rag_service.py scripts/cargar_apuntes.py && git commit -m "Etapa 4: RAG con pgvector"
git add schemas.py && git commit -m "Etapa 5: salida estructurada"
git add scripts/evaluar.py && git commit -m "Etapa 6: evaluacion"
git add render.yaml README.md && git commit -m "Despliegue en Render"
git push
```

Antes de cada `git add`, revisa con `git status` que `.env` **no** aparezca.

## Capturas para el PDF de evidencias

1. `git ls-files` (sin `.env`) y el repositorio en GitHub.
2. Supabase: tablas `apuntes` (con filas) y `mensajes`.
3. `python -m scripts.cargar_apuntes` terminado.
4. Interfaz del chat con una pregunta en nivel Principiante y otra en Intermedio.
5. Memoria: pregunta de seguimiento ("dame otro ejemplo") que se apoye en la anterior.
6. Respuesta con etiquetas: tema, dificultad y "Usó los apuntes".
7. `python -m scripts.evaluar` con el resumen final.
8. Render: panel con estado **Live** y la app abierta en la URL pública.
