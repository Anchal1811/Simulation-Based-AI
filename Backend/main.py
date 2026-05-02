from fastapi import FastAPI, UploadFile, File, Body
from core.rag_engine import HealthcareAI 
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Use updated Chroma import to avoid deprecation warnings
from langchain_chroma import Chroma 
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Healthcare AI DSS")

# FIX: Removed hardcoded API key fallback to satisfy GitHub security
raw_key = os.getenv("GROQ_API_KEY")

if not raw_key:
    raise ValueError("CRITICAL ERROR: GROQ_API_KEY not found. Ensure it is set in your .env file.")

ai_engine = HealthcareAI(api_key=raw_key)

@app.post("/ingest")
async def ingest_medical_data(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f: 
        f.write(await file.read())
    
    loader = PyPDFLoader(path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(loader.load())
    
    Chroma.from_documents(
        chunks, 
        ai_engine.embeddings, 
        persist_directory=ai_engine.vector_db_path
    )
    
    os.remove(path)
    return {"message": "Knowledge base updated successfully."}

@app.post("/analyze")
async def analyze_query(query: str = Body(..., embed=True)):
    response = ai_engine.get_response(query)
    return {"analysis": response}