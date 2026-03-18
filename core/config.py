from enum import Enum

# Enum for Log Levels
class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4

# --- Configuration Jarvis ---

# IA (Google Gemini)
GEMINI_API_KEY = "AIzaSyCJC_cbhRHjPjuOHk5Gu_olIbEDwPvB7rY"
# Modèle suggéré: gemini-2.5-flash, gemini-2.5-pro
GEMINI_MODEL = "gemini-2.5-flash"

# IA (Ollama par défaut s'il doit être utilisé)
# OLLAMA_HOST = "http://localhost:11434"
# OLLAMA_MODEL = "mistral"

# Voix
WAKE_WORD = "jarvis"
VOICE_RATE = 175 # Vitesse de la voix
VOICE_VOLUME = 1.0

# Vosk Path (Model)
# Télécharger un modèle Vosk FR ou EN sur https://alphacephei.com/vosk/models
# et le placer dans models/vosk-model
VOSK_MODEL_PATH = "models/vosk-model"

# Sécurité
REQUIRE_CONFIRMATION_FOR_COMMANDS = True # Sécurité pour exécution bash/cmd
FORBIDDEN_COMMANDS = ["rm -rf /", "mkfs", "del /s /q", "format"] # Commandes bloquées

LOG_LEVEL = LogLevel.INFO
