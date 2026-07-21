from ingestion.load_docs import load_documents
from ingestion.transformations import split_documents
from indexing.build_index import build_index
from retrieval.retriever import  get_retriever
from llm.llm_factory import get_llm
from retrieval.query_engine import get_query_engine
def main()-> None:
    # Load the documents
    load_docs=load_documents()

    #Split the documents into nodes
    nodes=split_documents(load_docs)

    #Build an index for the nodes and store in ChromaDB
    index=build_index(nodes)

  
    query_engine=get_query_engine(get_retriever(index),get_llm())

    #Ask a question
    question = "What was Nvidia's net income in fiscal year 2020 vs 2026?"


    response=query_engine.query(question)
    print (response)




if __name__ =="__main__":
    main()