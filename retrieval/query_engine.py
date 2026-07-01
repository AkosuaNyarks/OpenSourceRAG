from llama_index.core.query_engine import RetrieverQueryEngine

def get_query_engine(retriever,llm):
    query_engine = RetrieverQueryEngine.from_args(
        llm=llm,
        retriever=retriever
    )
    return query_engine