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

DB_PATH = Path("data/conversations.db")


def init_db():
    """Inicializa la base de datos y crea la tabla si no existe"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DROP TABLE IF EXISTS messages")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON messages(user_id)")
        
        conn.commit()
        conn.close()
        
        logger.info(f"✓ Base de datos inicializada: {DB_PATH}")
    except Exception as e:
        logger.error(f"✗ Error inicializando base de datos: {e}")
        raise


def save_message(user_id: str, role: str, content: str):
    """Guarda un mensaje en la base de datos para un usuario específico"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO messages (user_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (user_id, role, content, datetime.now().isoformat())
        )
        
        conn.commit()
        conn.close()
        
        logger.info(f"DB: Guardado mensaje para user_id={user_id}, role={role}")
    except Exception as e:
        logger.error(f"✗ Error guardando mensaje: {e}")


def get_history(user_id: str, limit: int = 50) -> list:
    """Obtiene los últimos N mensajes del historial de un usuario"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content FROM messages WHERE user_id = ? ORDER BY id ASC LIMIT ?",
            (user_id, limit)
        )
        
        messages = cursor.fetchall()
        conn.close()
        
        return [{"role": m[0], "content": m[1]} for m in messages]
    except Exception as e:
        logger.error(f"✗ Error obteniendo historial: {e}")
        return []


def clear_history(user_id: str) -> int:
    """Borra los mensajes del historial de un usuario específico"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM messages WHERE user_id = ?", (user_id,))
        
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        
        logger.info(f"✓ Historial borrado para usuario {user_id}: {deleted_count} mensajes eliminados")
        return deleted_count
    except Exception as e:
        logger.error(f"✗ Error borrando historial: {e}")
        return 0


def get_message_count(user_id: str) -> int:
    """Retorna el número de mensajes de un usuario específico"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM messages WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        
        conn.close()
        
        logger.info(f"DB: Consultando user_id={user_id}, mensajes encontrados={count}")
        return count
    except Exception as e:
        logger.error(f"✗ Error contando mensajes: {e}")
        return 0


def get_total_message_count() -> int:
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
