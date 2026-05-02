import json,os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import json
from retrieval.query_rewriter import rewrite_query



# same embedding model (IMPORTANT!)
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# load vectorstore
vectorstore = FAISS.load_local(
    r"faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# create retriever
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def build_query_with_history(query, history, max_turns=2):
    """
    Combine last few turns with current query to make retrieval context-aware.
    """
    if not history:
        return query

    # take last N turns
    recent = history[-max_turns:]
    parts = []
    for m in recent:
        parts.append(m["content"])

    # final query
    return " ".join(parts) + " " + query


def retrieve(query, k=10, history=None):
    # 👉 rewrite query using history
    query_for_retrieval = rewrite_query(query, history)

    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k, "lambda_mult": 0.7}
    )

    return retriever.invoke(query_for_retrieval)

    