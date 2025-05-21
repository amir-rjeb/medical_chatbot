import os
import streamlit as st
import requests
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from typing import List, Dict
from dataclasses import dataclass
from langchain.tools import tool  # Add this import

# Configuration
FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), '../faiss_index')
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL = "llama3"
OLLAMA_HOST = "http://localhost:11434"
TEMP = 0.2

st.set_page_config(page_title="Medical Chatbot", layout="wide")
st.title("🩺 Medical Chatbot")

@dataclass
class PubMedArticle:
    title: str
    pub_date: str
    doi: str = ""
    authors: List[str] = None
    abstract: str = ""

# Outil PubMed personnalisé
@tool
def search_pubmed_tool(query: str, max_results: int = 3) -> str:
    """Recherche des articles médicaux sur PubMed. Retourne les titres, dates et DOI."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    
    search_response = requests.get(base_url, params=search_params)
    search_response.raise_for_status()
    search_data = search_response.json()
    
    if not search_data.get("esearchresult", {}).get("idlist"):
        return "Aucun article trouvé sur PubMed."
    
    ids = search_data["esearchresult"]["idlist"]
    
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ",".join(ids),
        "retmode": "xml"
    }
    
    fetch_response = requests.get(fetch_url, params=fetch_params)
    fetch_response.raise_for_status()
    
    articles = []
    content = fetch_response.text
    articles_xml = content.split("<PubmedArticle>")[1:]
    
    for article_xml in articles_xml:
        try:
            title_start = article_xml.find("<ArticleTitle>") + len("<ArticleTitle>")
            title_end = article_xml.find("</ArticleTitle>", title_start)
            title = article_xml[title_start:title_end].strip()
            
            pub_date_start = article_xml.find("<PubDate>") + len("<PubDate>")
            pub_date_end = article_xml.find("</PubDate>", pub_date_start)
            pub_date = article_xml[pub_date_start:pub_date_end].strip()
            
            doi = ""
            if "<ArticleId IdType=\"doi\">" in article_xml:
                doi_start = article_xml.find("<ArticleId IdType=\"doi\">") + len("<ArticleId IdType=\"doi\">")
                doi_end = article_xml.find("</ArticleId>", doi_start)
                doi = article_xml[doi_start:doi_end].strip()
            
            articles.append(f"- {title} ({pub_date}) DOI: {doi}")
        except Exception:
            continue
    
    return "\n".join(articles) if articles else "Aucun article trouvé sur PubMed."

# Load vector store
@st.cache_resource
def load_store():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBED_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": False}
    )
    store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    return embeddings, store

embeddings, vector_store = load_store()

# VectorstoreTool
def faiss_search_tool(query: str) -> str:
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)
    return "\n\n".join([doc.page_content for doc in docs])

# Prompt template
prompt_template = """
Use the following context from medical documents to answer the question.
If the context contains specific information, present it clearly.
If the answer is not found in the context, state that explicitly.

Context:
{context}

Question:
{question}

Answer:
"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Tools setup
vectorstore_tool = Tool(
    name="VectorstoreTool",
    func=faiss_search_tool,
    description="Searches the local FAISS medical document database for relevant information."
)

pubmed_tool = Tool(
    name="PubMedTool",
    func=search_pubmed_tool,
    description="Accesses public medical articles from PubMed."
)

tools = [vectorstore_tool, pubmed_tool]

# LLM initialization
llm = OllamaLLM(model=OLLAMA_MODEL, base_url=OLLAMA_HOST, temperature=TEMP)

# Agent initialization
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# Interface utilisateur
query = st.text_input("Enter your medical question:")

if st.button("Get Answer") and query:
    with st.spinner("The agent is thinking..."):
        try:
            # Recherche dans la base locale
            retriever = vector_store.as_retriever(search_kwargs={"k": 5})
            qa = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=retriever,
                return_source_documents=True,
                chain_type_kwargs={"prompt": PROMPT},
            )
            res = qa.invoke({"query": query})
            
            # Affichage des résultats
            st.subheader("Answer:")
            st.markdown(res["result"])
            
            # Sources locales
            with st.expander("Local Sources"):
                for i, doc in enumerate(res["source_documents"], 1):
                    fn = doc.metadata.get("source", "Unknown source")
                    st.markdown(f"**{i}. {fn}**")
                    st.caption(doc.page_content[:200] + "...")
            
            # Si réponse insuffisante, proposer PubMed
            if "not found" in res["result"].lower() or len(res["result"].strip()) < 10:
                st.info("No precise answer found in local database. Searching PubMed...")
                pubmed_results = search_pubmed_tool(query)
                st.markdown(pubmed_results)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Trying alternative approach with agent...")
            try:
                response = agent.run(query)
                st.markdown(response)
            except Exception as agent_error:
                st.error(f"Agent error: {str(agent_error)}")