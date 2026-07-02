
from llama_index.core import PromptTemplate


qa_template=PromptTemplate("""You are a question-answering assistant. Answer ONLY using the context 
information provided below. Do not use any knowledge you learned during 
training.
If the answer cannot be found in the context, respond exactly with: 
"I don't have enough information in the provided documents to answer that."


-----------------
{context_str}
-------------------
Question : {query_str}
Answer:
"""
)