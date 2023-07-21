@echo off
if "%~1"=="" (
    echo Usage: run_fixed_script.bat "path/to/directory"
    exit /b 1
)

set "python_script=C:\tally-codebrewers\diskmanager.py"
set "path_arg=%~1"

if not exist "%path_arg%" (
    echo The specified path does not exist.
    exit /b 1
)


python "%python_script%" "%path_arg%"

