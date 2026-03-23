# OpenNemesis

Agente de IA modular, escalable y seguro inspirado en OpenClaw.

## Características

- **Comunicación**: Telegram Bot (texto y voz)
- **IA**: Google Gemini con function calling recursivo
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
- GOG CLI (descargar desde https://github.com/steipete/gogcli/releases, requiere autenticación OAuth)

## Quick Start

```bash
# Copiar plantilla de configuración
cp .env.example .env

# Editar .env con tus credenciales
# Requiere: TELEGRAM_BOT_TOKEN, GEMINI_API_KEY

# Ejecutar script de setup (crea venv, instala deps, configura GOG)
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
cp .env.example .env
# Editar .env con tus credenciales

# Ejecutar
python main.py
```

## Configuración

Copia `.env.example` a `.env` y configura las siguientes variables:

### Telegram Bot
| Variable | Descripción | Obligatorio |
|----------|-------------|-------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | Sí |
| `TELEGRAM_ALLOWED_USER_ID` | ID de usuario autorizado (separar por coma para múltiples) | No |
| `MAX_HISTORY_MESSAGES` | Mensajes a recordar (por defecto 50) | No |
| `PERSISTENCE_ENABLED` | Activar historial (true/false) | No |

### Google Gemini
| Variable | Descripción | Por defecto | Obligatorio |
|----------|-------------|-------------|-------------|
| `GEMINI_API_KEY` | API key de Google Gemini | - | Sí |
| `GEMINI_MODEL` | Modelo de Gemini | gemini-3.1-flash-lite-preview | No |

**Modelos disponibles:**
- `gemini-3.1-flash-lite-preview` (recomendado, 500 RPM)
- `gemini-2.0-flash`
- `gemini-2.0-flash-exp`

### GOG CLI
| Variable | Descripción | Por defecto | Obligatorio |
|----------|-------------|-------------|-------------|
| `GOG_ACCOUNT` | Cuenta Google para autenticación | - | No |
| `GOGCLI_PATH` | Ruta al binario de GOG | bin/gogcli | No |

## Base de datos

La base de datos SQLite se crea automáticamente en `data/conversations.db` al iniciar el bot. Almacena el historial de conversación por usuario de Telegram.

No es necesario crear la base de datos manualmente.

## GOG CLI (Google Workspace)

GOG CLI se usa para Gmail, Calendar, Drive y Contacts.

**Repositorio**: https://github.com/steipete/gogcli
**Descargar**: https://github.com/steipete/gogcli/releases

### Instalación

1. Descarga el binario de la página de releases
2. Guárdalo en `bin/gogcli/gog` (crea la carpeta si no existe)
3. Hazlo ejecutable: `chmod +x bin/gogcli/gog`

### Primera autenticación

Si es la primera vez que ejecutas GOG en esta máquina, necesitas autenticar:

```bash
./bin/gogcli/gog auth add tu@email.com --services gmail,calendar,drive,contacts
```

Se abrirá el navegador para autorizar. Los tokens se guardan en `~/.config/gog/` (no en el proyecto).

### Reinstalación en otra máquina

Los tokens OAuth no se incluyen en el proyecto. Al instalar en otra máquina, debes re-autenticar GOG con el mismo comando anterior.

## Estructura

```
OpenNemesis/
├── .agents/          # Documentación del desarrollador
├── bin/              # GOG CLI (descargar de releases)
├── scripts/          # Scripts de utilidad
├── skills/          # Skills del agente (carpetas con SKILL.md)
│   └── gog/         # Google Workspace
├── tools/           # Utilidades adicionales
├── data/            # Datos (base de datos SQLite)
├── prompt.py        # Prompts del sistema
├── main.py          # Punto de entrada
├── .env.example     # Plantilla de configuración
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
