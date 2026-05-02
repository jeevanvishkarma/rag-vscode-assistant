import os,json,sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts.load_prompt import  prompt_loader

with open("data\\retrieval__reranked_judgement_output.json", "r", encoding="utf-8") as f:
    retrieval_judgement_output = json.load(f)
print(retrieval_judgement_output[:2] )

import json
import json

detailed_results = []

total_queries = len(retrieval_judgement_output)

precision_sum = 0
recall_sum = 0
mrr_sum = 0
avg_relevant_docs = 0

for issue in retrieval_judgement_output:
    query = issue["query"]
    relevance = issue["llm_relevance"]  # [1,0,1]
    k = len(relevance)

    # -------- Precision --------
    precision = sum(relevance) / k
    precision_sum += precision

    # -------- Recall --------
    recall = 1 if sum(relevance) > 0 else 0
    recall_sum += recall

    # -------- MRR --------
    rr = 0
    for idx, val in enumerate(relevance):
        if val == 1:
            rr = 1 / (idx + 1)
            break
    mrr_sum += rr

    # -------- Avg relevant docs --------
    avg_relevant_docs += sum(relevance)

    # -------- Store per-query result --------
    detailed_results.append({
        "query": query,
        "llm_relevance": relevance,
        "precision": round(precision, 3),
        "recall": recall,
        "mrr": round(rr, 3)
    })


# -------- Aggregate metrics --------
avg_precision = precision_sum / total_queries
avg_recall = recall_sum / total_queries
mrr = mrr_sum / total_queries
avg_relevant = avg_relevant_docs / total_queries


# -------- Save summary --------
summary = {
    "precision_at_k": round(avg_precision, 3),
    "recall_at_k": round(avg_recall, 3),
    "mrr": round(mrr, 3),
    "avg_relevant_docs": round(avg_relevant, 3)
}

with open("evaluation/reranked_results.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)


# -------- Save detailed --------
with open("evaluation/reranked_detailed_results.json", "w", encoding="utf-8") as f:
    json.dump(detailed_results, f, indent=2)


print("✅ Summary + detailed results saved!")