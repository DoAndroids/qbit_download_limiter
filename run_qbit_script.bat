@echo off
REM Get the user's home directory
set "HOME_DIR=%USERPROFILE%"
set "VENV_DIR=%HOME_DIR%\PythonScripts\.venv"

REM Check if Python is installed
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

REM Create a virtual environment in the ".venv" folder if it doesn't exist
IF NOT EXIST "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

REM Activate the virtual environment
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate"

REM Install required dependencies
echo Installing dependencies...
pip install -q requests

REM Run the Python script
echo Running Python script...
IF NOT EXIST "%HOME_DIR%\PythonScripts\qbit_traffic_check.py" (
    echo Cannot find the Python script, exiting
    exit /b 1
)
python "%HOME_DIR%\PythonScripts\qbit_traffic_check.py"

REM Deactivate the virtual environment
echo Deactivating virtual environment...
deactivate

echo Script execution finished.
exit
