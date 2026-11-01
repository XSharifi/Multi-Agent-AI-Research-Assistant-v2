from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import get_settings

def get_vector_store():
    s=get_settings()
    return Chroma(collection_name="research_papers",
                  embedding_function=OpenAIEmbeddings(model="text-embedding-3-small", api_key=s.openai_api_key),
                  persist_directory=s.chroma_path)

def add_documents(documents):
    vs=get_vector_store(); vs.add_documents(documents); return vs

def get_retriever():
    return get_vector_store().as_retriever(search_kwargs={"k":5})
