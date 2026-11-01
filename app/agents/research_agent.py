from langchain_core.messages import HumanMessage, SystemMessage
from app.agents import get_llm
from app.tools.web_search import web_search

def research_agent(state):
    r=get_llm().bind_tools([web_search]).invoke([
        SystemMessage(content="You are a research agent. Use web search for external evidence. Prefer primary academic sources and never invent references."),
        HumanMessage(content=state["user_query"])])
    results=[]
    for call in r.tool_calls:
        if call["name"]=="web_search":
            results.append({"query":call["args"]["query"],"result":web_search.invoke(call["args"])})
    return {"web_results":results}
