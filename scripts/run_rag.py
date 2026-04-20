import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.retriever import retrieve as get_docs
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer

def run_rag(query, history=None):
    # Step 1: Retrieve (history-aware)
    docs = get_docs(query, k=10, history=history)

    # Step 2: Rerank
    docs = rerank(query, docs, top_k=3)

    # Step 3: Generate answer (history-aware)
    answer = generate_answer(query, docs, history=history)

    return answer, docs
    
if __name__ == "__main__":
    query = "What are the new features in Python 3.12?"
    answer , docs = run_rag(query)
    print("Final Answer:", answer)