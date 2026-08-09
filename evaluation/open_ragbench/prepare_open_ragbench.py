import json

META_DIR = 'data/open_ragbench/meta'
OUTPUT_PATH = 'data/open_ragbench/subset_questions.json'
NUM_DOCUMENTS = 5


def main():
    pdf_urls = json.loads(open(f'{META_DIR}/pdf_urls.json').read())
    queries = json.loads(open(f'{META_DIR}/queries.json').read())
    qrels = json.loads(open(f'{META_DIR}/qrels.json').read())
    answers = json.loads(open(f'{META_DIR}/answers.json').read())

    doc_ids = sorted({info['doc_id'] for info in qrels.values()})
    selected_docs = doc_ids[:NUM_DOCUMENTS]

    subset = []
    for query_id, info in qrels.items():
        if info['doc_id'] in selected_docs:
            subset.append({
                "question": queries[query_id]["query"],
                "answer": answers[query_id],
                "doc_id": info["doc_id"],
            })

    print(f"Found {len(subset)} questions across {len(selected_docs)} documents")
    print()
    print("Selected PDF URLs:")
    for doc_id in selected_docs:
        print(f"  {doc_id}: {pdf_urls[doc_id]}")

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(subset, f, indent=2)

    print(f"\nSaved {len(subset)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()