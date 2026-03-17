"""
OpenNemesis - Gemini Client
Cliente para Google Gemini con soporte multimodal, tools y skills
"""

import logging
import io
from typing import Union

import google.genai as genai
from google.genai import types

from prompt import get_system_prompt, reload_skills_context
from tools.tools import get_weather, get_time, search_web, execute_command

logger = logging.getLogger("OpenNemesis.Gemini")

SKILLS_CONTEXT = reload_skills_context()

TOOLS_SCHEMA = [{
    "function_declarations": [
        {
            "name": "execute_command",
            "description": "Execute a shell command. Use this for any system command, git operations, gog CLI commands, or any other terminal operation. ALWAYS use the full command with all arguments.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "command": {"type": "STRING", "description": "The complete command to execute"}
                },
                "required": ["command"]
            }
        },
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
        self.last_function_call_part = None
        self._init_client()
        self._init_tools()
    
    def _init_client(self):
        """Inicializa el cliente de Gemini"""
        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"✓ Cliente Gemini inicializado con modelo: {self.model}")
        except Exception as e:
            logger.error(f"✗ Error inicializando Gemini: {e}")
            raise
    
    def _init_tools(self):
        """Inicializa las tools disponibles"""
        try:
            self.tools = {
                "execute_command": execute_command,
                "get_weather": get_weather,
                "get_time": get_time,
                "search_web": search_web,
            }
            logger.info(f"✓ Tools cargadas: {list(self.tools.keys())}")
        except Exception as e:
            logger.error(f"✗ Error cargando tools: {e}")
            self.tools = {}
    
    def chat(self, message: str) -> str:
        """Envía un mensaje y obtiene respuesta (con function calling)"""
        try:
            system_instruction = get_system_prompt()
            if SKILLS_CONTEXT:
                system_instruction += "\n\n" + SKILLS_CONTEXT
            
            config = types.GenerateContentConfig(
                tools=TOOLS_SCHEMA,
                system_instruction=system_instruction
            )
            
            contents = [types.Content(role='user', parts=[types.Part(text=message)])]
            
            max_iterations = 10
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
                
                if not response.function_calls:
                    if response.text:
                        return response.text
                    elif contents:
                        for c in contents:
                            if c.role == 'function':
                                for p in c.parts:
                                    if p.function_response:
                                        return p.function_response.response.get('result', '⚠️ Sin respuesta')
                    return "⚠️ No se pudo obtener una respuesta."
                
                logger.info(f"🔧 Function calls detectados: {[fc.name for fc in response.function_calls]}")
                
                last_function_call_part = None
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if part.function_call:
                            last_function_call_part = part
                            break
                
                function_responses = []
                for fc in response.function_calls:
                    tool_name = fc.name
                    tool_args = dict(fc.args) if fc.args else {}
                    
                    if tool_name in self.tools:
                        logger.info(f"🔧 Ejecutando {tool_name} con args: {tool_args}")
                        try:
                            result = self.tools[tool_name](**tool_args)
                            logger.info(f"🔧 Resultado: {str(result)[:200]}...")
                        except Exception as e:
                            logger.error(f"🔧 Error ejecutando {tool_name}: {e}")
                            result = f"Error: {str(e)}"
                        
                        function_responses.append({
                            "name": tool_name,
                            "result": result
                        })
                
                contents.append(
                    types.Content(role='model', parts=[last_function_call_part]) if last_function_call_part 
                    else types.Content(role='model', parts=[types.Part(text="")])
                )
                
                for fr in function_responses:
                    contents.append(
                        types.Content(role='function', parts=[types.Part(
                            function_response=types.FunctionResponse(
                                name=fr["name"],
                                response={"result": fr["result"]}
                            )
                        )])
                    )
            
            return "⚠️ Demasiadas iteraciones."
            
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
            contents = []
            
            # Convertir historial al formato de Gemini
            for msg in history:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if content:
                    contents.append(types.Content(
                        role=role,
                        parts=[types.Part(text=content)]
                    ))
            
            # Añadir mensaje actual
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=message)]
            ))
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents
            )
            return response.text if response.text else "⚠️ Sin respuesta"
        except Exception as e:
            logger.error(f"Error en chat con historial: {e}")
            return "⚠️ Lo siento, hubo un error."
