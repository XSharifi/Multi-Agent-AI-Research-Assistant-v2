from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    tavily_api_key: str
    langchain_api_key: str | None = None
    langchain_tracing_v2: bool = True
    langchain_project: str = "multi-agent-research-assistant"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/research_assistant"
    llm_model: str = "gpt-5-mini"
    temperature: float = 0.0
    chroma_path: str = "./data/chroma"
    sqlite_checkpoint_path: str = "./data/checkpoints.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings():
    return Settings()
