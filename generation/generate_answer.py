from generation.call_llm import call_llm
from prompts.load_prompt import  prompt_loader
from generation.call_llm import call_llm


generation_llm_prompt = prompt_loader("answer_generation.txt")

def load_prompt(path="prompts/generation.txt"):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_context(docs, max_chars=300):
    """
    Convert retrieved docs into a clean context string
    """
    return "\n\n".join([doc.page_content for doc in docs])


# def generate_answer(query, docs,max_tokens=200):
#     """
#     Main function:
#     - loads prompt
#     - builds context
#     - fills template
#     - calls LLM
#     """
#     # template = generation_llm_prompt

#     context = build_context(docs)

#     prompt = generation_llm_prompt.format(
#         context=context,
#         query=query
#     )

#     answer = call_llm(  prompt, max_tokens=max_tokens)

#     return answer.strip()

def format_history(messages, max_turns=3):
    """
    Convert chat history into readable text for the prompt
    """
    if not messages:
        return ""

    # take last N messages
    history = messages[-max_turns:]

    formatted = ""
    for m in history:
        role = "User" if m["role"] == "user" else "Assistant"
        formatted += f"{role}: {m['content']}\n"

    return formatted.strip()

def generate_answer(query, docs, history=None,max_tokens=200):
    # template = load_prompt()

    context = build_context(docs)

    history_text = ""
    if history:
        history_text = format_history(history)

    prompt = generation_llm_prompt.format(
        context=context,
        query=query,
        history=history_text
    )

    return call_llm(prompt, max_tokens=max_tokens)