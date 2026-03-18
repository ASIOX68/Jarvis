import pyttsx3
from core.config import VOICE_RATE, VOICE_VOLUME
from utils.logger import log_error

def speak(text: str):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', VOICE_RATE)
        engine.setProperty('volume', VOICE_VOLUME)
        # Setup voice
        voices = engine.getProperty('voices')
        for voice in voices:
            if "fr" in voice.languages or "french" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
                
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        log_error(f"Erreur TTS : {e}")
