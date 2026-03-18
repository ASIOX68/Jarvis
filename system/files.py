import os
from utils.logger import log_info, log_error, log_success

def handle_file_operation(operation: str, path: str, content: str = "") -> bool:
    path = os.path.abspath(path)
    try:
        if operation == "create":
            dir_name = os.path.dirname(path)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            log_success(f"Fichier créé : {path}")
            return True
            
        elif operation == "create_dir":
            os.makedirs(path, exist_ok=True)
            log_success(f"Dossier créé : {path}")
            return True
            
        elif operation == "read":
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = f.read()
                log_info(f"Fichier lu : {path}")
                # Dans un cas réel, on renverrait data pour le LLM, 
                # ici on se contente d'indiquer le succès coté système.
                return True
            else:
                log_error(f"Fichier introuvable : {path}")
                return False
                
        elif operation == "delete":
            if os.path.exists(path):
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
                log_success(f"Élément supprimé : {path}")
                return True
            else:
                log_error(f"Fichier introuvable pour suppression : {path}")
                return False
                
        else:
            log_error(f"Opération sur fichier inconnue : {operation}")
            return False
    except Exception as e:
        log_error(f"Erreur lors de l'opération '{operation}' sur '{path}' : {e}")
        return False
