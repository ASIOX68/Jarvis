import time
import json
from voice.stt import listen
from voice.tts import speak
from ai.llm import ask_llm
from system.commands import execute_system_command
from system.files import handle_file_operation
from system.web import search_web
from system.media import control_spotify
from system.images import generate_image
from system.pdf import read_pdf
from utils.logger import log_info, log_warning, log_error, log_success
from core.config import WAKE_WORD

class Jarvis:
    def __init__(self):
        log_info("Initialisation des cœurs IA et Systèmes...")
        # Initialiser les modèles ou check connexions ici
        pass

    def start_cli_mode(self):
        """Mode interactif en base de texte"""
        log_success("Jarvis est prêt. Tapez 'exit' ou 'quit' pour quitter.")
        while True:
            try:
                user_input = input("\n[Vous] > ")
                if user_input.lower() in ["exit", "quit"]:
                    break
                if not user_input.strip():
                    continue
                
                self.process_query(user_input)
            except Exception as e:
                log_error(f"Erreur durant la proccess CLI : {e}")

    def start_voice_mode(self):
        """Mode interactif vocal avec mot de réveil"""
        log_success(f"Mode vocal activé. Dites '{WAKE_WORD}' pour réveiller Jarvis.")
        speak("Mode vocal activé. Je suis à votre écoute.")
        
        while True:
            try:
                text = listen(wake_word_mode=True)
                if text and WAKE_WORD.lower() in text.lower():
                    log_success("Mot de réveil détecté !")
                    speak("Oui ?")
                    # Attendre la vraie commande
                    command = listen(wake_word_mode=False)
                    if command:
                        log_info(f"Commande entendue: {command}")
                        self.process_query(command)
            except Exception as e:
                log_error(f"Erreur en mode vocal : {e}")
                time.sleep(1)

    def process_query(self, query: str, is_retry: bool = False):
        """Gère la requête de l'utilisateur en interrogeant l'IA"""
        if not is_retry:
            log_info(f"Analyse de la demande : {query}")
        
        # Envoie au LLM avec prompt spécifique pour formater la réponse en JSON
        response = ask_llm(query)
        
        if not response:
            speak("Désolé, je n'ai pas pu générer une réponse.")
            return

        try:
            # On s'attend à ce que l'IA réponde avec un JSON structuré.
            data = json.loads(response)
            
            # Gemini renvoie parfois une liste d'un seul objet json [{...}] au lieu d'un simple {...}
            if isinstance(data, list) and len(data) > 0:
                data = data[0]
            elif not isinstance(data, dict):
                raise ValueError("Format JSON inattendu (ni dict ni liste valide).")

            action_type = data.get("type", "chat")
            message = data.get("message", "")
            action_payload = data.get("payload", {})

            # 1. Dire le message
            if message:
                log_success(f"[Jarvis] : {message}")
                speak(message)

            # 2. Exécuter l'action requise
            if action_type == "system":
                command = action_payload.get("command", "")
                if command:
                    success, error_msg = execute_system_command(command)
                    if not success and not is_retry and "Action annulée" not in error_msg:
                        log_warning("La commande a échoué. Demande de correction à l'IA...")
                        speak("La commande a échoué, je tente de me corriger.")
                        correction_prompt = f"La commande précédente '{command}' a échoué avec l'erreur : '{error_msg}'. Corrige-la et donne moi la bonne action système ou commande JSON."
                        self.process_query(correction_prompt, is_retry=True)
            
            elif action_type == "file":
                operation = action_payload.get("operation") # create, read, delete
                path = action_payload.get("path")
                content = action_payload.get("content", "")
                handle_file_operation(operation, path, content)
                
            elif action_type == "code_generation":
                # L'IA a généré du code, on peut le sauvegarder dans un fichier temp ou demandé
                path = action_payload.get("path", "generated_code.txt")
                content = action_payload.get("code", "")
                log_info(f"Code généré prêt à être sauvegardé dans {path}")
                handle_file_operation("create", path, content)

            elif action_type == "chat":
                # Juste une réponse texte
                pass
                
            elif action_type == "web_search":
                query = action_payload.get("query", "")
                if query:
                    search_result = search_web(query)
                    # Relancer l'IA avec le résultat pour qu'elle le lise et réponde
                    feedback = f"Résultat de la recherche pour '{query}' :\n{search_result}\n\nFais un résumé utile pour l'utilisateur."
                    self.process_query(feedback, is_retry=True)
                    
            elif action_type == "spotify":
                action = action_payload.get("action", "")
                if action:
                    res = control_spotify(action)
                    log_info(res)

            elif action_type == "image":
                prompt = action_payload.get("prompt", "")
                path = action_payload.get("path", "image_generee.jpg")
                if prompt:
                    res = generate_image(prompt, path)
                    log_info(res)

            elif action_type == "pdf_read":
                path = action_payload.get("path", "")
                if path:
                    pdf_content = read_pdf(path)
                    feedback = f"Contenu du PDF '{path}' :\n{pdf_content}\n\nAgis en conséquence avec ces données pour répondre à la demande."
                    self.process_query(feedback, is_retry=True)

            else:
                log_warning(f"Type d'action inconnu : {action_type}")

        except json.JSONDecodeError:
            # Cas où l'IA ne renvoie pas un JSON parfaitement formaté
            log_warning("La réponse de l'IA n'était pas au format JSON. Réponse brute :")
            log_success(f"[Jarvis] : {response}")
            speak(response)
