# Asistente de Citas

App de escritorio que usa **Google Gemini AI** para ayudarte a conectar con personas, iniciar conversaciones atractivas y concretar citas o encuentros casuales.

## Funcionalidades

| Panel | Qué hace |
|---|---|
| **Iniciar Conversación** | Genera 3 opciones de primer mensaje dado un perfil |
| **Cómo Responder** | Sugiere 2-3 respuestas a mensajes recibidos con tono explicado |
| **Guía Paso a Paso** | Crea un plan de acción para concretar la cita |
| **Análisis de Tono** | Evalúa el nivel de interés y señales de la otra persona |

Todos los paneles soportan adjuntar **capturas de pantalla** y **archivos de audio** para dar más contexto a la IA.

## Requisitos

- Python 3.11+
- API key de Google Gemini (gratis en [aistudio.google.com/apikey](https://aistudio.google.com/apikey))

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/gonzademonte-svg/asistente-citas.git
cd asistente-citas

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar la API key
# Crea un archivo .env en la raíz del proyecto con:
# GEMINI_API_KEY=tu_api_key_aqui
# (puedes copiar env.example como base)
```

## Uso

```bash
python main.py
```

## Desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Ejecutar tests
pytest tests/ -v
```

## Estructura del Proyecto

```
asistente-citas/
├── main.py                  # Punto de entrada
├── env.example              # Plantilla para .env
├── requirements.txt         # Dependencias de producción
├── requirements-dev.txt     # Dependencias de desarrollo
├── app/
│   ├── controller.py        # Lógica central
│   ├── gemini_service.py    # Integración con Gemini API
│   ├── session_store.py     # Historial local en JSON
│   └── ui/
│       ├── main_window.py   # Ventana principal
│       ├── base_panel.py    # Componentes reutilizables
│       ├── panel_inicio.py
│       ├── panel_responder.py
│       ├── panel_guia.py
│       └── panel_tono.py
└── tests/
    └── test_core.py
```

## CI

El pipeline de GitHub Actions corre automáticamente en cada push a `main` y en pull requests.

Para habilitar tests con la API real en CI, agrega `GEMINI_API_KEY` en **Settings → Secrets and variables → Actions**.
