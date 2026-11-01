import sqlite3
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from app.config import get_settings
from app.graph.state import ResearchState
from app.graph.hitl import approval_node
from app.agents.orchestrator import classify_task, final_report_agent
from app.agents.research_agent import research_agent
from app.agents.paper_agent import paper_agent
from app.agents.coding_agent import coding_agent, execute_approved_code
from app.agents.evaluation_agent import evaluation_agent

def build_graph():
    g=StateGraph(ResearchState)
    g.add_node("orchestrator",lambda s:{**classify_task(s["user_query"])})
    g.add_node("research",research_agent); g.add_node("paper",paper_agent)
    g.add_node("coding",coding_agent); g.add_node("human_approval",approval_node)
    g.add_node("execute_code",execute_approved_code); g.add_node("evaluation",evaluation_agent)
    g.add_node("final_report",final_report_agent)
    g.add_edge(START,"orchestrator")
    g.add_conditional_edges("orchestrator",lambda s:(s.get("route") or ["evaluation"])[0],
                            {"research":"research","paper":"paper","coding":"coding","evaluation":"evaluation"})
    def nxt(name):
        def f(s):
            route=s.get("route",[])
            try: i=route.index(name)
            except ValueError: return "final_report"
            return route[i+1] if i+1<len(route) else "final_report"
        return f
    for name in ["research","paper","evaluation"]:
        g.add_conditional_edges(name,nxt(name),
            {"research":"research","paper":"paper","coding":"coding","evaluation":"evaluation","final_report":"final_report"})
    g.add_conditional_edges("coding",
        lambda s:"human_approval" if s.get("execution_requested") else nxt("coding")(s),
        {"human_approval":"human_approval","research":"research","paper":"paper","evaluation":"evaluation","final_report":"final_report"})
    g.add_edge("human_approval","execute_code"); g.add_edge("execute_code","evaluation")
    g.add_edge("final_report",END)
    conn=sqlite3.connect(get_settings().sqlite_checkpoint_path,check_same_thread=False)
    return g.compile(checkpointer=SqliteSaver(conn))
