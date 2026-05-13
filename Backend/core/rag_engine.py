import os
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

class HealthcareAI:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            # FIX: Change decommissioned model to llama-3.1-8b-instant
            model="llama-3.1-8b-instant", 
            groq_api_key=api_key,
            temperature=0
        )
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_db_path = "./chroma_db"

    def get_response(self, query: str):
        db = Chroma(
            persist_directory=self.vector_db_path, 
            embedding_function=self.embeddings
        )
        
        # Modern Prompt Template for 0.3.x
        system_prompt = (
            "You are a Clinical Decision Support AI. "
            "Use the following retrieved medical context to provide a technical analysis. "
            "If the answer is not in the context, state that insufficient clinical data is present.\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        # Create the chains the modern way
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(db.as_retriever(), question_answer_chain)
        
        # Execute
        response = rag_chain.invoke({"input": query})
        return response["answer"]