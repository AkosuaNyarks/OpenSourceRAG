import streamlit as st
import shutil
import uuid
from pathlib import Path

from ingestion.load_docs import load_documents
from ingestion.transformations import split_documents
from indexing.build_index import build_index
from retrieval.query_engine import build_query_engine_for_collection

st.set_page_config(page_title="OpenSourceRAG", page_icon="📄")
st.title("📄 Ask your documents")

if "collection_name" not in st.session_state:
    st.session_state.collection_name = None
    st.session_state.query_engine = None

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file and st.button("Index this document"):
    session_id = str(uuid.uuid4())[:8]
    upload_dir = Path(f"data/uploads/{session_id}")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / uploaded_file.name
    file_path.write_bytes(uploaded_file.getvalue())

    with st.spinner("Indexing document..."):
        documents = load_documents(input_dir=str(upload_dir))
        nodes = split_documents(documents)

        collection_name = f"session_{session_id}"
        persist_directory = f"db/chroma_db_{session_id}"
        hash_store_path = f"db/doc_hashes_{session_id}.json"

        build_index(
            documents,
            nodes,
            persist_directory=persist_directory,
            collection_name=collection_name,
            hash_store_path=hash_store_path,
        )

        st.session_state.collection_name = collection_name
        st.session_state.query_engine = build_query_engine_for_collection(
            persist_directory, collection_name
        )

    st.success(f"Indexed '{uploaded_file.name}' — ready for questions.")

if st.session_state.query_engine:
    question = st.text_input("Ask a question about your document")
    if question:
        with st.spinner("Thinking..."):
            response = st.session_state.query_engine.query(question)
        st.write(str(response))