from fastapi import FastAPI, UploadFile, File
import shutil
import os

from vector_store import create_vector_store
from rag_pipeline import load_rag

app = FastAPI()

UPLOAD_PATH = "data/uploaded.pdf"

# Ensure data folder exists
os.makedirs("data", exist_ok=True)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Save uploaded file
    with open(UPLOAD_PATH, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Create FAISS vector index
    create_vector_store(UPLOAD_PATH)

    return {"message": "PDF uploaded and processed successfully"}


@app.post("/ask")
async def ask_question(question: str):

    # Check if FAISS index exists
    if not os.path.exists("faiss_index"):
        return {"error": "Please upload a PDF first"}

    # Load RAG pipeline
    qa_chain = load_rag()

    result = qa_chain({"query": question})

    answer = result["result"]

    sources = [
        doc.metadata.get("source", "unknown")
        for doc in result["source_documents"]
    ]

    return {
        "answer": answer,
        "sources": sources
    }