import os,json,sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts.load_prompt import  prompt_loader
from generation.call_llm import call_llm
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


retrieval_llm_prompt = prompt_loader("retrieval_judge_prompt.txt")
retrieval_result = os.path.join(
                BASE_DIR,
                "data",
                "retrieval_results_reranked_all.json"
            )
with open(retrieval_result, "r", encoding="utf-8") as f:
    retrieval_results = json.load(f)

retrieval_llm_judgement_output = []
for query in retrieval_results[:]:
    llm_out ={"query": query["query"], "results": query["results"], 'llm_relevance': []}
    PROMPT = retrieval_llm_prompt.replace("{query}", query["query"]).replace("{doc1}", query["results"][0]).replace("{doc2}", query["results"][1]).replace("{doc3}", query["results"][2])
    out = call_llm(PROMPT, max_tokens=10)
    output_list = eval(out)
    llm_out['llm_relevance'] = output_list
    retrieval_llm_judgement_output.append(llm_out)
    print(f"Output: {output_list}")
retrieval_llm_judgement = os.path.join(
                BASE_DIR,
                "data",
                "retrieval__reranked_judgement_output_all.json"
            )
with open(retrieval_llm_judgement, "w", encoding="utf-8") as f:
    json.dump(retrieval_llm_judgement_output, f, indent=4)