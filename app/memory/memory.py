from app.database.database import get_memories, save_memory

def load_memory(thread_id):
    return get_memories(thread_id)

def remember(thread_id, memory_type, content):
    save_memory(thread_id, memory_type, content)
