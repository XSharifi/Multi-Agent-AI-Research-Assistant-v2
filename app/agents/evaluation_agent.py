from langchain_core.messages import HumanMessage, SystemMessage
from app.agents import get_llm

def evaluation_agent(state):
    r=get_llm().invoke([SystemMessage(content="Evaluate evidence support, source quality, relevance, completeness, hallucination risk, and experiment validity."),
                        HumanMessage(content=f"Question:{state.get('user_query')}\nWeb:{state.get('web_results')}\nPaper:{state.get('papers')}\nCode:{state.get('code')}\nOutput:{state.get('code_output')}")])
    return {"evaluation":{"report":r.content}}
