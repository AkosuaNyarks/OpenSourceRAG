
from typing import Sequence
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode
from ingestion.load_docs import load_documents

def split_documents(documents:Sequence[Document],chunk_size:int=512,chunk_overlap:int=100)->list[BaseNode]:
    """
    Spilt documents into Nodes

    Args:
        documents= a list of documents that were loaded by the load_docs function
        chunk_size:the maximum piece of text measured in tokens
        chunk_overlap: the amount of text that is repeated in each chunk

    Return: 
        A  List of Base Nodes

    """

    #Create an instance of SentenceSplitter, this stores the chunk
    sentence_splitter= SentenceSplitter(
        chunk_size= chunk_size,# 350-400 words
        chunk_overlap= chunk_overlap
    )
    nodes=sentence_splitter.get_nodes_from_documents(documents)
    return nodes


documents=load_documents()
nodes=split_documents(documents,chunk_size=512,chunk_overlap=100)
# print(len(nodes))
# print(nodes[0].text)
# print(nodes[0].metadata)
#print(len(documents))

