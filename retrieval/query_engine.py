

synthesizer = get_response_synthesizer(response_mode="compact")
query_engine = RAGQueryEngine(
    retriever=retriever, response_synthesizer=synthesizer
)