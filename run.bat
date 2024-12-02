@echo off

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python first.
    pause
    exit /b
)

:: Create a virtual environment if it does not exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install dependencies if they are not already installed
if not exist venv\Lib\site-packages\installed (
    if exist requirements.txt (
        echo Installing wheel for faster installation
        pip install wheel
        echo Installing dependencies...
        pip install -r requirements.txt
        echo. > venv\Lib\site-packages\installed
    ) else (
        echo requirements.txt not found, skipping dependency installation.
    )
) else (
    echo Dependencies are already installed, skipping installation.
)

:: Start the bot
echo Starting the bot...
python main.py

echo Done
pause
