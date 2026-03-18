#!/bin/bash
echo "Installation de Jarvis..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install setuptools
pip install -r requirements.txt
echo "Installation terminée ! Tapez 'source venv/bin/activate' puis 'python main.py --cli'."
