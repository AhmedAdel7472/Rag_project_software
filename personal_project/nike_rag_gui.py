"""
Nike AI Product Agent — Streamlit GUI
======================================
Drop-in UI for the RAG agent notebook.

Run with:
    streamlit run nike_agent_app.py

Requirements (same as notebook + streamlit):
    pip install streamlit langchain langchain-core langchain-openai \
                langchain-community langchain-chroma chromadb pymupdf \
                python-dotenv langchain-huggingface sentence-transformers
"""

import os
import re
import tempfile

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# ─────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nike AI Agent",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Custom CSS — clean dark-sport aesthetic
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* Root palette */
    :root {
        --bg:        #0d0d0d;
        --surface:   #161616;
        --border:    #2a2a2a;
        --accent:    #ff5a00;
        --accent2:   #ff8c42;
        --text:      #f0ede8;
        --muted:     #7a7570;
        --tool-bg:   #1a1200;
        --tool-border:#ff5a0040;
        --user-bg:   #0f1e2e;
        --user-border:#1e4d7b;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
        color: var(--text) !important;
        font-family: 'DM Sans', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border);
    }
    [data-testid="stSidebar"] * { color: var(--text) !important; }

    /* Header strip */
    .agent-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 20px 0 8px 0;
        border-bottom: 2px solid var(--accent);
        margin-bottom: 28px;
    }
    .agent-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.4rem;
        letter-spacing: 3px;
        color: var(--text);
        line-height: 1;
    }
    .agent-sub {
        font-size: 0.78rem;
        color: var(--muted);
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* Status pill */
    .status-pill {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    .status-ready   { background:#0f3a1a; color:#4cde7a; border:1px solid #1d6b33; }
    .status-missing { background:#3a0f0f; color:#de4c4c; border:1px solid #6b1d1d; }
    .status-loading { background:#2a1f00; color:#f0a030; border:1px solid #6b4a00; }

    /* Chat bubbles */
    .msg-user {
        background: var(--user-bg);
        border: 1px solid var(--user-border);
        border-radius: 12px 12px 4px 12px;
        padding: 14px 18px;
        margin: 8px 0 8px 60px;
        font-size: 0.93rem;
        line-height: 1.6;
    }
    .msg-assistant {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px 12px 12px 4px;
        padding: 14px 18px;
        margin: 8px 60px 8px 0;
        font-size: 0.93rem;
        line-height: 1.6;
    }
    .msg-tool {
        background: var(--tool-bg);
        border: 1px solid var(--tool-border);
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 80px 6px 60px;
        font-size: 0.78rem;
        font-family: 'Courier New', monospace;
        color: #ff8c42;
    }
    .tool-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--accent);
        margin-bottom: 4px;
        font-weight: 600;
    }
    .msg-role {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .role-user      { color: #5b9de6; }
    .role-assistant { color: var(--accent); }

    /* Chat input area */
    [data-testid="stChatInput"] textarea {
        background: var(--surface) !important;
        border: 1px solid var(--border) !important;
        color: var(--text) !important;
        border-radius: 10px !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px #ff5a0030 !important;
    }

    /* Buttons */
    .stButton > button {
        background: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
        transition: background 0.2s;
    }
    .stButton > button:hover {
        background: var(--accent2) !important;
    }

    /* Sliders, selects */
    [data-testid="stSlider"] .st-ae { color: var(--accent) !important; }
    div[data-baseweb="select"] > div { 
        background: var(--surface) !important; 
        border-color: var(--border) !important; 
        color: var(--text) !important;
    }

    /* Section labels in sidebar */
    .sidebar-section {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: var(--accent);
        font-weight: 700;
        margin: 20px 0 8px 0;
        padding-bottom: 4px;
        border-bottom: 1px solid var(--border);
    }

    /* Empty state */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: var(--muted);
    }
    .empty-state h3 {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.6rem;
        letter-spacing: 3px;
        color: var(--border);
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Session state initialisation
# ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []       # list of dicts: role / content / tool_calls
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "embeddings" not in st.session_state:
    st.session_state.embeddings = None
if "db_path" not in st.session_state:
    st.session_state.db_path = "./nike_chroma_db"


# ─────────────────────────────────────────────────────────────
# Sidebar — configuration
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        "<div style='font-family:Bebas Neue,sans-serif; font-size:1.5rem;"
        " letter-spacing:3px; color:#ff5a00;'>⚙ Configuration</div>",
        unsafe_allow_html=True,
    )

    # ── LLM settings ──
    st.markdown("<div class='sidebar-section'>LLM — LM Studio</div>", unsafe_allow_html=True)
    lm_base_url = st.text_input("Base URL", value="http://localhost:1234/v1")
    lm_api_key  = st.text_input("API Key",  value="lm-studio", type="password")
    lm_model    = st.text_input("Model name", value="qwen3-4b")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.05)

    # ── Embedding settings ──
    st.markdown("<div class='sidebar-section'>Embeddings</div>", unsafe_allow_html=True)
    embed_model = st.selectbox(
        "HuggingFace model",
        [
            "sentence-transformers/all-MiniLM-L6-v2",
            "sentence-transformers/all-mpnet-base-v2",
            "sentence-transformers/paraphrase-MiniLM-L6-v2",
        ],
    )

    # ── Chunking settings ──
    st.markdown("<div class='sidebar-section'>Chunking</div>", unsafe_allow_html=True)
    chunk_size    = st.slider("Chunk size",    100, 2000, 300, 50)
    chunk_overlap = st.slider("Chunk overlap",  0,  500,  50, 10)
    top_k         = st.slider("Top-K results",  1,   10,   3,  1)

    # ── Vector DB ──
    st.markdown("<div class='sidebar-section'>Vector Store</div>", unsafe_allow_html=True)
    db_path = st.text_input("ChromaDB path", value="./nike_chroma_db")
    st.session_state.db_path = db_path

    # ── PDF upload & build ──
    st.markdown("<div class='sidebar-section'>Catalog PDF</div>", unsafe_allow_html=True)
    uploaded_pdf = st.file_uploader("Upload PDF catalog", type=["pdf"])

    col1, col2 = st.columns(2)
    build_clicked = col1.button("🔨 Build DB", use_container_width=True)
    load_clicked  = col2.button("📂 Load DB",  use_container_width=True)

    # DB status
    if st.session_state.retriever is not None:
        st.markdown(
            "<span class='status-pill status-ready'>● Vector DB Ready</span>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<span class='status-pill status-missing'>○ No Vector DB</span>",
            unsafe_allow_html=True,
        )

    st.divider()
    if st.button("🗑 Clear chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()


# ─────────────────────────────────────────────────────────────
# Helper — get / cache embeddings model
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading embedding model…")
def get_embeddings(model_name: str):
    return HuggingFaceEmbeddings(model_name=model_name)


# ─────────────────────────────────────────────────────────────
# Build vector store from uploaded PDF
# ─────────────────────────────────────────────────────────────
if build_clicked:
    if uploaded_pdf is None:
        st.sidebar.error("Upload a PDF catalog first.")
    else:
        with st.sidebar:
            with st.spinner("Building vector store…"):
                # Save upload to a temp file (PyMuPDFLoader needs a real path)
                suffix = ".pdf"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_pdf.read())
                    tmp_path = tmp.name

                embeddings = get_embeddings(embed_model)
                st.session_state.embeddings = embeddings

                loader = PyMuPDFLoader(tmp_path)
                docs   = loader.load()

                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    separators=["\n\n", "\n", " "],
                )
                chunks = splitter.split_documents(docs)

                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embeddings,
                    persist_directory=db_path,
                )
                st.session_state.vectorstore = vectorstore
                st.session_state.retriever   = vectorstore.as_retriever(
                    search_kwargs={"k": top_k}
                )
                os.unlink(tmp_path)
            st.success(f"✅ Indexed {len(chunks)} chunks from {uploaded_pdf.name}")


# ─────────────────────────────────────────────────────────────
# Load existing vector store from disk
# ─────────────────────────────────────────────────────────────
if load_clicked:
    if not os.path.exists(db_path):
        st.sidebar.error(f"No ChromaDB found at `{db_path}`.")
    else:
        with st.sidebar:
            with st.spinner("Loading vector store…"):
                embeddings = get_embeddings(embed_model)
                st.session_state.embeddings = embeddings

                vectorstore = Chroma(
                    persist_directory=db_path,
                    embedding_function=embeddings,
                )
                st.session_state.vectorstore = vectorstore
                st.session_state.retriever   = vectorstore.as_retriever(
                    search_kwargs={"k": top_k}
                )
            st.success(f"✅ Loaded existing DB from `{db_path}`")


# ─────────────────────────────────────────────────────────────
# Main area — header
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="agent-header">
        <div>
            <div class="agent-title">👟 Nike AI Agent</div>
            <div class="agent-sub">RAG-Powered Football Catalog Assistant</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Chat history display
# ─────────────────────────────────────────────────────────────
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.markdown(
            """
            <div class="empty-state">
                <h3>Just Do It</h3>
                <p>Build or load a vector store, then ask anything about the Nike catalog.<br>
                Try: <em>"Show me Arsenal kits under £60"</em> or <em>"What boots do you have?"</em></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for msg in st.session_state.chat_history:
            role = msg["role"]

            if role == "user":
                st.markdown(
                    f"<div class='msg-user'>"
                    f"  <div class='msg-role role-user'>You</div>"
                    f"  {msg['content']}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

            elif role == "assistant":
                # Show tool calls if any
                for tc in msg.get("tool_calls", []):
                    args_str = ", ".join(f"{k}={repr(v)}" for k, v in tc["args"].items())
                    st.markdown(
                        f"<div class='msg-tool'>"
                        f"  <div class='tool-label'>🔧 Tool call → {tc['name']}</div>"
                        f"  {args_str}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                if msg["content"]:
                    st.markdown(
                        f"<div class='msg-assistant'>"
                        f"  <div class='msg-role role-assistant'>Agent</div>"
                        f"  {msg['content']}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

            elif role == "tool_result":
                with st.expander(f"📄 Tool result — {msg.get('tool_name', 'result')}", expanded=False):
                    st.text(msg["content"][:1500] + ("…" if len(msg["content"]) > 1500 else ""))


# ─────────────────────────────────────────────────────────────
# Agent runner
# ─────────────────────────────────────────────────────────────
def run_agent(question: str):
    """Run the agentic loop and stream results into session state."""
    retriever = st.session_state.retriever

    # ── Define tools (must be inside function so retriever is captured) ──
    @tool
    def nike_search(query: str) -> str:
        """Search the Nike product catalog. Use for questions about shirts,
        boots, shorts, club kits, prices, or availability."""
        docs = retriever.invoke(query)
        return "\n\n".join(d.page_content for d in docs)

    @tool
    def filter_by_price(query: str, max_price: float) -> str:
        """Search Nike products and return only those under a given price in GBP."""
        docs    = retriever.invoke(query)
        results = []
        for d in docs:
            text   = d.page_content
            prices = re.findall(r"£([\d.]+)", text)
            if prices and all(float(p) <= max_price for p in prices):
                results.append(text)
        return "\n\n".join(results) if results else "No products found under that price."

    tools       = [nike_search, filter_by_price]
    tools_dict  = {t.name: t for t in tools}

    llm = ChatOpenAI(
        base_url=lm_base_url,
        api_key=lm_api_key,
        model=lm_model,
        temperature=temperature,
    )
    llm_with_tools = llm.bind_tools(tools)

    messages = [
        SystemMessage(content=(
            "You are a Nike UK football product assistant. "
            "Use the nike_search tool to find products. "
            "Use filter_by_price when the user mentions a budget. "
            "Always mention the price in GBP in your final answer."
        )),
        HumanMessage(content=question),
    ]

    for _ in range(10):
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        tool_calls_info = []
        if response.tool_calls:
            for tc in response.tool_calls:
                tool_calls_info.append({"name": tc["name"], "args": tc["args"]})

        # Record assistant turn (may have tool calls but no text yet)
        st.session_state.chat_history.append(
            {
                "role": "assistant",
                "content": response.content or "",
                "tool_calls": tool_calls_info,
            }
        )

        if not response.tool_calls:
            break   # final answer reached

        # Execute tools
        for tc in response.tool_calls:
            result = tools_dict[tc["name"]].invoke(tc["args"])
            messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
            st.session_state.chat_history.append(
                {
                    "role": "tool_result",
                    "tool_name": tc["name"],
                    "content": str(result),
                }
            )


# ─────────────────────────────────────────────────────────────
# Chat input
# ─────────────────────────────────────────────────────────────
user_input = st.chat_input(
    "Ask about the Nike catalog… e.g. 'Do you have Barcelona kits under £50?'"
)

if user_input:
    if st.session_state.retriever is None:
        st.warning("⚠️ Please build or load the vector store first (sidebar → Build DB / Load DB).")
    else:
        # Record user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        with st.spinner("Agent is thinking…"):
            try:
                run_agent(user_input)
            except Exception as e:
                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": f"❌ Error: {e}",
                        "tool_calls": [],
                    }
                )
        st.rerun()