import sys
from utils.logger import log_error, log_info
from core.jarvis import Jarvis

def main():
    if "--cli" in sys.argv:
        log_info("Démarrage de Jarvis en mode : CLI")
        jarvis_instance = Jarvis()
        jarvis_instance.start_cli_mode()
    elif "--voice" in sys.argv:
        log_info("Démarrage de Jarvis en mode : VOIX")
        jarvis_instance = Jarvis()
        jarvis_instance.start_voice_mode()
    else:
        print("Usage: python main.py [--cli | --voice]")

if __name__ == "__main__":
    main()
