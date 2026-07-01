from llama_index.llms.openai import OpenAI

def get_llm():
    model="gpt-3.5-turbo"
    return OpenAI(model=model)

llm=get_llm()
