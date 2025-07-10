import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict, Optional
import json

class DatabaseManager:
    def __init__(self):
        self.connection_string = os.environ.get("DATABASE_URL")
        if self.connection_string and self.connection_string.startswith("postgres://"):
            # Convert postgres:// to postgresql:// for psycopg2 compatibility
            self.connection_string = self.connection_string.replace("postgres://", "postgresql://", 1)
        self.init_database()
    
    def get_connection(self):
        return psycopg2.connect(self.connection_string)
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    # Create chats table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS chats (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # Create messages table
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS messages (
                            id SERIAL PRIMARY KEY,
                            chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE,
                            role VARCHAR(50) NOT NULL,
                            content TEXT NOT NULL,
                            personality VARCHAR(100),
                            color VARCHAR(20),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # Create index for better performance
                    cur.execute("""
                        CREATE INDEX IF NOT EXISTS idx_messages_chat_id 
                        ON messages(chat_id);
                    """)
                    
                    conn.commit()
        except Exception as e:
            print(f"Database initialization failed: {e}")
            # For now, continue without database - will use in-memory fallback
    
    def create_chat(self, title: str) -> int:
        """Create a new chat session"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO chats (title) 
                    VALUES (%s) 
                    RETURNING id
                """, (title,))
                chat_id = cur.fetchone()[0]
                conn.commit()
                return chat_id
    
    def get_all_chats(self) -> List[Dict]:
        """Get all chat sessions"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT c.id, c.title, c.created_at, c.updated_at,
                           COUNT(m.id) as message_count
                    FROM chats c
                    LEFT JOIN messages m ON c.id = m.chat_id
                    GROUP BY c.id, c.title, c.created_at, c.updated_at
                    ORDER BY c.updated_at DESC
                """)
                return [dict(row) for row in cur.fetchall()]
    
    def get_chat_messages(self, chat_id: int) -> List[Dict]:
        """Get all messages for a specific chat"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT role, content, personality, color, created_at
                    FROM messages
                    WHERE chat_id = %s
                    ORDER BY created_at ASC
                """, (chat_id,))
                return [dict(row) for row in cur.fetchall()]
    
    def add_message(self, chat_id: int, role: str, content: str, 
                   personality: str = None, color: str = None):
        """Add a message to a chat"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO messages (chat_id, role, content, personality, color)
                    VALUES (%s, %s, %s, %s, %s)
                """, (chat_id, role, content, personality, color))
                
                # Update chat's updated_at timestamp
                cur.execute("""
                    UPDATE chats 
                    SET updated_at = CURRENT_TIMESTAMP 
                    WHERE id = %s
                """, (chat_id,))
                
                conn.commit()
    
    def delete_chat(self, chat_id: int):
        """Delete a chat and all its messages"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM chats WHERE id = %s", (chat_id,))
                conn.commit()
    
    def update_chat_title(self, chat_id: int, title: str):
        """Update chat title"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE chats 
                    SET title = %s, updated_at = CURRENT_TIMESTAMP 
                    WHERE id = %s
                """, (title, chat_id))
                conn.commit()
    
    def get_chat_info(self, chat_id: int) -> Optional[Dict]:
        """Get chat information"""
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, title, created_at, updated_at
                    FROM chats
                    WHERE id = %s
                """, (chat_id,))
                row = cur.fetchone()
                return dict(row) if row else None