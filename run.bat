@echo off
start cmd /k "cd /d %~dp0 && .\venv\Scripts\activate && python -m uvicorn main:app --reload"
timeout /t 3
start http://127.0.0.1:8000
start cmd /k "cd /d %~dp0 && .\venv\Scripts\activate && python simulator.py"