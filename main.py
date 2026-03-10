#!/usr/bin/env python3
"""
OpenNemesis - Agente de IA Modular
V1.0 - Validación de Conexiones
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("OpenNemesis")


def print_banner():
    """Muestra el banner de inicio."""
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
        import telegram
        from telegram import Bot
        
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            logger.error("✗ Token de Telegram no configurado")
            return False
        
        bot = Bot(token=token)
        bot_info = bot.get_me()
        
        logger.info(f"✓ Conexión exitosa con Telegram")
        logger.info(f"  Bot: @{bot_info.username}")
        logger.info(f"  Nombre: {bot_info.name}")
        logger.info(f"  ID: {bot_info.id}")
        
        return True
        
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
        import google.genai as genai
        
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-native-audio-latest")
        
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


def main():
    """Función principal de validación"""
    print_banner()
    
    logger.info("=" * 60)
    logger.info("INICIANDO VALIDACIÓN DE CONEXIONES")
    logger.info(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    # Cargar entorno
    if not load_environment():
        logger.error("✗ Error en carga de entorno. Abortando.")
        sys.exit(1)
    
    # Validar conexiones
    telegram_ok = validate_telegram_connection()
    gemini_ok = validate_gemini_connection()
    
    # Verificar estructura
    check_skills()
    check_tools()
    
    # Resumen
    logger.info("=" * 60)
    logger.info("RESUMEN DE VALIDACIÓN")
    logger.info("=" * 60)
    logger.info(f"Telegram Bot:    {'✓ CONECTADO' if telegram_ok else '✗ FALLO'}")
    logger.info(f"Google Gemini:   {'✓ CONECTADO' if gemini_ok else '✗ FALLO'}")
    logger.info("=" * 60)
    
    if telegram_ok and gemini_ok:
        logger.info("🎉 Todas las conexiones validadas correctamente")
        logger.info("OpenNemesis está listo para funcionar")
    else:
        logger.error("⚠ Hay errores de conexión. Revisa la configuración.")
        sys.exit(1)


if __name__ == "__main__":
    main()
