import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts.load_prompt import  prompt_loader
from generation.call_llm import call_llm
import json


def load_prompt(path="generation_judge.txt"):
    return prompt_loader(path)


def build_context(docs, max_chars=300):
    """
    Convert retrieved docs into a clean context string
    """
    return "\n\n".join([doc['text'] for doc in docs])


def judge_answer(query, docs, answer):
    generation_judge_prompt = load_prompt('generation_judge.txt')

    context = build_context(docs)
    # print(generation_judge_prompt)
    prompt = generation_judge_prompt.replace(
        "{query}",
        query
    ).replace(
        "{context}",
        context
    ).replace(
        "{answer}",
        answer
    )

    response = call_llm(prompt)

    try:
        return json.loads(response)
    except:
        return {
            "relevance": 0,
            "faithfulness": 0,
            "completeness": 0
        }