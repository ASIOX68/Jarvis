import speech_recognition as sr
from utils.logger import log_info, log_error

def listen(wake_word_mode: bool = False) -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        if not wake_word_mode:
            log_info("Écoute en cours...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            log_error(f"Erreur de réseau (STT) : {e}")
            return ""
        except Exception as e:
            log_error(f"Erreur STT inattendue : {e}")
            return ""
