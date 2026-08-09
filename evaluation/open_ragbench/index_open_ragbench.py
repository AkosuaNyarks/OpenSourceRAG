from ingestion.load_docs import load_documents
from ingestion.transformations import split_documents
from indexing.build_index import build_index

def main():
    documents = load_documents(input_dir="data/open_ragbench/pdf")
    nodes = split_documents(documents)

    index = build_index(
        documents,
        nodes,
        persist_directory="db/chroma_db_open_ragbench",
        collection_name="open_ragbench_collection",
        hash_store_path="db/doc_hashes_open_ragbench.json",
    )

    print(index)

if __name__ == "__main__":
    main()