import pymupdf
import os
from utils.logger import log_info, log_error

def read_pdf(path: str) -> str:
    path = os.path.abspath(path)
    log_info(f"Lecture du PDF : {path}")
    if not os.path.exists(path):
        err = f"Le fichier PDF n'existe pas : {path}"
        log_error(err)
        return err
        
    try:
        doc = pymupdf.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        
        if not text.strip():
            return f"Le PDF '{os.path.basename(path)}' a été lu mais aucun texte n'a pu être extrait (il s'agit peut-être d'images numérisées)."
            
        # Limiter la longueur si c'est astronomique
        max_chars = 50000 
        if len(text) > max_chars:
            text = text[:max_chars] + f"\n\n[... TEXTE TRONQUÉ CAR > {max_chars} CARACTÈRES ...]"
            
        return text
    except Exception as e:
        log_error(f"Erreur lors de la lecture du PDF {path} : {e}")
        return f"Erreur de lecture PDF : {e}"
