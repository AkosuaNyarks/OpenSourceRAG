
def get_retriever(index):
    retriever = index.as_retriever()
    return retriever