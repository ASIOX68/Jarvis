#!/bin/bash
echo "Installation de Ollama (IA Locale)..."
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
sleep 5
echo "Téléchargement de mistral..."
ollama pull mistral
echo "Ollama est prêt."
