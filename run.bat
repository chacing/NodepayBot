@echo off
REM Run the NodePay Ping Utility

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b
)

REM Check if dependencies are installed by testing 'requests' package
python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    REM Install required dependencies if 'requests' is not found
    echo Installing required dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install dependencies. Please check your Python and pip setup.
        pause
        exit /b
    )
) else (
    echo Dependencies are already installed. Skipping installation.
)

REM Run the main script
echo Running NodePay Ping Utility...
python main.py

pause
