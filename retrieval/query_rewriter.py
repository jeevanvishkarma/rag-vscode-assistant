from generation.call_llm import call_llm

def rewrite_query(query, history=None):
    if not history:
        return query

    recent = history[-2:]

    history_text = "\n".join(
        [f"{m['role']}: {m['content']}" for m in recent]
    )

    prompt = f"""
Rewrite the user query into a clear standalone search query.

Use history ONLY if needed to resolve references like "it", "this".

Ignore irrelevant history.

Conversation:
{history_text}

User query:
{query}

Rewritten query:
"""

    return call_llm(prompt).strip()