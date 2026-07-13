import chromadb
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from ingestion.transformations import split_documents
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
from ingestion.load_docs import load_documents

load_dotenv()

def build_index(nodes:list[BaseNode])->VectorStoreIndex:
    """
    It creates an index of embedded nodes
    
    Args:
        nodes: A list of document chunks

    Return:
        index: An index object that can be used to find embedded nodes relevant to a query

    """
    #Create a chroma client and collection
    persist_directory='db/chroma_db'
    client=chromadb.PersistentClient(persist_directory)
    collection=client.get_or_create_collection(name="rag_collection")

    #Create an instance of the ChromaVectorStore: vector_store
    print("Create Vector Store")
    vector_store=ChromaVectorStore(collection)

    print("Create Storage Context")
    storage_context=StorageContext.from_defaults(vector_store=vector_store)

    print("Create embedding models")
    embedding_model=OpenAIEmbedding(model="text-embedding-3-small")

    if collection.count()==0:
        print(f"embedding {len(nodes)} nodes-API call happens here")
        index=VectorStoreIndex(
            nodes=nodes,
            embed_model=embedding_model,
            storage_context=storage_context 
        )
    else:
        print("Collection already created.")
        index=VectorStoreIndex.from_vector_store(
            vector_store,
            embed_model=embedding_model,
        )

    print("Finished builing index")

    return index



def main():
    load_docs=load_documents()
    nodes=split_documents(load_docs)
    index=build_index(nodes)
    print(f"{index} this is the index")

if __name__ =="__main__":
    main()

