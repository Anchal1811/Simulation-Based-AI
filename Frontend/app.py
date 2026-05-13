import streamlit as st
import requests
import time

# 1. Page Configuration
st.set_page_config(
    page_title="CausalAI | Clinical Decision Support",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Enhanced CSS Overhaul
st.markdown("""
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(180deg, #F0F4F8 0%, #FFFFFF 100%);
    }
    
    /* Sidebar Overhaul */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E293B;
    }
    
    /* Styled Chips for Tech Stack */
    .tech-chip {
        display: inline-block;
        padding: 4px 12px;
        margin: 4px 2px;
        border-radius: 15px;
        background-color: #1E293B;
        border: 1px solid #334155;
        color: #94A3B8;
        font-size: 0.75rem;
        font-weight: 500;
    }

    /* Clinical Result Card */
    .report-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 16px;
        border-left: 6px solid #2563EB;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
        color: #1E293B;
    }

    /* Input Field Styling */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #CBD5E1 !important;
        background-color: #FFFFFF !important;
    }

    /* Primary Button Customization */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2563EB 0%, #1D4ED8 100%);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 10px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    
    /* Secondary/Clear Button */
    div.stButton > button:last-child {
        background-color: transparent;
        color: #64748B;
        border: 1px solid #E2E8F0;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Technical Stack
with st.sidebar:
    st.markdown("<h1 style='color: white; font-size: 1.5rem;'>🏥 System Hub</h1>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("### 🟢 Connection Status")
        st.caption("Backend: Active (Groq API)")
        
    st.divider()
    
    st.markdown("### 🛠️ Tech Stack")
    st.markdown("""
        <div class='tech-chip'>Llama 3.1</div>
        <div class='tech-chip'>ChromaDB</div>
        <div class='tech-chip'>FastAPI</div>
        <div class='tech-chip'>RAG</div>
        """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 🧬 Methodology")
    st.info("Utilizes Causal-RAG to map patient symptoms against longitudinal clinical datasets.")

# 4. Header Section
col_title, col_status = st.columns([4, 1])
with col_title:
    st.markdown("<h1 style='color: #0F172A; margin-bottom: 0;'>Clinical Decision Support</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 1.1rem;'>AI-Driven Causal Analysis for Precision Medicine</p>", unsafe_allow_html=True)

st.write("")

# 5. Main Layout
col1, col2 = st.columns([1, 1.8], gap="large")

with col1:
    st.markdown("#### 📥 Patient Presentation")
    query = st.text_area(
        label="Clinical Narrative",
        placeholder="Describe symptoms, medical history, or current vitals...",
        height=300,
        label_visibility="collapsed"
    )
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        analyze_btn = st.button("Generate Analysis")
    with btn_col2:
        if st.button("Clear Input"):
            st.rerun()

with col2:
    st.markdown("#### 🩺 Diagnostic Insights")
    
    if analyze_btn:
        if not query.strip():
            st.warning("Action required: Please provide patient clinical data.")
        else:
            with st.spinner("Analyzing causal nodes..."):
                try:
                    # Simulation of API Call
                    backend_url = "http://127.0.0.1:8000/analyze"
                    # response = requests.post(backend_url, json={"query": query})
                    # result = response.json().get("answer")
                    
                    time.sleep(1.5) # Simulated delay
                    result = "Example Analysis: Based on the symptoms described, there is a high correlation with Secondary Hypertension. Recommend checking renal artery stenosis."

                    st.markdown(f"""
                        <div class="report-card">
                            <span style="background-color: #DBEAFE; color: #1E40AF; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: bold;">CONFIDENTIAL REPORT</span>
                            <h3 style="color: #0F172A; margin-top: 15px;">🔍 AI Decision Synthesis</h3>
                            <p style="font-size: 0.85em; color: #64748B;">Reference ID: CDSS-{int(time.time())}</p>
                            <hr style="border: 0.1px solid #F1F5F9; margin: 20px 0;">
                            <div style="line-height: 1.7; font-size: 1rem; color: #334155;">
                                {result}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📄 Download Clinical Summary",
                        data=result,
                        file_name="cdss_summary.txt",
                        mime="text/plain"
                    )
                except:
                    st.error("System Offline: Connection to FastAPI backend failed.")
    else:
        # Professional placeholder
        st.markdown("""
            <div style="text-align: center; padding: 60px; border: 2px dashed #E2E8F0; border-radius: 16px;">
                <h4 style="color: #94A3B8;">Ready for Analysis</h4>
                <p style="color: #CBD5E1;">Submit patient data on the left to begin the causal simulation.</p>
            </div>
        """, unsafe_allow_html=True)

# 6. Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("🛡️ Compliance: System designed for research support. All outputs must be validated by a licensed physician.")