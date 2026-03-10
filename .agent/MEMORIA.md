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
- [ ] Testing y refinamiento
