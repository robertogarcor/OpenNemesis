"""
OpenNemesis - Gemini Client
Cliente para Google Gemini con soporte multimodal y tools
"""

import logging
from typing import Union

logger = logging.getLogger("OpenNemesis.Gemini")

TOOLS_SCHEMA = [{
    "function_declarations": [
        {
            "name": "get_weather",
            "description": "Get the current weather for a given city",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "city": {"type": "STRING", "description": "City name"}
                },
                "required": ["city"]
            }
        },
        {
            "name": "get_time",
            "description": "Get current time and date",
            "parameters": {
                "type": "OBJECT",
                "properties": {}
            }
        },
        {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    ]
}]


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-3.1-flash-lite-preview"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self._init_client()
        self._init_tools()
    
    def _init_client(self):
        """Inicializa el cliente de Gemini"""
        try:
            import google.genai as genai
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"✓ Cliente Gemini inicializado con modelo: {self.model}")
        except Exception as e:
            logger.error(f"✗ Error inicializando Gemini: {e}")
            raise
    
    def _init_tools(self):
        """Inicializa las tools disponibles"""
        try:
            from tools.tools import get_weather, get_time, search_web
            self.tools = {
                "get_weather": get_weather,
                "get_time": get_time,
                "search_web": search_web
            }
            logger.info(f"✓ Tools cargadas: {list(self.tools.keys())}")
        except Exception as e:
            logger.error(f"✗ Error cargando tools: {e}")
            self.tools = {}
    
    def chat(self, message: str) -> str:
        """Envía un mensaje y obtiene respuesta (con tools)"""
        try:
            from google.genai import types
            
            config = types.GenerateContentConfig(
                tools=TOOLS_SCHEMA
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=message,
                config=config
            )
            
            if response.function_calls:
                logger.info(f"🔧 Function calls detectados: {[fc.name for fc in response.function_calls]}")
                
                for fc in response.function_calls:
                    tool_name = fc.name
                    tool_args = dict(fc.args) if fc.args else {}
                    
                    if tool_name in self.tools:
                        logger.info(f"🔧 Ejecutando {tool_name} con args: {tool_args}")
                        result = self.tools[tool_name](**tool_args)
                        logger.info(f"🔧 Resultado: {str(result)[:100]}...")
                        
                        follow_up = self.client.models.generate_content(
                            model=self.model,
                            contents=[
                                {"function_response": {
                                    "name": tool_name,
                                    "response": {"result": result}
                                }}
                            ],
                            config=config
                        )
                        return follow_up.text
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error en chat: {e}")
            return "⚠️ Lo siento, hubo un error procesando tu mensaje."
    
    def chat_simple(self, message: str) -> str:
        """Envía un mensaje sin tools"""
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
        """Transcribe audio usando Gemini (vía file upload)"""
        try:
            import io
            
            audio_buffer = io.BytesIO(audio_bytes)
            audio_buffer.name = "audio.ogg"
            
            uploaded_file = self.client.files.upload(
                file=audio_buffer,
                config={"mime_type": "audio/ogg"}
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=[uploaded_file, "Transcribe este audio en español. Devuelve solo la transcripción."]
            )
            
            if response.text:
                return response.text
            return "⚠️ No se pudo transcribir el audio."
            
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
