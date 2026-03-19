# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [2026-03-19]

- ✨ feat: verificación de conflictos de calendario
  - Nueva sección en prompt.py: "VERIFICACIÓN DE CONFLICTOS DE CALENDARIO"
  - Antes de crear evento: verificar si hay conflicto con gog calendar events
  - Si hay conflicto: proponer horas libres del día + ofrecer actualizar existente
  - Si no hay conflicto: crear directamente
  - Nueva subsección en skills/gog/SKILL.md para verificación y actualización
  - El agente ahora evita duplicar eventos en el mismo horario
- ✨ feat: detección de follow-ups
  - Nueva sección en prompt.py: "DETECCIÓN DE FOLLOW-UPS"
  - Cuando usuario menciona proyecto/tema pasado, agente busca correos automáticamente
  - Muestra lista con remitente + asunto + fecha
  - Solo activa con intención clara (no con saludos o preguntas generales)

## [2026-03-18]

- ✨ feat: historial por usuario de Telegram
  - Añadir columna user_id a tabla messages
  - save_message, get_history, clear_history ahora reciben user_id
  - /history y /clear trabajan solo con historial del usuario
  - Cada usuario tiene contexto independiente
- ✨ feat: script de setup automatizado
  - scripts/setup.sh crea venv, instala deps, copia GOG, configura .env
  - Quick Start en README.md

## [2026-03-17]

- 🔧 fix: persistencia con function calling
  - Refactorizar usando patrón método común
  - chat() y chat_with_history() ahora comparten lógica
  - Ambos funcionan con tools
- 🔧 fix: incluir system prompt en chat con historial
  - El bot ahora recuerda su identidad (OpenNemesis)
- ✨ feat: añadir comandos /status y /skills al bot
  - /status muestra modelo, estado TTS y lista de skills
  - /skills lista skills con descripción
  - /help actualizado con nuevos comandos
- 🔒 security: añadir filtro de usuario (TELEGRAM_ALLOWED_USER_ID)
  - Solo el usuario autorizado puede usar el bot
  - Mensaje de "acceso denegado" para otros usuarios
  - Soporte para múltiples usuarios separados por coma
- 💾 feat: persistencia de conversación con SQLite
  - Nuevo archivo db.py con funciones de base de datos
  - Mover a directorio data/ (data/db.py, data/conversations.db)
  - Historial guardado entre sesiones
  - Comando /clear para borrar historial
  - Comando /history para ver estado
  - Variable MAX_HISTORY_MESSAGES configurable
  - Variable PERSISTENCE_ENABLED para activar/desactivar

## [2026-03-16]

- ♻️ refactor: rename .agent to .agents
  - Directorio renombrado para seguir convención plural
  - Actualizadas todas las referencias en AGENTS.md, README.md y skills
- ♻️ refactor: move execute_command to tools.py
  - Función extraída de gemini_client.py a tools/tools.py
  - Código más modular y mantenible

## [2026-03-14]

- 🐛 fix: exclude __pycache__ from skills loader
  - Añadido filtro para directorios que empiezan con "_"

## [2026-03-12]

- ✨ feat: sistema de skills con contexto SKILL.md
  - skills/loader.py carga automáticamente ./skills/*/SKILL.md
  - Contexto de skills incluido en system prompt de Gemini
  - Tool genérica execute_command para ejecutar comandos directamente
  - Nueva skill = solo añadir carpeta con SKILL.md
- 🔄 refactor: eliminar tools GOG predefinidas
  - Ahora Gemini ejecuta comandos directamente vía SKILL.md
  - Más flexible y escalable
- 🔄 revert: eliminar sistema de routing de skills
- 🔧 fix: añadir /opt/gogcli al PATH para ejecución de comandos
- 📝 docs: actualizar SKILL.md con ejemplos de fechas y timezone
- 📝 docs: crear prompt.py con system prompt separado
- 🔧 fix: prompt mejorado para fechas y tareas serias
  - get_time() para cualquier operación con fechas
  - Regla general: preguntar si información ambigua
  - Formato +01:00 para Europe/Madrid
- 🔧 fix: procesar function calls recursivamente hasta completar tarea
  - El agente ahora encadena múltiples llamadas a tools
- 📝 docs: clarificar búsqueda de correos enviados
  - Usar "from:me" para buscar correos enviados
  - Clarificar cómo responder "A quién envié"
- ⏳ pending: búsqueda de destinatarios en correos enviados

## [2026-03-11]

- 🗑️ remove: eliminar Groq (Whisper) - transcripción vía Gemini (8869991)
- ✨ feat: añadir tools (get_weather, get_time, search_web)
- 🔧 fix: soportar múltiples function calls en una misma petición
- 📦 deps: cambiar duckduckgo-search por ddgs
- ✨ feat: integrar GOG (Google Workspace) como tools
  - gmail_search, gmail_list_emails, gmail_send
  - calendar_list_events, calendar_create_event
  - drive_list_files, contacts_list
- 🔧 fix: calendar tools - add timezone support
- 🔧 fix: handle None response from function calls
- 🔄 Cambiar modelo a gemini-3.1-flash-lite-preview (500 RPM) (9b737da)

## [2026-03-10]

- ✨ feat: añadir Groq Whisper para transcripción de audio (986ef29)
- 🔧 fix: implementar transcripción de audio vía file upload (fde84ee)
- ✨ feat: mostrar transcripción de voz del usuario como mensaje de texto (224b6b3)
- ✨ feat: añadir transcripción de texto junto con respuesta de voz (3985504)
- 📝 docs: documentar opción LiveKit intercalado para V2.0 (f0bbd9b)
- ✨ feat: implementar opción B híbrida con TTS (a9575b7)
- 🔧 fix: usar gemini-2.5-flash para API REST (040c05c)
- ✨ feat: añadir puente de comunicación Telegram con handlers de texto y voz (a1f390c)
- 🐛 fix: usar async para get_me en validacion Telegram (560259d)
- ✨ feat: inicializar proyecto OpenNemesis v1.0 (4aff854)
