@echo off
echo Installation de Jarvis...
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install setuptools
pip install -r requirements.txt
echo Installation terminée ! Tapez 'venv\Scripts\activate' puis 'python main.py --cli'.
pause
