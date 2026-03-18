from duckduckgo_search import DDGS
from utils.logger import log_info, log_error

def search_web(query: str, max_results: int = 3) -> str:
    log_info(f"Recherche web en cours : {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return "Aucun résultat trouvé sur le web."
            
        summary = f"Résultats de la recherche pour '{query}':\n"
        for i, res in enumerate(results):
            summary += f"\n--- Résultat {i+1} ---\n"
            summary += f"Titre: {res.get('title', 'N/A')}\n"
            summary += f"Lien: {res.get('href', 'N/A')}\n"
            summary += f"Résumé: {res.get('body', 'N/A')}\n"
            
        return summary
    except Exception as e:
        log_error(f"Erreur lors de la recherche web : {e}")
        return f"Erreur de recherche web : {e}"
