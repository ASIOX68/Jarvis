import json
import os
import google.generativeai as genai
from core.config import GEMINI_API_KEY, GEMINI_MODEL
from utils.logger import log_error

# Initialisation du client Google Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Ce System Prompt "force" l'IA locale (Ollama) ou Gemini à répondre avec un format JSON strict.
# C'est vital pour que le code Python puisse parser la réponse et générer des actions (commandes, code, etc.).
SYSTEM_PROMPT = """Tu es Jarvis, un assistant système avancé, expert en programmation et gestion de serveur.
Tu peux contrôler l'ordinateur de l'utilisateur.

Réponds TOUJOURS au format JSON strict avec la structure suivante :

1. Simple conversation :
{{
    "type": "chat",
    "message": "Ta réponse textuelle à dire à voix haute"
}}

2. Exécution de commande (si tu estimes la commande sûre) :
{{
    "type": "system",
    "message": "J'exécute la commande demandée.",
    "payload": {{"command": "la commande terminal"}}
}}

3. Gestion de fichier ou dossier (Créer, Lire, Supprimer) :
{{
    "type": "file",
    "message": "Je m'en occupe.",
    "payload": {{
        "operation": "create", 
        "path": "{chemin_absolu_ou_relatif}", 
        "content": "contenu du fichier (met une chaine de caractères vide si l'utilisateur veut juste un fichier vide ou un dossier)"
    }}
}}
Note : l'argument 'operation' DOIT être :
- "create" (pour créer un fichier et écrire dedans, ou pour créer un fichier vide)
- "create_dir" (pour créer UNIQUEMENT un nouveau dossier sans fichier dedans)
- "read" (pour lire)
- "delete" (pour supprimer)
IMPORTANT: Le chemin ('path') DOIT toujours être défini précisément. Ne dis jamais des choses comme 'sur le bureau' ou '/Users/mon-bureau/' si tu es sur Linux. Utilise des chemins absolus en te basant sur le dossier actuel : {cwd} et le dossier utilisateur : {home}.
"""

# Mémoire Conversationnelle (FIFO de 10 messages)
# En fonction du modèle, trop de contexte consomme beaucoup de RAM (local) ou d'argent (API externe)
conversation_history = []
MAX_HISTORY = 10  # On garde les 10 derniers échanges pour ne pas exploser le contexte

def ask_llm(prompt: str) -> str:
    """Envoie une requête à Google Gemini avec mémoire du contexte"""
    global conversation_history
    
    current_cwd = os.getcwd()
    user_home = os.path.expanduser("~")
    formatted_system_prompt = SYSTEM_PROMPT.format(
        cwd=current_cwd,
        home=user_home,
        chemin_absolu_ou_relatif="{chemin_absolu_ou_relatif}"
    )
    # Instanciation du modèle avec le prompt système et contrainte JSON
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=formatted_system_prompt,
        generation_config={"response_mime_type": "application/json"}
    )
    
    # Construire la mémoire temporaire pour cet appel (Format Gemini)
    messages = []
    for msg in conversation_history:
        messages.append({
            "role": "user" if msg["role"] == "user" else "model",
            "parts": [msg["content"]]
        })
    messages.append({"role": "user", "parts": [prompt]})

    try:
        response = model.generate_content(messages)
        assistant_reply = response.text
        
        if assistant_reply:
            # Mise à jour de l'historique de Jarvis
            conversation_history.append({"role": "user", "content": prompt})
            conversation_history.append({"role": "assistant", "content": assistant_reply})
            
            # Nettoyage si l'historique est trop long
            if len(conversation_history) > MAX_HISTORY * 2:
                conversation_history = conversation_history[-(MAX_HISTORY * 2):]
                
            return assistant_reply
        else:
            log_error("Gemini a renvoyé une réponse vide.")
            return ""
            
    except Exception as e:
        log_error(f"Erreur lors de l'appel à Gemini. Vérifiez votre clé ou votre connexion : {e}")
        return ""
