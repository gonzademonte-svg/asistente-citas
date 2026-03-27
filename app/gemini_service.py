import os
import mimetypes
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

MODEL = "gemini-2.5-flash"

BASE_SYSTEM_PROMPT = """Eres un coach de relaciones directo, sin rodeos y práctico.
Tu objetivo es ayudar al usuario a conectar con personas y concretar citas o encuentros.
Sé honesto, concreto y evita clichés. Da respuestas cortas y accionables.
No sermones ni juicios morales. Habla siempre en español."""

PROMPTS = {
    "inicio": BASE_SYSTEM_PROMPT + """
Módulo: Generar apertura de conversación.
El usuario te dará información sobre la persona con quien quiere hablar.
Genera exactamente 3 opciones de primer mensaje numeradas (1. 2. 3.).
Cada opción debe ir seguida de una línea corta explicando por qué funciona.
Los mensajes deben sonar naturales, no forzados ni desesperados.
Si se adjunta una imagen o captura de pantalla, úsala para enriquecer el contexto.""",

    "responder": BASE_SYSTEM_PROMPT + """
Módulo: Consejo para responder mensajes.
El usuario pegará un mensaje recibido y el contexto de la conversación.
Genera 2-3 respuestas sugeridas numeradas. Indica el tono de cada una (ej: casual, con humor, directo).
Prioriza mantener el interés y avanzar hacia un encuentro real.
Si se adjunta una captura de pantalla de la conversación, analízala.""",

    "guia": BASE_SYSTEM_PROMPT + """
Módulo: Guía paso a paso para concretar una cita.
El usuario describe el estado actual de la situación y su objetivo.
Genera un plan concreto en pasos numerados: qué decir ahora, cuándo y cómo proponer el encuentro, qué evitar.
Sé directo y realista. Máximo 6 pasos.""",

    "tono": BASE_SYSTEM_PROMPT + """
Módulo: Análisis de tono e interés.
El usuario pegará uno o más mensajes de la otra persona.
Evalúa y responde con este formato exacto:
NIVEL DE INTERÉS: [Bajo / Medio / Alto]
SEÑALES POSITIVAS: (lista breve)
SEÑALES DE ALERTA: (lista breve, o "Ninguna")
RECOMENDACIÓN: (1-2 oraciones de qué hacer ahora)
Si se adjunta una captura de pantalla, analiza también el lenguaje visual y el contexto.""",
}


def _build_parts(text_prompt: str, image_path: str | None, audio_path: str | None) -> list:
    parts = []
    if image_path and os.path.isfile(image_path):
        mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        with open(image_path, "rb") as f:
            parts.append({"inline_data": {"mime_type": mime, "data": f.read()}})
    if audio_path and os.path.isfile(audio_path):
        mime = mimetypes.guess_type(audio_path)[0] or "audio/mpeg"
        with open(audio_path, "rb") as f:
            parts.append({"inline_data": {"mime_type": mime, "data": f.read()}})
    parts.append(text_prompt)
    return parts


def ask(module: str, user_prompt: str, image_path: str | None = None, audio_path: str | None = None) -> str:
    system_prompt = PROMPTS.get(module, BASE_SYSTEM_PROMPT)
    model = genai.GenerativeModel(
        model_name=MODEL,
        system_instruction=system_prompt,
    )
    parts = _build_parts(user_prompt, image_path, audio_path)
    try:
        response = model.generate_content(parts)
        return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Error al contactar Gemini: {e}") from e
