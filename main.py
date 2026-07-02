from ingestion.load_docs import load_documents
from ingestion.transformations import split_documents
from indexing.build_index import build_index
from retrieval.retriever import  get_retriever
from llm.llm_factory import get_llm
from retrieval.query_engine import get_query_engine
def main():
    # 1. Load the documents
    load_docs=load_documents()

    #2.Split the documents into nodes
    nodes=split_documents(load_docs)

    #3. Build an index for the nodes and store in ChromaDB
    index=build_index(nodes)

    #4. Create a retriever to retrieve the data  that...
    retriever=get_retriever(index)

    #5. Setup the LLM model
    llm=get_llm()

    #6.send the retriver and the llm to the query engine
    query_engine=get_query_engine(retriever,llm)

    #Ask a question
    question = "When was Apple founded, and by whom?"


    response=query_engine.query(question)
    print (response)




if __name__ =="__main__":
    main()