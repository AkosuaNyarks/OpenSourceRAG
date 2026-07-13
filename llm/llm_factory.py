from llama_index.llms.openai import OpenAI
from llama_index.core.llms import LLM

def get_llm(model:str="gpt-3.5-turbo") -> LLM:
    """
    Get access to LLM

        Args:
            model=Name of the OpenAI model to use

        Return:
            A large language model instance
    """

    return OpenAI(model=model)

llm=get_llm()
