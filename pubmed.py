# pubmed.py
from typing import List
import requests
from dataclasses import dataclass
from langchain.tools import Tool
from langchain.agents import tool

# Remplacer les imports obsolètes
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun, YouTubeSearchTool
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_community.utilities import GoogleSearchAPIWrapper
@dataclass
class Article:
    title: str
    pub_date: str
    abstract: str = ""
    doi: str = ""
    authors: List[str] = None

# Outil PubMed personnalisé
@tool
def search_pubmed(query: str, max_results: int = 3) -> str:
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
            # Extraction du titre
            title_start = article_xml.find("<ArticleTitle>") + len("<ArticleTitle>")
            title_end = article_xml.find("</ArticleTitle>", title_start)
            title = article_xml[title_start:title_end].strip()
            
            # Extraction de la date de publication
            pub_date_start = article_xml.find("<PubDate>") + len("<PubDate>")
            pub_date_end = article_xml.find("</PubDate>", pub_date_start)
            pub_date = article_xml[pub_date_start:pub_date_end].strip()
            
            # Extraction du DOI
            doi = ""
            if "<ArticleId IdType=\"doi\">" in article_xml:
                doi_start = article_xml.find("<ArticleId IdType=\"doi\">") + len("<ArticleId IdType=\"doi\">")
                doi_end = article_xml.find("</ArticleId>", doi_start)
                doi = article_xml[doi_start:doi_end].strip()
            
            articles.append(f"- {title} ({pub_date}) DOI: {doi}")
        except Exception as e:
            continue
    
    return "\n".join(articles) if articles else "Aucun article trouvé sur PubMed."


def get_tools():
    """Retourne tous les outils configurés"""
    
    # Outil Wikipedia
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    
    # Outil Arxiv (pour les prépublications scientifiques)
    arxiv = ArxivAPIWrapper()
    
    # Outil de recherche Google (nécessite une API key)
    # google_search = GoogleSearchAPIWrapper()
    
    # Outil DuckDuckGo
    duckduckgo = DuckDuckGoSearchRun()
    
    # Outil YouTube
    youtube = YouTubeSearchTool()
    
    # Création des outils LangChain
    tools = [
        Tool(
            name="PubMedTool",
            func=search_pubmed,
            description="Recherche d'articles médicaux sur PubMed. Input: requête de recherche."
        ),
        Tool(
            name="WikipediaTool",
            func=wikipedia.run,
            description="Recherche d'informations générales sur Wikipedia. Input: requête de recherche."
        ),
        Tool(
            name="DuckDuckGoSearch",
            func=duckduckgo.run,
            description="Recherche sur Internet. Input: requête de recherche."
        ),
        Tool(
            name="YouTubeSearch",
            func=youtube.run,
            description="Recherche de vidéos éducatives sur YouTube. Input: requête de recherche."
        )
    ]
    
    return tools

# Pour tester les outils
if __name__ == "__main__":
    print("=== Test PubMedTool ===")
    print(search_pubmed("COVID-19 treatment"))
    
    print("\n=== Test WikipediaTool ===")
    wikipedia_tool = get_tools()[1]
    print(wikipedia_tool.run("Hypothyroidism"))