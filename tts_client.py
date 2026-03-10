"""
OpenNemesis - Text to Speech
Usando Edge TTS (gratuito)
"""

import asyncio
import io
import logging

logger = logging.getLogger("OpenNemesis.TTS")

VOICES = {
    "es": "es-ES-ElviraNeural",
    "en": "en-US-JennyNeural",
    "default": "es-ES-ElviraNeural"
}

async def text_to_speech(text: str, lang: str = "es") -> bytes:
    """Convierte texto a audio usando Edge TTS"""
    try:
        import edge_tts
        
        voice = VOICES.get(lang, VOICES["default"])
        
        communicate = edge_tts.Communicate(text, voice)
        
        audio_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        
        audio_buffer.seek(0)
        logger.info(f"✓ TTS generado: {len(audio_buffer.getvalue())} bytes")
        return audio_buffer.getvalue()
        
    except Exception as e:
        logger.error(f"Error en TTS: {e}")
        return None


def text_to_speech_sync(text: str, lang: str = "es") -> bytes:
    """Versión síncrona de TTS"""
    return asyncio.run(text_to_speech(text, lang))
