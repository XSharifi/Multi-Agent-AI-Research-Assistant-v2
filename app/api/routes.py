import shutil, tempfile
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from langgraph.types import Command
from app.api.models import *
from app.database.database import init_db,get_memories,save_memory
from app.graph.workflow import build_graph
from app.rag.ingestion import ingest_pdf

router=APIRouter(); graph=build_graph(); init_db()

@router.post("/research",response_model=ResearchResponse)
async def research(req:ResearchRequest):
    cfg={"configurable":{"thread_id":req.thread_id}}
    result=graph.invoke({"user_query":req.query,"thread_id":req.thread_id,
                         "execution_requested":req.execution_requested,
                         "memory_context":get_memories(req.thread_id)},config=cfg)
    save_memory(req.thread_id,"research_request",req.query)
    return ResearchResponse(report=result.get("final_report",""),evaluation=result.get("evaluation",{}),route=result.get("route",[]))

@router.post("/research/{thread_id}/resume")
async def resume(thread_id:str,req:ApprovalRequest):
    cfg={"configurable":{"thread_id":thread_id}}
    result=graph.invoke(Command(resume={"approved":req.approved,"feedback":req.feedback}),config=cfg)
    return {"status":"resumed","report":result.get("final_report",""),"evaluation":result.get("evaluation",{})}

@router.post("/papers/ingest",response_model=PDFIngestionResponse)
async def ingest(file:UploadFile=File(...)):
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400,"Only PDF files are accepted.")
    with tempfile.TemporaryDirectory() as d:
        path=Path(d)/file.filename
        with path.open("wb") as out: shutil.copyfileobj(file.file,out)
        n=ingest_pdf(str(path))
    return PDFIngestionResponse(filename=file.filename,chunks_added=n)

@router.get("/memory/{thread_id}",response_model=MemoryResponse)
async def memory(thread_id:str):
    return MemoryResponse(memories=get_memories(thread_id))
