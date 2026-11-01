from langchain_core.messages import HumanMessage, SystemMessage
from app.agents import get_llm
from app.tools.python_sandbox import execute_python_sandboxed

def coding_agent(state):
    r=get_llm().invoke([SystemMessage(content="Generate safe reproducible Python only. No shell, network, subprocess, credential access, or file deletion."),
                        HumanMessage(content=state["user_query"])])
    code=r.content.replace("```python","").replace("```","").strip()
    return {"code":code}

def execute_approved_code(state):
    if not state.get("human_approved"):
        return {"code_output":"Execution not approved."}
    return {"code_output":execute_python_sandboxed.invoke({"code":state.get("code","")})}
