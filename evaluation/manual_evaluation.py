from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
import json
# same embedding model (IMPORTANT!)
embeddings = SentenceTransformerEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# load vectorstore
vectorstore = FAISS.load_local(
    r"C:\Users\jeeva\OneDrive\Desktop\Rag_Chatbot\vs_code_issues_rag\faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

# create retriever
# retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "lambda_mult": 0.7}
)

# test query
query = "VS Code explorer not showing files"


queries = [
    "explorer not showing files",
    "terminal not opening",
    "copilot error",
]
# for query in queries:
#     print(f"\n🔍 Query: {query}")
#     docs = retriever.invoke(query)
#     for i, doc in enumerate(docs):
#         print(f"\nResult {i+1}")
#         print(doc.page_content[:300])

evaluation_data = [
    {
        "query": "explorer not showing files",
        "expected_ticket_id": [311218 ,311208 ]
    },
    {
        "query": "copilot rate limit error",
        "expected_ticket_id": [253124 ]
    }
]

def evaluate(retriever, eval_data, k=3):
    print(eval_data)
    total = len(eval_data)
    hits = 0
    precision_sum = 0

    for item in eval_data:
        query = item["query"]
        expected_ids = set(item["expected_ticket_id"])

        docs = retriever.invoke(query)

        retrieved_ids = [doc.metadata["ticket_id"] for doc in docs]

        # ---- Recall@k (hit rate) ----
        hit = any(rid in expected_ids for rid in retrieved_ids)
        if hit:
            hits += 1

        # ---- Precision@k ----
        correct_count = sum(1 for rid in retrieved_ids if rid in expected_ids)
        precision = correct_count / k
        precision_sum += precision

        print(f"\nQuery: {query}")
        print(f"Expected: {expected_ids}")
        print(f"Retrieved: {retrieved_ids}")
        print(f"Hit: {hit}, Precision@{k}: {precision:.2f}")

    recall_at_k = hits / total
    avg_precision = precision_sum / total

    print("\n==== Summary ====")
    print(f"Recall@{k}: {recall_at_k:.2f}")
    print(f"Avg Precision@{k}: {avg_precision:.2f}")

    return recall_at_k, avg_precision
with open("evaluation_data.json", "r", encoding="utf-8") as f:
    evaluation_data = json.load(f)
evaluate(retriever, evaluation_data, k=3)