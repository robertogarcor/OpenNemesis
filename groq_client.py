"""
OpenNemesis - Groq Whisper Client
Transcripción de audio usando Groq Whisper
"""

import logging
import os

logger = logging.getLogger("OpenNemesis.Groq")


class GroqWhisper:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        if api_key:
            self._init_client()
    
    def _init_client(self):
        """Inicializa el cliente de Groq"""
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            logger.info("✓ Cliente Groq Whisper inicializado")
        except Exception as e:
            logger.error(f"✗ Error inicializando Groq: {e}")
            self.client = None
    
    def transcribe(self, audio_bytes: bytes, filename: str = "audio.ogg") -> str:
        """Transcribe audio usando Groq Whisper"""
        if not self.client:
            logger.warning("⚠️ Groq no inicializado, возвращение None")
            return None
        
        try:
            transcription = self.client.audio.transcriptions.create(
                file=(filename, audio_bytes),
                model="whisper-large-v3-turbo",
                response_format="json",
                language="es"
            )
            
            text = transcription.text.strip()
            logger.info(f"✓ Transcripción Groq: {text[:50]}...")
            return text
            
        except Exception as e:
            logger.error(f"Error en transcripción Groq: {e}")
            return None
