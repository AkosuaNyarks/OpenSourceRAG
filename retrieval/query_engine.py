from llama_index.core.query_engine import RetrieverQueryEngine
from llm.prompts import qa_template

def get_query_engine(retriever,llm):
    query_engine = RetrieverQueryEngine.from_args(
        llm=llm,
        retriever=retriever,
        text_qa_template=qa_template
    )
    return query_engine