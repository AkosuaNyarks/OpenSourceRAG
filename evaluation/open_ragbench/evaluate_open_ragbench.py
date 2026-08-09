import json
from pathlib import Path
from evaluation.open_ragbench.prepare_open_ragbench import OUTPUT_PATH
from llm.llm_factory import get_llm
from retrieval.query_engine import get_query_engine
from indexing.build_index import connect_to_index

PERSIST_DIRECTORY = "db/chroma_db_open_ragbench"
COLLECTION_NAME = "open_ragbench_collection"
QUESTIONS_PATH ="data/open_ragbench/subset_questions.json"
OUTPUT_PATH = "data/open_ragbench/eval_dataset.json"


def build_query_engine():
    index = connect_to_index(PERSIST_DIRECTORY, COLLECTION_NAME)
    retriever = index.as_retriever(similarity_top_k=8)
    llm = get_llm()
    query_engine = get_query_engine(retriever, llm)
    return query_engine


def run_eval_set(query_engine, questions, output_path):
    records = []
    with open(output_path, "w") as f:
        for i, item in enumerate(questions, 1):
            response = query_engine.query(item["question"])
            contexts = []
            for node in response.source_nodes:
                contexts.append(node.get_content())

            record = {
                "id": f"q{i}",
                "question": item["question"],
                "answer": str(response),
                "contexts": contexts,
                "ground_truth": item["answer"],
                "doc_id": item["doc_id"],
            }
            records.append(record)
            f.write(json.dumps(record) + "\n")
            print(f"[{record['id']}] done — retrieved {len(contexts)} chunks")

    return records
def main():
    query_engine = build_query_engine()

    questions = json.loads(Path(QUESTIONS_PATH).read_text())
    records = run_eval_set(query_engine, questions, OUTPUT_PATH)

    print(f"\nSaved {len(records)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()