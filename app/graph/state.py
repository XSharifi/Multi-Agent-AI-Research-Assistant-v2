from typing import Any, TypedDict

class ResearchState(TypedDict, total=False):
    user_query: str
    thread_id: str
    task_type: str
    route: list[str]
    web_results: list[dict[str, Any]]
    papers: list[dict[str, Any]]
    retrieved_documents: list[dict[str, Any]]
    code: str
    code_output: str
    execution_requested: bool
    evaluation: dict[str, Any]
    requires_human_review: bool
    human_approved: bool
    human_feedback: str
    memory_context: list[dict[str, Any]]
    final_report: str
