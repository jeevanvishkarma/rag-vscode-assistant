import streamlit as st
from scripts.run_rag import run_rag

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="VS Code issues RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# -------------------------------
# Styling (optional but nice)
# -------------------------------
st.markdown("""
<style>
.stChatMessage {
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.title("🤖 RAG Assistant")
st.caption("Ask questions about your dataset")

# -------------------------------
# Session State (Chat History)
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.write("Retrieval: Top 10 → Rerank Top 3")
    st.write("Model: GPT-4o-mini")
    st.markdown("---")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------
# Display Chat History
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# User Input
# -------------------------------
query = st.chat_input("Ask your question...")

if query:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.markdown(query)

    # -------------------------------
    # RAG Pipeline
    # -------------------------------
    with st.spinner("Thinking..."):
        answer, docs = run_rag(
            query,
            history=st.session_state.messages
        )

    # -------------------------------
    # Show Assistant Response
    # -------------------------------
    with st.chat_message("assistant"):
        st.markdown(answer)

        # Context viewer (very useful)
        with st.expander("📄 Retrieved Context"):
            for i, d in enumerate(docs):
                st.markdown(f"**Doc {i+1}:** {d.page_content[:300]}")

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
