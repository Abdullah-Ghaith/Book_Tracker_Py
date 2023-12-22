@echo off

pip show pillow > nul 2>&1 || pip install pillow
pip show requests > nul 2>&1 || pip install requests

python3 main.py
