import subprocess
import shlex
from core.config import REQUIRE_CONFIRMATION_FOR_COMMANDS, FORBIDDEN_COMMANDS
from utils.logger import log_warning, log_error, log_info

def execute_system_command(command: str) -> tuple[bool, str]:
    for forbidden in FORBIDDEN_COMMANDS:
        if forbidden in command:
            log_error(f"Commande interdite : {command}")
            return False, "Commande interdite pour des raisons de sécurité."

    if REQUIRE_CONFIRMATION_FOR_COMMANDS:
        log_warning(f"L'IA souhaite exécuter la commande suivante :\n> {command}")
        choice = input("Autoriser l'exécution ? (o/n) : ")
        if choice.lower() != 'o':
            log_warning("Exécution annulée par l'utilisateur.")
            return False, "Action annulée par l'utilisateur."

    log_info("Exécution en cours...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return True, result.stdout
        else:
            err_msg = f"Code de retour {result.returncode}\nSortie standard:\n{result.stdout}\nErreur standard:\n{result.stderr}"
            log_error(f"Erreur lors de l'exécution :\n{err_msg}")
            return False, err_msg
    except Exception as e:
        log_error(f"Exception lors de l'exécution : {e}")
        return False, str(e)
