import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Causal AI - Healthcare DSS", page_icon="🏥", layout="wide")

st.title("🏥 Simulation-Based Causal AI")
st.markdown("---")

# Sidebar for Ingestion
with st.sidebar:
    st.header("1. Data Ingestion")
    uploaded_file = st.file_uploader("Upload Medical PDF", type=["pdf"])
    if st.button("Upload & Process"):
        if uploaded_file:
            with st.spinner("Processing PDF..."):
                files = {"file": uploaded_file.getvalue()}
                # Sending the file to the FastAPI /ingest endpoint
                response = requests.post("http://127.0.0.1:8000/ingest", files={"file": (uploaded_file.name, uploaded_file.getvalue())})
                if response.status_code == 200:
                    st.success("Knowledge Base Updated!")
                else:
                    st.error("Upload failed.")
        else:
            st.warning("Please select a file.")

# Main area for Analysis
st.header("2. Clinical Analysis")
query = st.text_input("Enter clinical query or patient symptoms:")

if st.button("Analyze"):
    if query:
        with st.spinner("LLM is analyzing causal factors..."):
            # Sending the query to the FastAPI /analyze endpoint
            # Note: We use json={"query": query} to match the Body(embed=True) in main.py
            payload = {"query": query}
            response = requests.post("http://127.0.0.1:8000/analyze", json=payload)
            
            if response.status_code == 200:
                result = response.json().get("analysis")
                st.subheader("AI Decision Support Result")
                st.info(result)
            else:
                st.error(f"Error: {response.text}")
    else:
        st.warning("Please enter a question.")