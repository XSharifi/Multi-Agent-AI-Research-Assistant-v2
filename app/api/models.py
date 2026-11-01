from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    query:str=Field(min_length=3)
    thread_id:str="default"
    execution_requested:bool=False

class ResearchResponse(BaseModel):
    report:str
    evaluation:dict
    route:list[str]

class ApprovalRequest(BaseModel):
    approved:bool
    feedback:str=""

class PDFIngestionResponse(BaseModel):
    filename:str
    chunks_added:int

class MemoryResponse(BaseModel):
    memories:list[dict]
