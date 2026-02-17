@echo off
echo ========================================
echo    MediaAgentIQ - AI Agent Platform
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q

echo.
echo Starting MediaAgentIQ server...
echo Dashboard: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
