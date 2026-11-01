import json
from langchain_core.messages import HumanMessage, SystemMessage
from app.agents import get_llm

def classify_task(query):
    r=get_llm().invoke([SystemMessage(content="""Route the request. Available agents: research, paper, coding, evaluation.
Return ONLY JSON: {"task_type":"research|paper|coding|mixed","route":["..."]}.
Always include evaluation. Research=external/current sources; paper=indexed PDFs; coding=Python experiments."""),
                        HumanMessage(content=query)])
    try:
        return json.loads(r.content)
    except Exception:
        return {"task_type":"mixed","route":["research","paper","evaluation"]}

def final_report_agent(state):
    r=get_llm().invoke([SystemMessage(content="Write a scientific report from state evidence only. Do not fabricate citations. Include findings, evidence, experiments, evaluation, limitations, and next steps."),
                        HumanMessage(content=f"QUESTION:{state.get('user_query')}\nMEMORY:{state.get('memory_context')}\nWEB:{state.get('web_results')}\nPAPER:{state.get('papers')}\nCODE:{state.get('code')}\nOUTPUT:{state.get('code_output')}\nEVAL:{state.get('evaluation')}")])
    return {"final_report":r.content}
