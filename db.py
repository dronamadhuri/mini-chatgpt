import sqlite3
import uuid
import logging
from datetime import datetime

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("db_module")

DB_FILE = "chat_history.db"

def get_connection():
    """Establish connection and guarantee foreign key constraint execution."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection attempt failed: {e}")
        raise

def init_db():
    """Setup table structure safely."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Chats table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                chat_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats (chat_id) ON DELETE CASCADE
            )
        """)
        conn.commit()
        conn.close()
        logger.info("Database schemas initialized successfully.")
    except sqlite3.Error as e:
        logger.error(f"Fatal error during database schemas initialization: {e}")
        raise

def create_new_chat(title="New Chat") -> str:
    """Generate and insert unique chat session, returning UUID string."""
    chat_id = str(uuid.uuid4())
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (chat_id, title) VALUES (?, ?)", (chat_id, title))
        conn.commit()
        conn.close()
        logger.info(f"Database log: Spawned new chat session '{chat_id}'")
        return chat_id
    except sqlite3.Error as e:
        logger.error(f"Database error while spawning new chat: {e}")
        return ""

def save_message(chat_id: str, role: str, content: str):
    """Save user/assistant messages and auto-update title from first user prompt."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
            (chat_id, role, content)
        )
        
        # Auto rename from 'New Chat' to snippet of first user query
        if role == "user":
            cursor.execute("SELECT title FROM chats WHERE chat_id = ?", (chat_id,))
            row = cursor.fetchone()
            if row and row[0] == "New Chat":
                new_title = content[:25] + "..." if len(content) > 25 else content
                cursor.execute("UPDATE chats SET title = ? WHERE chat_id = ?", (new_title, chat_id))
                logger.info(f"Auto-renamed session '{chat_id}' title to: '{new_title}'")
                
        conn.commit()
        conn.close()
        logger.info(f"Database log: Saved message for role '{role}' under session '{chat_id}'")
    except sqlite3.Error as e:
        logger.error(f"Database error saving message to session '{chat_id}': {e}")

def load_chat(chat_id: str) -> list:
    """Load historical conversation ordered chronologically."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content FROM messages WHERE chat_id = ? ORDER BY id ASC",
            (chat_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        logger.info(f"Database log: Restored {len(rows)} message rows for session '{chat_id}'")
        return [{"role": row[0], "content": row[1]} for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Database error reading session '{chat_id}' messages: {e}")
        return []

def list_chats() -> list:
    """Retrieve full list of past conversations sorted by recency."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id, title, created_at FROM chats ORDER BY created_at DESC")
        rows = cursor.fetchall()
        conn.close()
        return [{"chat_id": row[0], "title": row[1], "created_at": row[2]} for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Database error reading chat threads index: {e}")
        return []

def delete_chat(chat_id: str):
    """Delete a chat session and let SQLite cascade delete messages."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
        conn.commit()
        conn.close()
        logger.info(f"Database log: Purged session '{chat_id}' and all message history")
    except sqlite3.Error as e:
        logger.error(f"Database error deleting session '{chat_id}': {e}")

def update_chat_title(chat_id: str, title: str):
    """Update title of a chat session."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE chats SET title = ? WHERE chat_id = ?", (title, chat_id))
        conn.commit()
        conn.close()
        logger.info(f"Database log: Updated title for session '{chat_id}' to: '{title}'")
    except sqlite3.Error as e:
        logger.error(f"Database error updating title for session '{chat_id}': {e}")
