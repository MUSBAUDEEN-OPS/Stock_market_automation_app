@echo off
REM Quick Start Script for Stock Predictor App (Windows)
REM This script sets up and runs the app locally

echo ========================================
echo Stock Market Predictor - Quick Start
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Check if .env file exists
if not exist ".env" (
    echo No .env file found.
    echo Creating .env from template...
    copy .env.example .env
    echo .env file created. Please edit it with your email credentials.
    echo.
)

REM Create subscribers.json if it doesn't exist
if not exist "subscribers.json" (
    echo Creating subscribers file...
    echo [] > subscribers.json
)

echo.
echo Setup complete!
echo.
echo Starting Streamlit app...
echo The app will open in your browser at http://localhost:8501
echo.
echo To stop the app, press Ctrl+C
echo.

REM Run the app
streamlit run app.py
