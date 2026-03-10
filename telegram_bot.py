"""
OpenNemesis - Telegram Bot Handler
Manejo de mensajes de texto y voz con TTS opcional
"""

import logging
import io
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logger = logging.getLogger("OpenNemesis.Telegram")


class TelegramBot:
    def __init__(self, token: str, gemini_client, groq_client=None, use_tts: bool = False):
        self.token = token
        self.gemini_client = gemini_client
        self.groq_client = groq_client
        self.use_tts = use_tts
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja el comando /start"""
        await update.message.reply_text(
            "🎉 ¡Hola! Soy OpenNemesis\n\n"
            "Estoy listo para ayudarte. Envíame un mensaje de texto o audio.\n\n"
            "Comandos:\n"
            "/tts - Activar/desactivar respuestas de voz\n"
            "/help - Mostrar ayuda"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja el comando /help"""
        status = "activado" if self.use_tts else "desactivado"
        await update.message.reply_text(
            f"📖 Comandos disponibles:\n"
            f"/start - Iniciar el bot\n"
            f"/tts - Toggle TTS (actualmente {status})\n"
            f"/help - Mostrar ayuda\n\n"
            f"También puedes enviarme mensajes de voz o texto."
        )
    
    async def tts_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle TTS"""
        self.use_tts = not self.use_tts
        status = "✓ Activado" if self.use_tts else "✗ Desactivado"
        await update.message.reply_text(f"{status} respuestas de voz")
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa mensajes de texto"""
        user_message = update.message.text
        user = update.message.from_user
        user_name = user.first_name if user else "Usuario"
        
        logger.info(f"Mensaje de {user_name}: {user_message[:50]}...")
        
        await update.message.chat.send_action("typing")
        
        response = self.gemini_client.chat(user_message)
        
        if self.use_tts and response:
            await self.send_voice_response(update, response)
        else:
            await update.message.reply_text(response)
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa mensajes de voz/audio"""
        voice = update.message.voice
        user = update.message.from_user
        user_name = user.first_name if user else "Usuario"
        
        logger.info(f"Audio de {user_name}: {voice.duration}s")
        
        await update.message.chat.send_action("typing")
        
        file = await context.bot.get_file(voice.file_id)
        audio_bytes = await file.download_as_bytearray()
        
        transcription = None
        
        if self.groq_client:
            logger.info("🔄 Intentando transcripción con Groq...")
            transcription = self.groq_client.transcribe(audio_bytes)
        
        if not transcription:
            logger.info("🔄 Fallback a Gemini para transcripción...")
            transcription = self.gemini_client.transcribe_audio(audio_bytes)
        
        if not transcription or "⚠️" in transcription:
            await update.message.reply_text(
                "🎤 No pude procesar el audio. "
                "Por favor, escribe tu mensaje en texto."
            )
            return
        
        logger.info(f"Transcripción: {transcription[:100]}...")
        
        await update.message.reply_text(f"🎤 {transcription}")
        
        response = self.gemini_client.chat(transcription)
        
        if self.use_tts and response:
            await self.send_voice_response(update, response)
        else:
            await update.message.reply_text(response)
    
    async def send_voice_response(self, update: Update, text: str):
        """Envía respuesta como voz usando TTS + texto"""
        try:
            from tts_client import text_to_speech_sync
            
            await update.message.chat.send_action("record_voice")
            
            audio_bytes = text_to_speech_sync(text)
            
            if audio_bytes:
                audio_file = io.BytesIO(audio_bytes)
                await update.message.reply_voice(audio_file)
                await update.message.reply_text(f"📝 {text}")
                logger.info("✓ Respuesta enviada como voz + texto")
            else:
                await update.message.reply_text(text)
                
        except Exception as e:
            logger.error(f"Error en TTS: {e}")
            await update.message.reply_text(text)
    
    async def handle_error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja errores"""
        logger.error(f"Error: {context.error}")
        if update and update.message:
            await update.message.reply_text("⚠️ Ha ocurrido un error. Inténtalo de nuevo.")
    
    async def start(self):
        """Inicia el bot"""
        logger.info("🚀 Iniciando Telegram Bot...")
        
        self.application = Application.builder().token(self.token).build()
        
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("tts", self.tts_command))
        
        self.application.add_handler(
            MessageHandler(filters.VOICE, self.handle_voice)
        )
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text)
        )
        
        self.application.add_error_handler(self.handle_error)
        
        logger.info("✓ Telegram Bot iniciado y escuchando...")
        await self.application.run_polling()
