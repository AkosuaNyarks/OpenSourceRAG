
from llama_index.core import VectorStoreIndex
from llama_index.core.base.base_retriever import BaseRetriever


def get_retriever(index:VectorStoreIndex)->BaseRetriever:
    retriever = index.as_retriever()
    return retriever