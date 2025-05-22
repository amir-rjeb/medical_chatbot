import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pickle


# Configuration
PDF_DIR = os.path.join(os.path.dirname(__file__), '../data/pdfs')
FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), '../faiss_index')
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Initialize embedding model
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL_NAME,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": False}
)

# Load and process PDFs
all_docs = []
for filename in os.listdir(PDF_DIR):
    if filename.lower().endswith('.pdf'):
        path = os.path.join(PDF_DIR, filename)
        loader = PyPDFLoader(path)
        docs = loader.load()
        for doc in docs:
            doc.metadata["source_file"] = filename
        all_docs.extend(docs)
        print(f"Loaded {len(docs)} pages from {filename}")

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(all_docs)
print(f"Split into {len(chunks)} chunks.")

#  FAISS
vectorstore = FAISS.from_documents(chunks, embeddings)

# Save 
vectorstore.save_local(FAISS_INDEX_PATH)
print("Ingestion complete.")