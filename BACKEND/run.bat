@echo off
echo Starting Uvicorn Server...
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
pause