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

### Hito 3: Skills y Tools
- [x] Implementar TTS con Edge TTS
- [x] Sistema híbrido texto/voz
- [ ] Implementar tools (clima, búsqueda web, hora)
- [ ] Integrar skill GOG
- [ ] Sistema de routing de skills

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
