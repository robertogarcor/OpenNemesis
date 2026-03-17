# OpenNemesis - Memoria del Proyecto

Este documento sirve como referencia técnica y memoria de la evolución del proyecto OpenNemesis para Antigravity y otros asistentes de IA.

## Descripción
OpenNemesis es un agente de IA diseñado para ser sencillo, funcional, escalable y seguro. Está inspirado en la idea de OpenClaw y su objetivo principal es asistir al usuario inicialmente a través de Telegram, para posteriormente escalar a plataformas web, móviles u otras interfaces (ej. LiveKit).

## Historial de Desarrollo

### Hito 1: Infraestructura y Git (2026-03-10)
- [x] Inicializar repositorio Git (rama main)
- [x] Crear .gitignore para Python
- [x] Crear plantilla .env.local con variables de entorno
- [x] Crear requirements.txt con dependencias
- [x] Crear README.md para el usuario
- [x] Crear main.py con validación de conexiones (Telegram/Gemini)
- [x] Fix: usar async para get_me() en Telegram

### Hito 2: Puente de Comunicación (Telegram)
- [x] Configurar Application con handlers
- [x] Procesar mensajes de texto
- [x] Procesar mensajes de voz/audio
- [x] Testing y refinamiento
- [x] Corrección de modelo Gemini
- [x] Transcripción de audio vía Gemini (file upload)
- [x] Eliminar Groq - usar solo Gemini para transcripción
- [x] Actualizar a modelo gemini-3.1-flash-lite-preview (500 RPM)

### Hito 3: Skills y Tools
- [x] Implementar TTS con Edge TTS
- [x] Sistema híbrido texto/voz
- [x] Implementar tools (get_weather, get_time, search_web)
- [x] Function calling con Gemini
- [x] Soporte múltiples tools en una petición
- [x] Integrar GOG (Google Workspace CLI) como skills
- [x] Sistema de skills con contexto SKILL.md
  - [x] skills/loader.py carga SKILL.md automáticamente
  - [x] Contexto de skills incluido en system prompt
  - [x] Tool genérica execute_command para ejecución directa
  - [x] Nueva skill = solo añadir carpeta con SKILL.md
- [x] Prompt separado en prompt.py
- [x] Function calling recursivo (múltiples llamadas en cadena)
- [x] Mejoras en fechas y timezone
  - [x] get_time() para operaciones con fechas
  - [x] Formato +01:00 para Europe/Madrid
- [x] Fix: exclude __pycache__ from skills loader
- [x] Búsqueda de destinatarios en correos enviados (usar messages search + --json)

### Hito 4: Refactorización (2026-03-17)
- [x] Refactorizar imports (mover a nivel de módulo)
  - [x] main.py - imports de telegram, google.genai
  - [x] telegram_bot.py - import de tts_client
  - [x] gemini_client.py - imports de google.genai, types, io, tools
  - [x] prompt.py - import de skills.loader
  - [x] tts_client.py - import de edge_tts
  - [x] tools/tools.py - import de ddgs

### Hito 5: Comandos Adicionales (2026-03-17)
- [x] Añadir comando /status (modelo, TTS, skills)
- [x] Añadir comando /skills (listar skills con descripción)
- [x] Actualizar /help con nuevos comandos

### Hito 6: Seguridad - Filtro de Usuario (2026-03-17)
- [x] Añadir variable TELEGRAM_ALLOWED_USER_ID en .env.local
- [x] Implementar filtro en todos los handlers
- [x] Mensaje de acceso denegado para usuarios no autorizados

### Hito 7: Persistencia de Conversación (2026-03-17)
- [x] Crear db.py con SQLite para persistencia
- [x] Funciones: save_message, get_history, clear_history
- [x] Integrar persistencia en handle_text y handle_voice
- [x] Añadir comando /clear para borrar historial
- [x] Añadir variable MAX_HISTORY_MESSAGES (configurable)
- [x] Historial unificado (sin user_id) - escalable para futuro multiusuario

## Roadmap Futuro

### Opción LiveKit Intercalado (V2.0)
Arquitectura para voz ilimitada en tiempo real:

```
Telegram (audio) → Servidor Python → LiveKit → Gemini Live API
                                              ↓
Telegram (audio) ← Servidor Python ← LiveKit ← Respuesta
```

**Características:**
- Voz en tiempo real (no mensajes estáticos)
- Conversación voz-a-voz fluida
- Ilimitado (si tienes API de LiveKit + Gemini Live)
- Múltiples usuarios simultáneos

**Requisitos:**
- Servidor corriendo 24/7
- LiveKit desplegado (self-hosted o cloud)
- Webhook de Telegram para voz

**Estado:** Pendiente de implementación

---

## Tareas Pendientes

### Prioridad Alta
- [ ] Implementar memoria del agente (persistencia de conversación entre sesiones)

### Prioridad Media
- [ ] Implementar LiveKit (V2.0) - Voz en tiempo real
