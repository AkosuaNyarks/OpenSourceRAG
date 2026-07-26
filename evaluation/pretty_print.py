import json


def pretty_print(path: str):
    with open(path, "r") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            record=json.loads(line)
            print(f"\n{'='*80}")
            print(f"[{record['id']}] {record['question']}")
            print(f"{'='*80}")
            print(f"\n Answer: \n {record['answer']}")
            print(f"\nGround truth:\n  {record['ground_truth']}")
            print(f"\nContexts ({len(record['contexts'])}):")
            for i, context in enumerate(record["contexts"], start=1):
                print(f"\n ---chunk {i} ---")
                print(f" {context}")
if __name__ == "__main__":
    pretty_print("evaluation/evaluate_dataset.json")

