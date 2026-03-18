# OpenNemesis

Agente de IA modular, escalable y seguro inspirado en OpenClaw.

## Características

- **Comunicación**: Telegram Bot (texto y voz)
- **IA**: Google Gemini (gemini-3.1-flash-lite-preview - 500 RPM) con function calling recursivo
- **Tools**:
  - Básicas: get_weather, get_time, search_web
  - Genérica: execute_command (ejecuta cualquier comando CLI)
- **Skills**: Contexto automático desde `./skills/*/SKILL.md`
  - gog: Google Workspace (Gmail, Calendar, Drive, Contacts)
- **Arquitectura**: Modular y escalable
  - Sistema de prompts en `prompt.py`
  - Skills auto-cargables sin código

## Requisitos

- Python 3.10+
- Entorno virtual `.venv/`
- Telegram Bot Token
- Google Gemini API Key
- GOG CLI (incluido en `bin/gog`)

## Quick Start

```bash
# Ejecutar script de setup (crea venv, instala deps, copia GOG, configura .env)
./scripts/setup.sh

# Iniciar el bot
python main.py run
```

## Instalación manual

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

## Base de datos

La base de datos SQLite se crea automáticamente en `data/conversations.db` al iniciar el bot. Almacena el historial de conversación por usuario de Telegram.

No es necesario crear la base de datos manualmente.

## Estructura

```
OpenNemesis/
├── .agents/          # Documentación del desarrollador
├── bin/              # Binarios (gog)
├── scripts/          # Scripts de utilidad
├── skills/          # Skills del agente (carpetas con SKILL.md)
│   └── gog/         # Google Workspace
├── tools/           # Utilidades adicionales
├── data/            # Datos (base de datos SQLite)
├── prompt.py        # Prompts del sistema
├── main.py          # Punto de entrada
├── .env.local       # Plantilla de configuración
└── requirements.txt
```

## Añadir nueva skill

1. Crear carpeta en `skills/`
2. Añadir `SKILL.md` con documentación
3. El agente la cargará automáticamente

## Uso

Inicia el bot en Telegram y envíale mensajes de texto o audio.

### Comandos disponibles

- `/start` - Iniciar el bot
- `/status` - Ver estado (modelo, TTS, skills)
- `/skills` - Listar skills disponibles
- `/history` - Ver estado de persistencia
- `/clear` - Borrar historial
- `/tts` - Activar/desactivar respuestas de voz
- `/help` - Mostrar ayuda
