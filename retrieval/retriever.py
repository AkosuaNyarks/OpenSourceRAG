
from llama_index.core import VectorStoreIndex
from llama_index.core.base.base_retriever import BaseRetriever


def get_retriever(index:VectorStoreIndex,top_k:int=8)->BaseRetriever:
    retriever = index.as_retriever(similarity_top_k=top_k)
    return retriever