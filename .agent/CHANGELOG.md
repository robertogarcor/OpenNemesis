# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

## [2026-03-11]

- 🗑️ remove: eliminar Groq (Whisper) - transcripción ahora vía Gemini (8869991)
- ✨ feat: actualizar modelo Gemini a gemini-3.1-flash-lite-preview (500 RPM)
- 🔧 fix: sincronizar modelo por defecto en main.py y gemini_client.py
- ✨ feat: añadir tools (get_weather, get_time)
- 📦 deps: limpiar dependencias (eliminar livekit, langchain, email)

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
