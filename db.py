"""
OpenNemesis - Persistencia de Historial
Módulo SQLite para guardar historial de conversación
"""

import sqlite3
import os
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger("OpenNemesis.DB")

DB_PATH = Path("conversations.db")


def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Base de datos inicializada: {DB_PATH}")
    except Exception as e:
        logger.error(f"✗ Error inicializando base de datos: {e}")
        raise


def save_message(role: str, content: str):
    """Guarda un mensaje en la base de datos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (role, content, created_at) VALUES (?, ?, ?)",
            (role, content, datetime.now().isoformat())
        )
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"✗ Error guardando mensaje: {e}")


def get_history(limit: int = 50) -> list:
    """Obtiene los últimos N mensajes del historial"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content FROM messages ORDER BY id ASC LIMIT ?",
            (limit,)
        )
        
        messages = cursor.fetchall()
        conn.close()
        
        return [{"role": m[0], "content": m[1]} for m in messages]
    except Exception as e:
        logger.error(f"✗ Error obteniendo historial: {e}")
        return []


def clear_history():
    """Borra todos los mensajes del historial"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM messages")
        
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        
        logger.info(f"✓ Historial borrado: {deleted_count} mensajes eliminados")
        return deleted_count
    except Exception as e:
        logger.error(f"✗ Error borrando historial: {e}")
        return 0


def get_message_count() -> int:
    """Retorna el número total de mensajes en la base de datos"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        
        conn.close()
        return count
    except Exception as e:
        logger.error(f"✗ Error contando mensajes: {e}")
        return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("=== DB Test ===")
    init_db()
    print(f"Mensajes en DB: {get_message_count()}")
