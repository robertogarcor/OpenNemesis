# OpenNemesis

Agente de IA modular, escalable y seguro inspirado en OpenClaw.

## Características

- **Comunicación**: Telegram Bot (texto y voz)
- **IA**: Google Gemini (gemini-3.1-flash-lite-preview - 500 RPM) con function calling
- **Tools**: get_weather, get_time, search_web
- **Skills**: GOG (Google Workspace CLI) - pendiente integración
- **Arquitectura**: Modular y escalable

## Requisitos

- Python 3.10+
- Entorno virtual `.venv/`
- Telegram Bot Token
- Google Gemini API Key

## Instalación

```bash
# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.local .env
# Editar .env con tus credenciales

# Ejecutar
python main.py
```

## Estructura

```
OpenNemesis/
├── .agent/          # Documentación y herramientas del desarrollador
├── skills/          # Capacidades del agente (gog, etc.)
├── tools/          # Utilidades adicionales
├── main.py         # Punto de entrada
├── .env.local      # Plantilla de configuración
└── requirements.txt
```

## Uso

Inicia el bot en Telegram y envíale mensajes de texto o audio.
