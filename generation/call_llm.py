from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()

client = OpenAI(api_key=os.getenv("gpt_api_key"))

def call_llm(prompt,max_tokens = 50):
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # cheap + good
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens
    )

    return response.choices[0].message.content

# a = call_llm("What is RAG?")
# print(a)