import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ANYTHING_LLM_URL = "http://localhost:3001/api/v1"
WORKSPACE_SLUG = "cyberaudit"
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="CyberAudit GPT", page_icon=None, layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
        background-color: #0d0f12;
        color: #e6edf3;
    }

    .stApp {
        background-color: #0d0f12;
    }

    /* ── Header ── */
    .header-block {
        text-align: center;
        padding: 0;
        margin: 0 0 2rem 0;
    }

    .header-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #58a6ff;
        margin-bottom: 1rem;
    }

    .header-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 4rem;
        font-weight: 600;
        color: #ffffff; 
        line-height: 1.1;
        margin: 0;
    }

    .header-sub {
        font-size: 1.2rem;
        color: #c9d1d9; 
        margin-top: 1rem;
        font-weight: 400;
        letter-spacing: 0.04em;
    }

    .section-divider {
        border: none;
        border-top: 1px solid #30363d;
        margin: 2.5rem 0;
        width: 100%;
    }

    .input-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #c9d1d9; /* Mais claro */
        margin-bottom: 1rem;
        text-align: center;
        display: block;
    }

    .stTextInput > div > div > input {
        background-color: #161b22 !important;
        border: 2px solid #30363d !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 1.2rem !important;
        padding: 1.2rem 1.5rem !important;
        text-align: center !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #58a6ff !important;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15) !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #8b949e !important; 
    }

    .stButton > button {
        background-color: #161b22 !important;
        color: #58a6ff !important;
        border: 2px solid #30363d !important;
        border-radius: 8px !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        padding: 1rem 2rem !important;
        width: 60% !important;
        margin: 1.5rem auto 0 auto !important;
        display: block !important;
        white-space: nowrap !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: #1c2128 !important;
        border-color: #58a6ff !important;
        color: #79c0ff !important;
        transform: translateY(-2px);
    }

    .stButton > button:active {
        background-color: #0d1117 !important;
        transform: translateY(0);
    }

    .stSpinner > div {
        border-top-color: #58a6ff !important;
        margin: 2rem auto;
    }

    .result-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #3fb950;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        margin-top: 2rem;
    }

    .result-header::before {
        content: '';
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #3fb950;
        border-radius: 50%;
    }

    .result-box {
        background-color: #161b22;
        border: 1px solid #21262d;
        border-top: 4px solid #3fb950;
        border-radius: 8px;
        padding: 2rem;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #e6edf3;
        text-align: left;
    }

    .stAlert {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        font-family: 'IBM Plex Sans', sans-serif !important;
        font-size: 1.1rem !important;
        text-align: center;
    }

    .footer {
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid #30363d;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.1em;
        color: #8b949e; /* Mais claro também */
    }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { 
        padding-top: 22vh !important; 
        max-width: 900px !important; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-block">
    <div class="header-label">RAG · Audit Platform · v1.0</div>
    <div class="header-title">CyberAudit GPT</div>
    <div class="header-sub">Retrieval-augmented analysis against network inventory and security documentation</div>
</div>
<hr class="section-divider">
""", unsafe_allow_html=True)

st.markdown('<div class="input-label">System Query</div>', unsafe_allow_html=True)

query = st.text_input(
    label="query",
    label_visibility="collapsed",
    placeholder="e.g. Identify open ports and cross-reference with CVEs..."
)

run = st.button("Run Audit", use_container_width=True)

if run:
    if not query.strip():
        st.warning("Enter a query before running the audit.")
    else:
        with st.spinner("Querying workspace — cross-referencing inventory against knowledge base..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"message": query, "mode": "chat"}
            url = f"{ANYTHING_LLM_URL}/workspace/{WORKSPACE_SLUG}/chat"

            try:
                response = requests.post(url, json=payload, headers=headers)

                if response.status_code == 200:
                    text_response = response.json().get("textResponse", "No response returned.")

                    st.markdown('<div class="result-header">Analysis complete</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-box">{text_response}</div>', unsafe_allow_html=True)

                else:
                    st.error(f"Request failed — HTTP {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("Connection refused. Ensure AnythingLLM is running on localhost:3001.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

st.markdown("""
<div class="footer">
    <span>CyberAudit GPT</span>
    <span>AnythingLLM · Workspace: cyberaudit</span>
</div>
""", unsafe_allow_html=True)