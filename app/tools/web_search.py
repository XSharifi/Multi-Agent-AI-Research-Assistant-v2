from langchain_core.tools import tool
from langchain_tavily import TavilySearch

@tool
def web_search(query: str) -> str:
    """Search the web for research information."""
    return str(TavilySearch(max_results=5).invoke({"query": query}))
