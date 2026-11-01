from fastapi import FastAPI
from app.api.routes import router
app=FastAPI(title="Multi-Agent AI Research Assistant",version="0.2.0")
app.include_router(router,prefix="/api")
@app.get("/")
def root(): return {"name":"Multi-Agent AI Research Assistant","version":"0.2.0","status":"running"}
@app.get("/health")
def health(): return {"status":"healthy"}
