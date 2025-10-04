@echo off
set REPO_NAME=app-discord
cd $HOME/Downloads
if exist "%REPO_NAME%" (
    echo Repository already exists. Updating...
    cd %REPO_NAME%
    git pull
) else (
    echo Cloning repository...
    git clone https://github.com/dev-rorybolan/app-discord.git
    if errorlevel 1 (
        echo Failed to clone repository!
        pause
        exit /b 1
    )
    cd %REPO_NAME%
)

if errorlevel 1 (
    echo Failed to change directory!
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Failed to install dependencies!
    pause
    exit /b 1
)

echo Running application...
cd src
python main.py

pause
