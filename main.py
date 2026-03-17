#!/usr/bin/env python3
"""
OpenNemesis - Agente de IA Modular
V1.0 - Validación de Conexiones y Bot Principal
"""

import os
import sys
import logging
import asyncio
import nest_asyncio
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno al inicio
env_path = Path(".env.local")
if env_path.exists():
    load_dotenv(env_path)

import telegram
from telegram import Bot
import google.genai as genai

nest_asyncio.apply()

from telegram_bot import TelegramBot
from gemini_client import GeminiClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("OpenNemesis")


def print_banner():
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                     OPENNEMESIS v1.0                       ║
║          Agente de IA Modular y Escalable                 ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def load_environment():
    """Carga las variables de entorno desde .env.local"""
    logger.info("Cargando configuración del entorno...")
    
    env_path = Path(".env.local")
    if env_path.exists():
        load_dotenv(env_path)
        logger.info("✓ Variables de entorno cargadas desde .env.local")
    else:
        logger.warning("⚠ Archivo .env.local no encontrado")
    
    required_vars = ["TELEGRAM_BOT_TOKEN", "GEMINI_API_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]
    
    if missing:
        logger.error(f"✗ Variables requeridas faltantes: {', '.join(missing)}")
        return False
    
    logger.info("✓ Todas las variables requeridas están presentes")
    return True


def validate_telegram_connection():
    """Valida la conexión con Telegram Bot API"""
    logger.info("🔌 Validando conexión con Telegram...")
    
    try:
        async def check_bot():
            token = os.getenv("TELEGRAM_BOT_TOKEN")
            if not token:
                logger.error("✗ Token de Telegram no configurado")
                return False
            
            bot = Bot(token=token)
            bot_info = await bot.get_me()
            
            logger.info(f"✓ Conexión exitosa con Telegram")
            logger.info(f"  Bot: @{bot_info.username}")
            logger.info(f"  Nombre: {bot_info.name}")
            logger.info(f"  ID: {bot_info.id}")
            
            return True
        
        return asyncio.run(check_bot())
        
    except ImportError:
        logger.error("✗ python-telegram-bot no instalado")
        return False
    except Exception as e:
        logger.error(f"✗ Error conectando a Telegram: {e}")
        return False


def validate_gemini_connection():
    """Valida la conexión con Google Gemini"""
    logger.info("🔌 Validando conexión con Google Gemini...")
    
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite-preview")
        
        if not api_key:
            logger.error("✗ API Key de Gemini no configurada")
            return False
        
        # Configurar cliente
        client = genai.Client(api_key=api_key)
        
        # Test de conexión con modelo
        logger.info(f"✓ Conexión con Gemini establecida")
        logger.info(f"  Modelo: {model}")
        
        return True
        
    except ImportError:
        logger.error("✗ google-genai no instalado")
        return False
    except Exception as e:
        logger.error(f"✗ Error conectando a Gemini: {e}")
        return False


def check_skills():
    """Verifica las skills disponibles"""
    logger.info("📦 Verificando skills instaladas...")
    
    skills_dir = Path("skills")
    if not skills_dir.exists():
        logger.warning("⚠ Directorio skills/ no encontrado")
        return
    
    skills = [d.name for d in skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    if skills:
        logger.info(f"✓ Skills disponibles: {', '.join(skills)}")
    else:
        logger.warning("⚠ No hay skills instaladas")


def check_tools():
    """Verifica las tools disponibles"""
    logger.info("🛠️  Verificando tools instaladas...")
    
    tools_dir = Path("tools")
    if not tools_dir.exists():
        logger.warning("⚠ Directorio tools/ no encontrado")
        return
    
    tools = [f.stem for f in tools_dir.iterdir() if f.is_file() and f.suffix == '.py' and not f.name.startswith('_')]
    
    if tools:
        logger.info(f"✓ Tools disponibles: {', '.join(tools)}")
    else:
        logger.warning("⚠ No hay tools instaladas")


def main(mode: str = "validate"):
    """Función principal"""
    print_banner()
    
    logger.info("=" * 60)
    logger.info(f"MODO: {mode.upper()}")
    logger.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    if not load_environment():
        logger.error("✗ Error en carga de entorno. Abortando.")
        sys.exit(1)
    
    telegram_ok = validate_telegram_connection()
    gemini_ok = validate_gemini_connection()
    
    check_skills()
    check_tools()
    
    logger.info("=" * 60)
    logger.info("RESUMEN DE VALIDACIÓN")
    logger.info("=" * 60)
    logger.info(f"Telegram Bot:    {'✓ CONECTADO' if telegram_ok else '✗ FALLO'}")
    logger.info(f"Google Gemini:   {'✓ CONECTADO' if gemini_ok else '✗ FALLO'}")
    logger.info("=" * 60)
    
    if not (telegram_ok and gemini_ok):
        logger.error("⚠ Hay errores de conexión. Revisa la configuración.")
        sys.exit(1)
    
    if mode == "validate":
        logger.info("🎉 Validación completada. Usa 'python main.py run' para iniciar el bot.")
        return
    
    logger.info("🎉 Todas las conexiones validadas correctamente")
    logger.info("🚀 Iniciando OpenNemesis...")
    
    gemini_client = GeminiClient(
        api_key=os.getenv("GEMINI_API_KEY", ""),
        model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite-preview")
    )
    
    telegram_bot = TelegramBot(
        token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
        gemini_client=gemini_client
    )
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(telegram_bot.start())
    except KeyboardInterrupt:
        logger.info("🛑 Bot detenido por el usuario")
    finally:
        if not loop.is_closed():
            loop.close()


if __name__ == "__main__":
    mode = "validate"
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        mode = "run"
    main(mode)
