import subprocess
from utils.logger import log_info, log_error, log_warning

def control_spotify(action: str) -> str:
    valid_actions = ["play", "pause", "play-pause", "next", "previous", "open"]
    if action not in valid_actions:
        return f"Action Spotify non reconnue : {action}. Actions valides : {valid_actions}"
        
    try:
        if action == "open":
            log_info("Ouverture de Spotify...")
            # Lance spotify en détachement (Background)
            subprocess.Popen(["spotify"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return "Spotify a été lancé avec succès."
            
        log_info(f"Contrôle Spotify : {action}")
        # Utilisation de playerctl (standard linux)
        result = subprocess.run(["playerctl", "--player=spotify", action], capture_output=True, text=True)
        if result.returncode == 0:
            return f"Action Spotify '{action}' exécutée avec succès."
        else:
            log_warning("playerctl a échoué. Spotify est-il lancé ?")
            return f"Impossible d'exécuter l'action. Assurez-vous que Spotify est ouvert et que 'playerctl' est installé. Erreur: {result.stderr}"
    except FileNotFoundError:
        log_error("La commande 'playerctl' ou 'spotify' est introuvable sur le système.")
        return "Erreur : playerctl ou spotify n'est peut-être pas installé (Linux uniquement pour l'instant via MPRIS)."
    except Exception as e:
        log_error(f"Erreur lors du contrôle de Spotify : {e}")
        return f"Erreur critique lors du contrôle de Spotify : {e}"
