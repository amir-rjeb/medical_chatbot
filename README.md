

---

````markdown
# 🩺 Medical Chatbot using LLM, RAG & Agents

This project is a **medical chatbot**, using modern AI techniques such as:

- **LLM** (Large Language Model)
- **RAG** (Retrieval-Augmented Generation)
- **LangChain Agents**
- **FAISS vector store**

The chatbot can answer medical questions by retrieving information from **locally embedded medical documents**. If no relevant answer is found locally, it can optionally consult **PubMed** (can be disabled).

---

## 🚀 Features

- 💬 Natural language interaction with a medical chatbot
- 🧠 Local knowledge base powered by **FAISS** & **HuggingFace embeddings**
- 🔍 Optional integration with **PubMed** for external article lookup
- 🤖 Powered by **Ollama LLM** (local LLM runtime)
- 🖥️ Simple web interface built with **Streamlit**
- 🎨 Custom background and design with HTML & CSS

---

## 🛠️ Tech Stack

- **Python 3.11+**
- **Streamlit** for UI
- **LangChain** for chaining and agent logic
- **FAISS** for vector storage
- **Ollama** for local LLM inference (supports models like `llama3`)
- **HuggingFace Transformers** for embeddings
- **HTML & CSS** for custom interface design

---

## 📦 Requirements

Make sure you install the following Python libraries (with version numbers tested):

```bash
pip install streamlit==1.32.2
pip install langchain==0.1.16
pip install langchain-community==0.0.36
pip install langchain-ollama==0.0.6
pip install langchain-huggingface==0.0.5
pip install faiss-cpu==1.7.4
pip install requests==2.31.0
````

You also need to install **Ollama**:

* Install from [https://ollama.com](https://ollama.com)
* Run it locally with your model (e.g., `llama3`):

  ```bash
  ollama run llama3
  ```

---

## 📁 Project Structure

```bash
medical_chatbot/
├── scripts/
│   ├── app.py                # Main Streamlit app
│   └── ingest.py             # Script d'indexation des PDF
├── pubmed.py                 # Outils externes (PubMed, Wikipedia, etc.)
├── faiss_index/              # Local vectorstore (généré par ingest.py)
├── data/
│   └── pdfs/                 # Tes fichiers PDF médicaux
├── static/
│   ├── index.html            # Custom HTML interface (optionnel)
│   └── style.css             # Custom styles (optionnel)
├── requirements.txt          # Dépendances Python du projet
├── .gitignore                # Fichiers à ignorer par git
├── README.md                 # Documentation du projet
```

---

## ✅ How to Run

1. Start **Ollama** in a terminal:

   ```bash
   ollama run llama3
   ```

2. Start the chatbot UI:

   ```bash
   streamlit run scripts/app.py
   ```

3. Open your browser at:

   ```
   http://localhost:8501
   ```

---

## 👨‍⚕️ Example Questions

* What are the recommended treatments for type 2 diabetes?
* What are the common symptoms of high blood pressure?
* How is asthma diagnosed in adults?



## 📬 Contact

For any questions, feel free to reach out via GitHub or linkedin.

*account linkedin: https://www.linkedin.com/in/rjeb-amir-0866bb250/



