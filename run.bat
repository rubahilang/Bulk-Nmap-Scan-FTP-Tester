@echo off
:: Save the current directory
setlocal
set "CURRENT_DIR=%~dp0"

:: Check if running as administrator
openfiles >nul 2>&1
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%0' -Verb runAs"
    exit /b
)

:: Check if Python is installed
where python >nul 2>&1
if '%errorlevel%' NEQ '0' (
    echo Python not found. Installing Python...
    powershell -Command "Start-Process 'msiexec.exe' -ArgumentList '/i https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe /quiet InstallAllUsers=1 PrependPath=1' -Wait"
    if '%errorlevel%' NEQ '0' (
        echo [ERROR] Failed to install Python.
        exit /b
    )
    echo Python installed successfully.
)

:: Change to the directory containing the script
cd /d "%CURRENT_DIR%"

:: Run the Python script from the saved directory
python scan.py
pause
