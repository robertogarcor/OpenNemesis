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
        },
        # GOG Tools
        {
            "name": "gmail_search",
            "description": "Search emails in Gmail",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING", "description": "Gmail search query (e.g., 'from:someone@gmail.com newer_than:7d')"},
                    "max_results": {"type": "INTEGER", "description": "Maximum number of results (default 5)"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "gmail_list_emails",
            "description": "List recent emails from inbox",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "max_results": {"type": "INTEGER", "description": "Maximum number of emails to list (default 10)"}
                }
            }
        },
        {
            "name": "gmail_send",
            "description": "Send an email via Gmail",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "to": {"type": "STRING", "description": "Recipient email address"},
                    "subject": {"type": "STRING", "description": "Email subject"},
                    "body": {"type": "STRING", "description": "Email body content"}
                },
                "required": ["to", "subject", "body"]
            }
        },
        {
            "name": "calendar_list_events",
            "description": "List calendar events",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "calendar_id": {"type": "STRING", "description": "Calendar ID (default: primary)"},
                    "from_date": {"type": "STRING", "description": "Start date (RFC3339, date like '2026-03-15', or relative like 'today', 'tomorrow')"},
                    "to_date": {"type": "STRING", "description": "End date (RFC3339, date like '2026-03-15', or relative like 'today', 'tomorrow')"}
                }
            }
        },
        {
            "name": "calendar_create_event",
            "description": "Create a calendar event",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "calendar_id": {"type": "STRING", "description": "Calendar ID (default: primary)"},
                    "summary": {"type": "STRING", "description": "Event title"},
                    "start_time": {"type": "STRING", "description": "Start time with timezone (e.g., 2026-03-15T10:00:00+01:00)"},
                    "end_time": {"type": "STRING", "description": "End time with timezone (e.g., 2026-03-15T11:00:00+01:00)"}
                },
                "required": ["summary", "start_time", "end_time"]
            }
        },
        {
            "name": "drive_list_files",
            "description": "List or search files in Google Drive",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {"type": "STRING", "description": "Search query for Drive files"},
                    "max_results": {"type": "INTEGER", "description": "Maximum number of files (default 10)"}
                }
            }
        },
        {
            "name": "contacts_list",
            "description": "List Google Contacts",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "max_results": {"type": "INTEGER", "description": "Maximum number of contacts (default 20)"}
                }
            }
        }
    ]
}]


class GeminiClient:
    def __init__(self, api_key: str, model: str = "gemini-3.1-flash-lite-preview"):
        self.api_key = api_key
        self.model = model
        self.client = None
        self.last_function_call_part = None
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
            from tools.gog_tools import (
                gmail_search, gmail_list_emails, gmail_send,
                calendar_list_events, calendar_create_event,
                drive_list_files, contacts_list
            )
            self.tools = {
                # Basic tools
                "get_weather": get_weather,
                "get_time": get_time,
                "search_web": search_web,
                # GOG tools
                "gmail_search": gmail_search,
                "gmail_list_emails": gmail_list_emails,
                "gmail_send": gmail_send,
                "calendar_list_events": calendar_list_events,
                "calendar_create_event": calendar_create_event,
                "drive_list_files": drive_list_files,
                "contacts_list": contacts_list
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
                
                # Obtener la part con thought_signature
                last_function_call_part = None
                if response.candidates and response.candidates[0].content.parts:
                    last_function_call_part = response.candidates[0].content.parts[0]
                
                # Ejecutar TODOS los function calls
                function_responses = []
                for fc in response.function_calls:
                    tool_name = fc.name
                    tool_args = dict(fc.args) if fc.args else {}
                    
                    if tool_name in self.tools:
                        logger.info(f"🔧 Ejecutando {tool_name} con args: {tool_args}")
                        try:
                            result = self.tools[tool_name](**tool_args)
                            logger.info(f"🔧 Resultado: {str(result)[:100]}...")
                        except Exception as e:
                            logger.error(f"🔧 Error ejecutando {tool_name}: {e}")
                            result = f"Error: {str(e)}"
                        
                        function_responses.append({
                            "name": tool_name,
                            "result": result
                        })
                
                # Construir contents con TODAS las respuestas
                contents_parts = [
                    types.Content(role='user', parts=[types.Part(text=message)]),
                    types.Content(role='model', parts=[last_function_call_part])
                ]
                
                for fr in function_responses:
                    contents_parts.append(
                        types.Content(role='function', parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=fr["name"],
                                response={"result": fr["result"]}
                            )
                        )])
                    )
                
                # Enviar follow-up con todas las respuestas
                follow_up = self.client.models.generate_content(
                    model=self.model,
                    contents=contents_parts,
                    config=config
                )
                
                # Manejar caso donde text es None
                if follow_up.text:
                    return follow_up.text
                elif function_responses:
                    # Devolver el resultado de la última función si no hay texto
                    return function_responses[-1]["result"]
                return "⚠️ No se pudo obtener una respuesta."
            
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
