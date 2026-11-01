from langchain_core.messages import HumanMessage, SystemMessage
from app.agents import get_llm
from app.rag.retriever import get_retriever

def paper_agent(state):
    docs=get_retriever().invoke(state["user_query"])
    ctx="\n\n".join(f"Source: {d.metadata.get('source')} page {d.metadata.get('page')}\n{d.page_content}" for d in docs)
    r=get_llm().invoke([SystemMessage(content="Analyze only the retrieved paper evidence; say when evidence is insufficient."),
                        HumanMessage(content=f"Question:\n{state['user_query']}\n\nEvidence:\n{ctx}")])
    return {"retrieved_documents":[{"content":d.page_content,"metadata":d.metadata} for d in docs],
            "papers":[{"analysis":r.content}]}
