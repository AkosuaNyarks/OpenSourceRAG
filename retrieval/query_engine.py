from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.llms import LLM
from llama_index.core.query_engine import RetrieverQueryEngine
from llm.prompts import qa_template

def get_query_engine(retriever:BaseRetriever,llm:LLM)->RetrieverQueryEngine:
    """
    Args:
      retriever: A retriver Object
      llm: An instance of an LLM
       text_qa_template: A Prompt template
    

    Return:


    """
    query_engine = RetrieverQueryEngine.from_args(
        llm=llm,
        retriever=retriever,
        text_qa_template=qa_template
    )
    return query_engine