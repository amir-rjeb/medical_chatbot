Here is the **English version** of your project description, along with a list of required `pip` packages and instructions to run the Ollama interface:

---

### 🧠 **Project Description – Medical AI Chatbot**

This project is an **intelligent medical chatbot** built using **open-source NLP models** and a **local document knowledge base** indexed with FAISS.

#### 🔍 How it Works:

* At its core, the system uses a **local large language model (LLM)** served through **Ollama** (`llama3`), eliminating dependency on cloud-based services such as OpenAI.
* It leverages a **vector database (FAISS)** populated with embedded medical documents (e.g., PDFs) to support semantic search and Retrieval-Augmented Generation (RAG).
* Embeddings are generated using `all-MiniLM-L6-v2` from Hugging Face.
* When a user submits a medical question:

  1. Relevant content is retrieved from the vector store using FAISS.
  2. A structured prompt is created with that context.
  3. The local LLM generates an accurate and context-aware medical answer.

#### ✅ Goals:

* Provide **reliable, context-based medical answers** using trusted sources without relying on internet or PubMed.
* Ensure **data privacy** by keeping all processes fully local.
* Support **medical inquiry automation** for use cases such as patient education, clinical reference, or decision support.

---

### 📦 Required Python Packages

Before running the project, install the following dependencies using pip:

```
pip numpy==1.26.4
 pip pillow==10.4.0
 pip packaging==23.2
pip markupsafe==2.1.5
pip langchain
pip langchain-community
pip langchain-huggingface
pip faiss-cpu
pip sentence-transformers
streamlit
pip langchain-ollama
ollama
```

> ⚠️ Make sure your Python environment (e.g. virtualenv or conda) is activated.

---

### 🛠️ Running the Ollama Model

1. **Install Ollama** from the official website:
   [https://ollama.com](https://ollama.com)

2. **Start the Ollama service** (from terminal or command prompt):

   ```
   ollama serve
   ```

3. **Download the LLM (e.g., llama3):**

   ```
   ollama run llama3
   ```

> Once running, the model will be accessible via `http://localhost:11434`.

---

Would you like me to prepare a `requirements.txt` file or a `README.md` to include with the project?
