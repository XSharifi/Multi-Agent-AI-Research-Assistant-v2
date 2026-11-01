from sqlalchemy import create_engine, text
from app.config import get_settings

engine = create_engine(get_settings().database_url, pool_pre_ping=True)

def init_db():
    with engine.begin() as c:
        c.execute(text("""CREATE TABLE IF NOT EXISTS memories (
            id SERIAL PRIMARY KEY, thread_id TEXT NOT NULL,
            memory_type TEXT NOT NULL, content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""))

def save_memory(thread_id, memory_type, content):
    with engine.begin() as c:
        c.execute(text("INSERT INTO memories(thread_id,memory_type,content) VALUES (:t,:m,:c)"),
                  {"t":thread_id,"m":memory_type,"c":content})

def get_memories(thread_id, limit=10):
    with engine.begin() as c:
        rows = c.execute(text("""SELECT id,thread_id,memory_type,content,created_at
            FROM memories WHERE thread_id=:t ORDER BY created_at DESC LIMIT :n"""),
                         {"t":thread_id,"n":limit}).mappings().all()
    return [dict(r) for r in rows]
