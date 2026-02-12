@echo off
echo ========================================
echo Starting MINDBRIDGE Server (Fresh)
echo ========================================
echo.

cd sleepy\server

echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/4] Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__
if exist *.pyc del /q *.pyc

echo [3/4] Starting Flask server...
echo.
echo Server will be available at: http://127.0.0.1:5000
echo.
echo To test the signup page:
echo   1. Open: http://127.0.0.1:5000/clear-cache-signup.html
echo   2. Or directly: http://127.0.0.1:5000/signup.html
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
