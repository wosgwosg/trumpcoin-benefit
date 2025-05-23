@echo off
REM TrumpCoin Benefit Program Development Server Script
REM This script activates the virtual environment and runs the development server

echo Starting TrumpCoin Benefit Program Development Server...
echo.

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Run the development server
python manage.py runserver

REM If the server stops, keep the window open
pause
