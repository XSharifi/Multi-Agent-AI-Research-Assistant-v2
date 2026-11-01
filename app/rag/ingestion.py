import fitz
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.retriever import add_documents

def load_pdf(path):
    d=fitz.open(path); docs=[]
    for n,p in enumerate(d):
        text=p.get_text()
        if text.strip():
            docs.append(Document(page_content=text, metadata={"source":str(path),"page":n+1}))
    d.close()
    return docs

def split_documents(docs):
    return RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150).split_documents(docs)

def ingest_pdf(path):
    chunks=split_documents(load_pdf(path))
    if chunks: add_documents(chunks)
    return len(chunks)
