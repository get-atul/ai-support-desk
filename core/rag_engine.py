import os

from langchain_openai import ChatOpenAI


def get_llm():
    return ChatOpenAI(
        model="gpt-5-nano",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3,
    )