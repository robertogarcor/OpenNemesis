"""
OpenNemesis - Gemini Client
Cliente para Google Gemini con soporte multimodal
"""

import logging
from typing import Union

logger = logging.getLogger("OpenNemesis.Gemini")


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash-native-audio-latest"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self.chat_session = None
        self._init_client()
    
    def _init_client(self):
        """Inicializa el cliente de Gemini"""
        try:
            import google.genai as genai
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"✓ Cliente Gemini inicializado con modelo: {self.model}")
        except Exception as e:
            logger.error(f"✗ Error inicializando Gemini: {e}")
            raise
    
    def chat(self, message: str) -> str:
        """Envía un mensaje y obtiene respuesta"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=message
            )
            return response.text
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            return "⚠️ Lo siento, hubo un error procesando tu mensaje."
    
    def transcribe_audio(self, audio_bytes: bytes) -> str:
        """Transcribe audio usando Gemini"""
        try:
            from google.genai import types
            
            audio_file = types.Media(
                mime_type="audio/ogg",
                data=audio_bytes
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[audio_file, "Transcribe este audio"]
            )
            
            return response.text
        except Exception as e:
            logger.error(f"Error transcribiendo audio: {e}")
            return "⚠️ No pude procesar el audio."
    
    def chat_with_history(self, message: str, history: list) -> str:
        """Chat con historial de conversación"""
        try:
            contents = history + [message]
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            return response.text
        except Exception as e:
            logger.error(f"Error en chat con historial: {e}")
            return "⚠️ Lo siento, hubo un error."
