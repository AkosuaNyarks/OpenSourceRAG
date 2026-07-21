import json
from pathlib import Path
from ragas import EvaluationDataset
from ragas.dataset_schema import SingleTurnSample


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