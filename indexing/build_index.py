import chromadb
import hashlib
import json
from pathlib import Path
from llama_index.core import Document
from llama_index.core.schema import BaseNode
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.openai import OpenAIEmbedding
from ingestion.transformations import split_documents
from llama_index.core import VectorStoreIndex
from dotenv import load_dotenv
from ingestion.load_docs import load_documents

HASH_STORE_PATH = "db/doc_hashes.json"

load_dotenv()


def get_document_hash(document: Document)->str:
    content=document.get_content()
    return hashlib.sha256(content.encode()).hexdigest()

def load_hash_store(path:str = HASH_STORE_PATH)-> dict:
    if not Path(path).exists():
        return {}
    return json.loads(Path(path).read_text())

def save_hash_store(hashes:dict, path:str=HASH_STORE_PATH)-> None:
    Path(path).write_text(json.dumps(hashes, indent=2))

def connect_to_index(persist_directory: str, collection_name: str) -> VectorStoreIndex:
    client = chromadb.PersistentClient(persist_directory)
    collection = client.get_or_create_collection(collection_name)
    vector_store = ChromaVectorStore(collection)
    embedding_model = OpenAIEmbedding(model="text-embedding-3-small")
    return VectorStoreIndex.from_vector_store(vector_store, embed_model=embedding_model)

def get_file_hash(documents_for_file: list[Document]) -> str:
    combined_content = ""
    for doc in documents_for_file:
        combined_content += doc.get_content()
    return hashlib.sha256(combined_content.encode()).hexdigest()


def detect_changed_documents(documents: list[Document], hash_store_path:str = HASH_STORE_PATH):
    stored_hashes=load_hash_store(hash_store_path)

    file_groups={}
    for doc in documents:
        filename=doc.metadata['file_name']
        if filename not in file_groups:
            file_groups[filename]=[]
        file_groups[filename].append(doc)   

    current_hashes={}
    changed_filenames=[]
    for filename,docs_for_file in file_groups.items():
        file_hash=get_file_hash(docs_for_file)
        current_hashes[filename] = file_hash

        if stored_hashes.get(filename) != file_hash:
            changed_filenames.append(filename)

    return changed_filenames, current_hashes



def build_index(
    documents: list[Document],
    nodes:list[BaseNode],
    persist_directory:str='db/chroma_db',
    collection_name:str="rag_collection",
    hash_store_path: str = HASH_STORE_PATH
    )->VectorStoreIndex:
    """
    It creates an index of embedded nodes
    
    Args:
        nodes: A list of document chunks

    Return:
        index: An index object that can be used to find embedded nodes relevant to a query

    """
    #Create a chroma client and collection
    client=chromadb.PersistentClient(persist_directory)
    collection=client.get_or_create_collection(collection_name)

    #Create an instance of the ChromaVectorStore: vector_store
    print("Create Vector Store")
    vector_store=ChromaVectorStore(collection)

    print("Create Storage Context")
    storage_context=StorageContext.from_defaults(vector_store=vector_store)

    print("Create embedding models")
    embedding_model=OpenAIEmbedding(model="text-embedding-3-small")

    changed_filenames, current_hashes = detect_changed_documents(documents, hash_store_path)
    if changed_filenames:
        nodes_to_embed = []
        for n in nodes:
            if n.metadata["file_name"] in changed_filenames:
                nodes_to_embed.append(n)

        print(f"embedding {len(nodes_to_embed)} nodes from {len(changed_filenames)} changed document(s)")
        index = VectorStoreIndex(
            nodes=nodes_to_embed,
            embed_model=embedding_model,
            storage_context=storage_context
        )
        save_hash_store(current_hashes, hash_store_path)
    else:
        print("No new or changed documents.")
        index = connect_to_index(persist_directory, collection_name)
    return index


def main():
    load_docs=load_documents()
    nodes=split_documents(load_docs)
    index=build_index(load_docs,nodes)
    print(f"{index} this is the index")

if __name__ =="__main__":
    main()

