from langchain_openai import ChatOpenAI
from app.config import get_settings

def get_llm():
    s = get_settings()
    return ChatOpenAI(model=s.llm_model, temperature=s.temperature, api_key=s.openai_api_key)
