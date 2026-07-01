import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from ingestion.transformations import split_documents
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
from ingestion.load_docs import load_documents

load_dotenv()

def build_index(nodes):

    #Create a chroma client and collection
    persist_directory='db/chroma_db'
    client=chromadb.PersistentClient(persist_directory)
    collection=client.get_or_create_collection(name="rag_collection")

    #Create the chromaVectorStore
    print("Create Vector Store")
    vector_store=ChromaVectorStore(collection)

    #
    print("Create Storage Context")
    storage_context=StorageContext.from_defaults(vector_store=vector_store)

    print("Create embedding models")
    embedding_model=OpenAIEmbedding(model="text-embedding-3-small")

    index=VectorStoreIndex(
        nodes=nodes,
        embed_model=embedding_model,
        storage_context=storage_context,
        
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

