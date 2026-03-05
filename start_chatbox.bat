@echo off
cd /d "%~dp0"

echo ==========================================================
echo Starting Hybrid Schema-LLM Guided Chatbox Environment
echo ==========================================================
echo.

echo [1/2] Starting AI Backend (FastAPI) on port 8080...
start cmd /k "python -m uvicorn backend.main:app --port 8081 --reload"

echo Waiting 3 seconds for backend to initialize...
timeout /t 3 /nobreak > nul

echo.
echo [2/2] Launching Chat Interface (Streamlit)...
start cmd /k "python -m streamlit run frontend/app.py"

echo.
echo Success! The Chatbox has been launched in your browser.
echo Please do not close the black terminal windows while using the chatbox.
pause
