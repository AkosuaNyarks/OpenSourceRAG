**OpenSourceRAG**

An evaluation-focused Retrieval-Augmented Generation (RAG) system for asking grounded questions about PDF documents.

OpenSourceRAG turns PDFs into searchable chunks, retrieves the most relevant context for a question, and uses a language model to generate an answer constrained to the uploaded documents. The project also includes an evaluation workflow for measuring context recall and faithfulness, making it useful for studying not only how to build a RAG pipeline, but also where retrieval can fail.

**Why I Built This**

I built this project to understand the complete RAG pipeline and investigate how engineering decisions—including PDF parsing, chunking, embeddings, retrieval depth, and prompt design—affect the quality of generated answers.

Rather than treating RAG as a black box, the repository separates ingestion, indexing, retrieval, generation, and evaluation into individual modules. This makes it easier to test each stage independently and identify whether an incorrect answer was caused by retrieval or generation.



**Features**

Upload and ask questions about a PDF through a Streamlit interface

Parse PDFs with PyMuPDF through LlamaIndex

Split documents into sentence-aware chunks with configurable size and overlap

Generate vector embeddings with OpenAI's text-embedding-3-small

Store and persist vectors locally with ChromaDB

Detect changed documents with SHA-256 hashes to avoid unnecessary re-embedding

Retrieve the top-k most relevant chunks for each question

Generate document-grounded responses with a strict fallback when the context is insufficient

Evaluate the pipeline with RAGAS faithfulness and context-recall metrics

Prepare and index an Open RAG Benchmark subset for broader evaluation





**How It Works**

Ingestion: PyMuPDFReader extracts text and metadata from each PDF.

Chunking: SentenceSplitter divides the extracted text into 512-token chunks with a 100-token overlap by default.

Indexing: Each chunk is embedded and stored in a persistent ChromaDB collection.

Change detection: File-level SHA-256 hashes identify new or modified documents so unchanged files do not need to be embedded again.

Retrieval: The system retrieves the eight most similar chunks by default.

Generation: The retrieved chunks and the user's question are passed to a grounded prompt. If the context does not support an answer, the model is instructed to say so instead of guessing.

Evaluation: RAGAS compares generated answers, retrieved contexts, and reference answers to measure faithfulness and context recall.


 
  
  **Tech Stack**

Application UI       Streamlit

RAG orchestration    LlamaIndex

PDF parsing          PyMuPDF

Chunking             LlamaIndex SentenceSplitter

Embeddings.          OpenAI text-embedding-3-small

Vector database.     ChromaDB

Generation.          OpenAI gpt-4o-mini by default

Evaluation.          RAGAS and Open RAG Benchmark data

**Note:**
The pipeline is assembled with open-source RAG infrastructure, but the current implementation uses OpenAI models for embeddings, answer generation, and evaluation. An OpenAI API key is therefore required.




**Getting Started**

**Prerequisites**

Python 3.10 or later

An OpenAI API key

**1. Clone the repository**

    git clone https://github.com/AkosuaNyarks/OpenSourceRAG.git
    cd OpenSourceRAG

**2. Create and activate a virtual environment**

macOS or Linux:

    python3 -m venv .venv
    source .venv/bin/activate

Windows PowerShell:

    python -m venv .venv
    .venv\Scripts\Activate.ps1

**3. Install the dependencies**

    pip install streamlit chromadb pymupdf python-dotenv \
    llama-index llama-index-readers-file llama-index-vector-stores-chroma \
    llama-index-embeddings-openai llama-index-llms-openai \
    ragas langchain-openai pandas

**4. Configure the environment**

Create a .env file in the project root:

    OPENAI_API_KEY=your_openai_api_key
    OPENAI_MODEL=gpt-4o-mini

OPENAI_MODEL is optional; the application uses gpt-4o-mini by default.




**Run the Streamlit App**

    streamlit run app.py

Then:

1. Upload a PDF.

2. Select Index this document.

3. Wait for the document to be parsed, chunked, embedded, and indexed.

4. Ask a question about its contents.

Each upload session receives its own ChromaDB collection and hash store under db/.


**Design Decisions**

**Sentence-aware overlapping chunks**

The default 512-token chunk size balances semantic completeness with retrieval precision. A 100-token overlap reduces the chance that useful context is lost at chunk boundaries.

**Persistent vector storage**

ChromaDB persists embeddings between runs, avoiding the need to rebuild the full index every time the application starts.

**Hash-based incremental indexing**

The system computes a SHA-256 hash for each source file. Only files whose content has changed are selected for embedding, reducing duplicate work and API usage.

**Grounded generation**

The question-answering prompt directs the model to rely only on retrieved context, preserve exact names and numbers, and return a fixed insufficient-context response when the evidence does not support an answer.




**Current Limitations**
1. The Streamlit interface accepts one PDF per indexing session.

2. Retrieval currently uses dense vector similarity without sparse retrieval or reranking.

3. The application does not yet display citations or retrieved source passages in the UI.

4. Scanned or image-only PDFs require OCR, which is not currently part of the ingestion pipeline.

5. Uploaded files and per-session vector collections are not automatically cleaned up.

6. Dependency versions are not yet pinned in a requirements file.
   



**Future Improvements**

1. Add hybrid retrieval using dense vectors and BM25

2. Add a cross-encoder reranker after initial retrieval

3. Compare chunk sizes, overlap values, embedding models, and top-k settings systematically

4. Add OCR support for scanned PDFs

5. Display page-level citations and retrieved evidence with each answer

6. Support multi-document collections and conversational history

7. Replace hosted models with fully local embedding and generation options

8. Expand benchmark coverage and report reproducible experiment results

9. Add automated tests and continuous integration

