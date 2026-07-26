from dotenv import load_dotenv
import json
import pandas
from pathlib import Path
from ragas import EvaluationDataset,evaluate
from ragas.dataset_schema import SingleTurnSample
from ragas.metrics import Faithfulness,ContextRecall
from evaluation.llm_judge import get_judge_llm


load_dotenv()
def load_ragas_dataset(path:str)->EvaluationDataset:
    samples = []
    with open (path,"r") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            r=json.loads(line)
            samples.append(
                SingleTurnSample(
                    user_input=r["question"],
                    response=r["answer"],
                    retrieved_contexts=r["contexts"],
                    reference=r["ground_truth"],
            )
        )

    return EvaluationDataset(samples=samples)

def main():
    dataset = load_ragas_dataset("evaluation/evaluate_dataset.json")
    judge_llm = get_judge_llm()

    results = evaluate(
        dataset=dataset,
        metrics=[Faithfulness(), ContextRecall()],
        llm=judge_llm,
    )

    print(results)
    df = results.to_pandas()
    print(df[["user_input", "faithfulness", "context_recall"]].to_string())


if __name__ == "__main__":
    main()