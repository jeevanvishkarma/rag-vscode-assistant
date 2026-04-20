import sys,os ,json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from retrieval.retriever import retrieve as get_docs
from retrieval.reranker import rerank
from generation.generate_answer import generate_answer
from evaluation.generation_judge_llm import judge_answer

import json

if __name__ == "__main__":

    with open("data\\llm_generated_queries.json", "r", encoding="utf-8") as f:
        query_data = json.load(f)

    final_output = []

    # ---- Aggregation ----
    total = 0
    relevance_sum = 0
    faithfulness_sum = 0
    completeness_sum = 0

    for query in query_data[:]:
        
        docs = get_docs(query, k=10)
        docs = rerank(query, docs, top_k=5)
        print("\n-----------------------\n")
        print('query')
        print(query)
        print("context")
        for doc in docs:
            print(doc.page_content)
        answer = generate_answer(query, docs,max_tokens=600)
        print("generated answer")
        print(answer)

        llm_score = judge_answer(query, docs, answer)
        print("llm_score")
        print(llm_score)
        print("\n-----------------------\n")

        # ---- Update sums ----
        relevance_sum += llm_score.get("relevance", 0)
        faithfulness_sum += llm_score.get("faithfulness", 0)
        completeness_sum += llm_score.get("completeness", 0)
        total += 1

        final_output.append({
            "query": query,
            "context": [d.page_content for d in docs],  # fix (docs not JSON serializable)
            "answer": answer,
            "score": llm_score
        })

    # ---- Compute averages ----
    avg_scores = {
        "avg_relevance": round(relevance_sum / total, 3),
        "avg_faithfulness": round(faithfulness_sum / total, 3),
        "avg_completeness": round(completeness_sum / total, 3)
    }

    print("\n=== Generation Metrics ===")
    print(avg_scores)

    # ---- Save detailed ----
    with open("data\\generation_judgement_output.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4)

    # ---- Save summary ----
    with open("data\\generation_summary.json", "w", encoding="utf-8") as f:
        json.dump(avg_scores, f, indent=4)