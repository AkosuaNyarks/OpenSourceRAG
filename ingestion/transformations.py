
from llama_index.core.node_parser import SentenceSplitter
from ingestion.load_docs import load_documents


def split_documents(documents,chunk_size=512,chunk_overlap=100):

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

# c