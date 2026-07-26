import os
from langchain_openai import ChatOpenAI
from ragas.llms import LangchainLLMWrapper

def get_judge_llm():
    chat_model = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    return LangchainLLMWrapper(chat_model)
