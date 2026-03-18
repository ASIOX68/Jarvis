import requests
import os
import urllib.parse
from utils.logger import log_info, log_success, log_error

def generate_image(prompt: str, output_path: str = "generated_image.jpg") -> str:
    log_info(f"Génération de l'image pour le prompt : {prompt}")
    try:
        # Encode le prompt pour l'URL
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            # S'assurer que le dossier parent existe
            dir_name = os.path.dirname(os.path.abspath(output_path))
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
                
            with open(output_path, 'wb') as f:
                f.write(response.content)
            log_success(f"Image générée avec succès : {output_path}")
            return f"Image générée et sauvegardée au chemin : {os.path.abspath(output_path)}"
        else:
            err = f"L'API d'image a renvoyé le code {response.status_code}"
            log_error(err)
            return err
    except Exception as e:
        log_error(f"Erreur lors de la génération d'image : {e}")
        return f"Erreur lors de la création de l'image : {e}"
