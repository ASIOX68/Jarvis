# 🤖 Jarvis - Assistant Personnel Avancé

Bienvenue dans le dépôt de **Jarvis**, un assistant personnel local et cloud (moteur IA Gemini) conçu pour l'interaction vocale et textuelle, capable d'interagir nativement avec votre ordinateur.

## ✨ Fonctionnalités
- **Chat intelligent** : Propulsé par Google Gemini 2.5 Flash, avec mémoire temporelle pour tenir une vraie discussion.
- **Opérations Systèmes** : L'IA peut générer et exécuter des commandes bash automatiquement (avec votre accord de sécurité) depuis le prompt, et créer des fichiers ou dossiers localement.
- **Interaction Vocale** : Mode `--voice` intégré combinant *Speech-To-Text* (via micro) et *Text-To-Speech* temps réel.
- **Recherche Web Automatique** 🌐 : Scraping en arrière-plan (DuckDuckGo Search) pour retrouver et synthétiser de l'information fraîche depuis internet.
- **Lecteur de PDF** 📄 : L'assistant lit le contenu des documents `.pdf` envoyés et dresse un résumé compréhensif sur demande.
- **Générateur d'images** 🎨 : Crée des maquettes ou des arts conceptuels depuis le chat et les télécharge sur votre disque.
- **Contrôle Spotify** 🎵 : Commandez l'application musique ouverte avec votre voix (Lecture, Pause, Suivant).

## 🚀 Installation

### 1. Pré-requis
- **Python 3.10+**
- Un compte [Google AI Studio](https://aistudio.google.com/) pour obtenir une clé API gratuite.
- *(Optionnel mais recommandé sur Linux)* : Les librairies `espeak` ou `flite` pour le Text-to-Speech, et `playerctl` pour le contrôle Spotify.

### 2. Récupération et configuration
```bash
git clone https://github.com/ASIOX68/Jarvis.git
cd Jarvis
```

Créez un fichier **`.env`** à la racine pour sécuriser votre clé (ce fichier sera ignoré par Git) :
```
GEMINI_API_KEY=AIzaSy...votre_cle_ici...
```

### 3. Exécution du script magique
Pour l'installer, il suffit de run le script correspondant à votre OS :
- **Linux** : `./install.sh`
- **Windows** : `./install.bat`

Cela va créer et activer un environnement virtuel (`venv`), installer toutes les dépendances (requests, google-generativeai, pymupdf, duckduckgo-search, etc) et le préparer.

## 💻 Utilisation
Activez d'abord l'environnement avec `source venv/bin/activate` (Linux) ou `venv\Scripts\activate` (Windows), puis lancez Jarvis :

### Mode Textuel (CLI)
```bash
python main.py --cli
```

### Mode Vocal
```bash
python main.py --voice
```
*(Le mot de réveil par défaut est "Jarvis")*

---
**⚠️ Sécurité** : Des filtres dits "FORBIDDEN" sont activés dans `config.py` pour bloquer toute commande terminal potentiellement dangereuse (ex: rm -rf /).
