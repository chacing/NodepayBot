@echo off
REM Run the Nodepay Ping Utility

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b
)

REM Run the main script
echo Running Nodepay Ping Utility...
python run.py

pause
