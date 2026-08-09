from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.llms import LLM
from llama_index.core.query_engine import RetrieverQueryEngine
from indexing.build_index import connect_to_index
from llm.llm_factory import get_llm
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

def build_query_engine_for_collection(
    persist_directory: str,
    collection_name: str,
    top_k: int = 8,
) -> RetrieverQueryEngine:
    """
    Build a query engine for any existing, already-embedded collection.

    Args:
        persist_directory: Path to the Chroma persistence directory.
        collection_name: Name of the Chroma collection to connect to.
        top_k: Number of chunks to retrieve per query.

    Return:
        A ready-to-use query engine for that collection.
    """
    index = connect_to_index(persist_directory, collection_name)
    retriever = index.as_retriever(similarity_top_k=top_k)
    llm = get_llm()
    return get_query_engine(retriever, llm)