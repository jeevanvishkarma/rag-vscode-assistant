import streamlit as st
from scripts.run_rag import run_rag
from dotenv import load_dotenv
import os
import warnings

# =====================================
# ENV
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

load_dotenv(
    os.path.join(BASE_DIR, ".env")
)

warnings.filterwarnings("ignore")

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="VS Code Issues RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# CUSTOM CSS
# =====================================
st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .stChatMessage {
        padding: 14px;
        border-radius: 14px;
        margin-bottom: 12px;
    }

    .metric-box {
        background-color: #111827;
        padding: 12px;
        border-radius: 12px;
        text-align: center;
    }

    .suggestion-box {
        background-color: #1f2937;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 10px;
    }

    .small-text {
        font-size: 13px;
        color: #9ca3af;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# TITLE
# =====================================
st.title("🤖 VS Code Issues RAG Assistant")

st.caption(
    "Hybrid Retrieval + Cross-Encoder Reranking over GitHub VS Code Issues"
)

# =====================================
# SESSION STATE
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# SIDEBAR
# =====================================
with st.sidebar:

    st.header("⚙️ System Info")

    st.markdown("""
    ### Retrieval Pipeline

    1. Dense FAISS Retrieval (Top 100)
    2. BM25 Lexical Rerank (Top 20)
    3. Cross-Encoder Rerank (Top 5)
    4. GPT-4o-mini Answer Generation
    """)

    st.markdown("---")

    st.subheader("💡 Suggested Questions")

    suggested_queries = [

        "VS Code Python interpreter not detected after update",

        "Explorer not showing files after opening workspace",

        "Copilot is really slow in VS Code",

        "VS Code crashes on macOS when opening terminal",

        "Python environment keeps changing",

        "Why is Pylance not indexing properly?",

        "Terminal freezes after latest VS Code update"
    ]

    for q in suggested_queries:

        st.markdown(
            f"""
            <div class="suggestion-box">
            {q}
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("📊 Dataset")

    st.write("• ~250K GitHub Issues")

    st.write("• ~800K Semantic Chunks")

    st.write("• Hybrid Retrieval")

    st.write("• FAISS IVF Index")

    st.write("• BM25 Lexical Search")

    st.markdown("---")

    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================
# CHAT HISTORY
# =====================================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =====================================
# CHAT INPUT
# =====================================
query = st.chat_input(
    "Ask a VS Code issue question..."
)

# =====================================
# MAIN QUERY FLOW
# =====================================
if query:

    # =================================
    # SAVE USER MESSAGE
    # =================================
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):

        st.markdown(query)

    # =================================
    # RUN RAG
    # =================================
    with st.spinner(
        "Running hybrid retrieval + reranking..."
    ):

        answer, docs, timings = run_rag(
            query,
            history=st.session_state.messages
        )

    # =================================
    # ASSISTANT RESPONSE
    # =================================
    with st.chat_message("assistant"):

        st.markdown(answer)

        # =================================
        # LATENCY METRICS
        # =================================
        st.markdown("## ⚡ Pipeline Latency")

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric(
            "Dense",
            f"{timings['dense_retrieval']}s"
        )

        col2.metric(
            "BM25",
            f"{timings['bm25']}s"
        )

        col3.metric(
            "Rerank",
            f"{timings['rerank']}s"
        )

        col4.metric(
            "Generation",
            f"{timings['generation']}s"
        )

        col5.metric(
            "Total",
            f"{timings['total']}s"
        )

        st.markdown("---")

        # =================================
        # RETRIEVED CONTEXT
        # =================================
        with st.expander(
            "📄 Retrieved Context"
        ):

            for i, d in enumerate(docs):

                st.markdown(
                    f"## Document {i+1}"
                )

                # -------------------------
                # TITLE
                # -------------------------
                if d.get("title"):

                    st.markdown(
                        f"### {d['title']}"
                    )

                # -------------------------
                # TEXT
                # -------------------------
                st.code(
                    d["text"][:1200],
                    language="markdown"
                )

                # -------------------------
                # METADATA
                # -------------------------
                st.markdown(
                    f"""
                    <div class="small-text">

                    Ticket ID: {d.get('ticket_id')}

                    Timestamp: {d.get('timestamp')}

                    Chunk Index: {d.get('chunk_index', 0)}

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("---")

    # =================================
    # SAVE ASSISTANT RESPONSE
    # =================================
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })