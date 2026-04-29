import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Causal AI Decision Support", layout="wide")

st.title("🩺 Causal AI Treatment Simulator")
st.write("This system uses **Structural Causal Modeling** to simulate patient outcomes.")

# Sidebar for inputs
with st.sidebar:
    st.header("Simulation Settings")
    sample_size = st.slider("Number of Patients", 100, 5000, 1000)
    if st.button("Run Simulation"):
        # We call your FastAPI backend here
        response = requests.get(f"http://127.0.0.1:8000/test-data?samples={sample_size}")
        if response.status_code == 200:
            st.session_state['data'] = response.json()
            st.success("Data received from Backend!")
        else:
            st.error("Could not connect to Backend. Is it running?")

# Main Dashboard
if 'data' in st.session_state:
    df = pd.DataFrame(st.session_state['data'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Simulated Patient Data")
        st.dataframe(df.head(10))
        
    with col2:
        st.subheader("Distribution of Recovery")
        st.bar_chart(df['Recovery'].head(50))

    st.divider()
    st.info("Next Step: Integrate the Causal Brain to see the 'True Effect' sliders.")
else:
    st.warning("Please click 'Run Simulation' in the sidebar to fetch data.")