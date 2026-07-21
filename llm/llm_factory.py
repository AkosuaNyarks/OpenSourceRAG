import os
from typing import Optional
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import LLM

def get_llm(model:Optional[str]=None,api_key:Optional[str]= None) -> LLM:
    """
    Get access to LLM

        Args:
            model=Name of the OpenAI model to use
            api_key = OPEN AI API Key

        Return:
            A large language model instance
    """
    if model is None:
        model=os.environ.get("OPENAI_MODEL","gpt-4o-mini")
    if api_key is None:
        api_key=os.environ.get("OPENAI_API_KEY")
    return OpenAI(model=model,api_key=api_key)
