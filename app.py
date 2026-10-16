"""Rutas de Flask (la web)."""
import os
import uuid
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session

from services.tutor_service import responder, cargar_historial, borrar_historial

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "cambia-esto-en-produccion")


def sesion_actual():
    """Cada navegador tiene su propio id de conversación (se guarda en la cookie)."""
    if "sesion_id" not in session:
        session["sesion_id"] = str(uuid.uuid4())
    return session["sesion_id"]


@app.route("/")
def inicio():
    sesion_actual()
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    datos = request.get_json(silent=True) or {}
    pregunta = (datos.get("mensaje") or "").strip()
    nivel = datos.get("nivel", "principiante")

    if not pregunta:
        return jsonify({"error": "Escribe una pregunta."}), 400
    if len(pregunta) > 1000:
        return jsonify({"error": "La pregunta es demasiado larga (máx. 1000 caracteres)."}), 400

    try:
        resultado = responder(sesion_actual(), pregunta, nivel)
        return jsonify(resultado)
    except Exception as error:
        print(f"[chat] Error: {error}")
        return jsonify({"error": "No pude responder en este momento. Intenta de nuevo."}), 500


@app.route("/historial")
def historial():
    try:
        return jsonify(cargar_historial(sesion_actual(), limite=50))
    except Exception as error:
        print(f"[historial] Error: {error}")
        return jsonify([])


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    try:
        borrar_historial(sesion_actual())
    except Exception as error:
        print(f"[reiniciar] Error: {error}")
        return jsonify({"error": "No se pudo reiniciar."}), 500
    return jsonify({"ok": True})


@app.route("/salud")
def salud():
    return jsonify({"estado": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
