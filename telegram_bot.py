"""
OpenNemesis - Telegram Bot Handler
Manejo de mensajes de texto y voz
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logger = logging.getLogger("OpenNemesis.Telegram")


class TelegramBot:
    def __init__(self, token: str, gemini_client):
        self.token = token
        self.gemini_client = gemini_client
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja el comando /start"""
        await update.message.reply_text(
            "🎉 ¡Hola! Soy OpenNemesis\n\n"
            "Estoy listo para ayudarte. Envíame un mensaje de texto o audio."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Maneja el comando /help"""
        await update.message.reply_text(
            "📖 Comandos disponibles:\n"
            "/start - Iniciar el bot\n"
            "/help - Mostrar ayuda\n\n"
            "También puedes enviarme mensajes de voz o texto."
        )
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Procesa mensajes de texto"""
        user_message = update.message.text
        user = update.message.from_user
        user_name = user.first_name if user else "Usuario"
        
        logger.info(f"Mensaje de {user_name}: {user_message[:50]}...")
        
        await update.message.chat.send_action("typing")
        
        response = self.gemini_client.chat(user_message)
        
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
        
        transcription = self.gemini_client.transcribe_audio(audio_bytes)
        
        logger.info(f"Transcripción: {transcription[:100]}...")
        
        response = self.gemini_client.chat(transcription)
        
        await update.message.reply_text(response)
    
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
        
        self.application.add_handler(
            MessageHandler(filters.VOICE, self.handle_voice)
        )
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text)
        )
        
        self.application.add_error_handler(self.handle_error)
        
        logger.info("✓ Telegram Bot iniciado y escuchando...")
        await self.application.run_polling()
