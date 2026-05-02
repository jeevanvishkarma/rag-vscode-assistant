import os,json,sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts.load_prompt import  prompt_loader
from generation.call_llm import call_llm


retrieval_llm_prompt = prompt_loader("retrieval_judge_prompt.txt")

with open("data\\retrieval_results_reranked.json", "r", encoding="utf-8") as f:
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

with open("data\\retrieval__reranked_judgement_output.json", "w", encoding="utf-8") as f:
    json.dump(retrieval_llm_judgement_output, f, indent=4)