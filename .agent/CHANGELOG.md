# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

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
