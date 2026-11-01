from langgraph.types import interrupt

def approval_node(state):
    decision=interrupt({"type":"code_execution_approval",
                        "question":"Approve execution of this generated Python experiment?",
                        "code":state.get("code","")})
    return {"human_approved":bool(decision.get("approved",False)),
            "human_feedback":str(decision.get("feedback","")),
            "requires_human_review":False}
