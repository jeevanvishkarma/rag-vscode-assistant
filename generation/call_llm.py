from turtle import st

from openai import OpenAI
import dotenv
import os
dotenv.load_dotenv()
import streamlit as st
def get_secret(key):
    value = os.getenv(key)
    if not value:
        st.error(f"Error: {key} not found in environment variables.")
        st.stop()
    return value

client = OpenAI(api_key=get_secret("gpt_api_key"))

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