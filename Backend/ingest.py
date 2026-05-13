import os
import shutil
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma  # Updated to the new standalone package

# --- CONFIGURATION ---
DATA_PATH = "./data"
DB_PATH = "./chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

def run_ingestion():
    # 1. Clean existing database to avoid version conflicts
    if os.path.exists(DB_PATH):
        print(f" Removing old database at {DB_PATH}...")
        shutil.rmtree(DB_PATH)

    print(" Starting Ingestion for Overall Health Knowledge Base...")

    # 2. Support multiple file types (PDF and TXT) for overall health data
    # Loading PDFs
    pdf_loader = DirectoryLoader(DATA_PATH, glob="./*.pdf", loader_cls=PyPDFLoader)
    # Loading Text files (for your overall_health_corpus.txt)
    txt_loader = DirectoryLoader(DATA_PATH, glob="./*.txt", loader_cls=TextLoader)

    print(" Loading documents...")
    docs = pdf_loader.load() + txt_loader.load()
    
    if not docs:
        print(" Error: No documents found in ./data. Please add PDFs or TXT files.")
        return

    # 3. Intelligent Splitting
    # We use a smaller chunk_size (800) for medical data to keep context precise
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        add_start_index=True,
        strip_whitespace=True,
        separators=["\n\n", "\n", ".", " "]
    )
    
    print(f"✂️ Splitting {len(docs)} documents into chunks...")
    chunks = text_splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} unique knowledge chunks.")

    # 4. Initialize Embeddings
    print(f"🧠 Generating embeddings using {EMBED_MODEL}...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    # 5. Create and Persist Vector Database
    print(f"💾 Saving to {DB_PATH}...")
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    print("\n" + "="*30)
    print("✅ SUCCESS: Clinical Knowledge Base Rebuilt!")
    print(f"📍 Location: {DB_PATH}")
    print(f"📚 Total Chunks Indexed: {len(chunks)}")
    print("="*30)

if __name__ == "__main__":
    run_ingestion()