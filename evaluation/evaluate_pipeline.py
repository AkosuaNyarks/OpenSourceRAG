import json
from pathlib import Path
from textwrap import indent

from llama_index.core.query_engine import RetrieverQueryEngine
from ingestion.load_docs import load_documents
from ingestion.transformations import split_documents
from indexing.build_index import build_index
from retrieval.retriever import  get_retriever
from llm.llm_factory import get_llm
from retrieval.query_engine import get_query_engine

GOLDEN_SET_PATH="evaluation/ground_truth.json"
OUTPUT="evaluation/evaluate_dataset.json"

def build_pipeline():
    load_docs=load_documents()
    nodes=split_documents(load_docs)
    index=build_index(nodes)
    retriever = get_retriever(index)
    llm = get_llm()
    query_engine=get_query_engine(retriever,llm)
    return query_engine



def run_eval_set(query_engine:RetrieverQueryEngine,golden_set:list[dict],output_path:str)->list[dict]:
    records=[]
    with open(output_path,"w") as f:
        for item in golden_set:
            response=query_engine.query(item["question"])
            contexts=[]
            for node in response.source_nodes:
                contexts.append(node.get_content())

            record={
                "id": item["id"],
                "question": item["question"],
                "answer": str(response),
                "contexts": contexts,
                "ground_truth": item["ground_truth"],
                "type": item.get("type"),
                "source_document": item.get("source_document"),
            }
            records.append(record)
            f.write(json.dumps(record, indent=2)+ "\n")

            print(f"[{item['id']}] done — retrieved {len(contexts)} chunks")

    return records
       
def main():
    golden_set=json.loads(Path(GOLDEN_SET_PATH).read_text())
    query_engine=build_pipeline()
    records=run_eval_set(query_engine,golden_set,output_path=OUTPUT)
    print(f"\n Saved {len(records)} to {OUTPUT}")


if __name__ =="__main__":
    main()