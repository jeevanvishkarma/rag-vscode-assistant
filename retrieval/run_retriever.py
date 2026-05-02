import json
import sys,os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.retriever import retrieve as retrieve
from retrieval.reranker import rerank as rerank

if __name__ == "__main__":
    query_data = json.load(open("data\\llm_generated_queries.json", "r", encoding="utf-8"))

    retrieval_output = []

    for query in query_data:
        print(f"\n🔍 Query: {query}")

        query_result = {"query": query, "results": []}

        # Step 1: Retrieve top 10
        docs = retrieve(query, k=10)

        # Step 2: Rerank → keep top 3
        docs = rerank(query, docs, top_k=3)

        for i, doc in enumerate(docs):
            print(f"\nResult {i+1}")
            query_result["results"].append(doc.page_content)

        retrieval_output.append(query_result)

    with open("data\\retrieval_results_reranked.json", "w", encoding="utf-8") as f:
        json.dump(retrieval_output, f, indent=4)