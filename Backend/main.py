import sys
import os

# --- PERMANENT PATH FIX START ---
# This forces the script to find the 'deps' folder you just created
current_dir = os.path.dirname(os.path.abspath(__file__))
deps_path = os.path.join(current_dir, 'deps')
if deps_path not in sys.path:
    sys.path.insert(0, deps_path)
# --- PERMANENT PATH FIX END ---

from fastapi import FastAPI, UploadFile, File, Body
from core.rag_engine import HealthcareAI 
from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter
# This already has its own package (langchain-chroma)
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Healthcare AI DSS")

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