import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

ANYTHING_LLM_URL = f"http://{os.getenv('DOCKER_HOST_IP', 'localhost')}:3001/api/v1"
WORKSPACE_SLUG = "cyberaudit"
API_KEY = os.getenv("API_KEY")

st.set_page_config(page_title="CyberAudit GPT", page_icon=None, layout="centered")

if "query_history" not in st.session_state:
    st.session_state.query_history = []

if "query" not in st.session_state:
    st.session_state.query = ""

if "output_text" not in st.session_state:
    st.session_state.output_text = ""

if "output_sources" not in st.session_state:
    st.session_state.output_sources = []

if "last_error" not in st.session_state:
    st.session_state.last_error = ""


def check_server_status():
    try:
        response = requests.get(f"http://{os.getenv('DOCKER_HOST_IP', 'localhost')}:3001/api/ping", timeout=2)
        return response.status_code == 200
    except requests.RequestException:
        return False

server_online = check_server_status()
server_indicator = "🟢 Engine: Online" if server_online else "🔴 Engine: Offline"
server_color = "#3fb950" if server_online else "#ff5f5f"

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
        color: #c9d1d9;
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

    .result-header + .stMarkdown > div {
        border: 1px solid #3fb950;
        background-color: #0f161f;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 0 0 1px rgba(63, 185, 80, 0.12);
        margin-top: 0.5rem;
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
        color: #8b949e;
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

st.markdown(
    f'<div style="display:flex; justify-content:flex-end; margin-bottom:1rem; color:{server_color}; font-family: IBM Plex Mono, monospace; letter-spacing: 0.08em;">{server_indicator}</div>',
    unsafe_allow_html=True,
)

with st.expander("VIEW SYSTEM ARCHITECTURE"):
    st.markdown("""
    ### System Architecture: Local RAG Pipeline

    ```text
    [ Auditor Query ] 
            │
            ▼
    [ Streamlit Frontend ] ──(REST API)──► [ AnythingLLM Local Server ]
                                                    │
                                ┌───────────────────┴───────────────────┐
                                ▼                                       ▼
                      [ Vector Database ]                       [ Local LLM ]
                     (Indexed PDFs & CSVs)                  (Inference Engine)
                                │                                       │
                                └───────────► Context Retrieval ────────┘
                                                    │
                                                    ▼
                                            [ Audit Analysis ]
    ```

    ### Component Breakdown:
    *   **Frontend (Streamlit):** Provides a secure, local web interface for the auditor to submit queries without relying on external cloud platforms.
    *   **API Layer:** Connects the frontend to the local AnythingLLM instance securely via environment variables (Secrets Management).
    *   **Orchestration (AnythingLLM):** Manages the Retrieval-Augmented Generation (RAG) pipeline, ensuring the LLM only accesses authorized local data.
    *   **Vector Database:** Stores mathematically embedded representations of the structured data (Network Inventory CSV) and unstructured theoretical data (Cybersecurity PDFs).
    *   **Local LLM Engine:** Processes the auditor's query alongside the retrieved context to generate fact-based, private cybersecurity insights, entirely on-premises.
    """, unsafe_allow_html=True)

st.markdown('<div class="input-label">System Query</div>', unsafe_allow_html=True)

query = st.text_input(
    label="query",
    label_visibility="collapsed",
    placeholder="e.g. Identify open ports and cross-reference with CVEs...",
    key="query"
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
                response = requests.post(url, json=payload, headers=headers, timeout=500)

                if response.status_code == 200:
                    text_response = response.json().get("textResponse", "No response returned.")
                    sources = response.json().get("sources", [])
                    st.session_state.output_text = text_response
                    st.session_state.output_sources = sources
                    st.session_state.last_error = ""
                elif response.status_code in [401, 403]:
                    st.error("Authentication Error: Check if your API_KEY in the .env file is correct.")
                    st.session_state.last_error = "Authentication Error"
                else:
                    st.error(f"Request failed — HTTP {response.status_code}: {response.text}")
                    st.session_state.last_error = f"HTTP {response.status_code}"

            except requests.exceptions.Timeout:
                st.error("The AI engine took too long to respond (Timeout > 500s).")
                st.session_state.last_error = "Timeout"
            except requests.exceptions.ConnectionError:
                st.error("Connection refused. Ensure AnythingLLM is running on localhost:3001.")
                st.session_state.last_error = "ConnectionError"
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                st.session_state.last_error = "Exception"

if st.session_state.output_text:
    st.markdown('<div class="result-header">Analysis complete</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-box">{st.session_state.output_text}</div>', unsafe_allow_html=True)
    export_content = f"CyberAudit GPT Report\n{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\nQUERY:\n{query}\n\nANALYSIS:\n{st.session_state.output_text}"

    st.download_button(
        label="Export Analysis",
        data=export_content,
        file_name=f"audit_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )

    if st.session_state.output_sources:
        st.markdown("**Sources consulted:**")
        for source in st.session_state.output_sources:
            title = source.get("title", source.get("id", str(source)))
            st.markdown(f"- `{title}`")

st.markdown("""
<div class="footer">
    <span>CyberAudit GPT</span>
    <span>AnythingLLM · Workspace: cyberaudit</span>
</div>
""", unsafe_allow_html=True)