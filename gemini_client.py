"""
OpenNemesis - Gemini Client
Cliente para Google Gemini con soporte multimodal, tools y skills
"""

import logging
from typing import Union

logger = logging.getLogger("OpenNemesis.Gemini")

from prompt import get_system_prompt, reload_skills_context

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
            import subprocess
            import os
            
            def execute_command(command: str) -> str:
                """Execute a shell command"""
                try:
                    env = os.environ.copy()
                    env["GOG_ACCOUNT"] = os.getenv("GOG_ACCOUNT", "")
                    if "/opt/gogcli" not in env.get("PATH", ""):
                        env["PATH"] = "/opt/gogcli:" + env.get("PATH", "")
                    
                    result = subprocess.run(
                        command,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=60,
                        env=env
                    )
                    if result.returncode != 0:
                        return f"Error: {result.stderr}"
                    return result.stdout if result.stdout else "Comando ejecutado correctamente."
                except subprocess.TimeoutExpired:
                    return "Error: Timeout ejecutando comando"
                except Exception as e:
                    return f"Error: {str(e)}"
            
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
            from google.genai import types
            
            system_instruction = get_system_prompt()
            if SKILLS_CONTEXT:
                system_instruction += "\n\n" + SKILLS_CONTEXT
            
            config = types.GenerateContentConfig(
                tools=TOOLS_SCHEMA,
                system_instruction=system_instruction
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
