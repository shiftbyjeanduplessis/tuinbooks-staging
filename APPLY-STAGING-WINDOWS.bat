@echo off
setlocal
if "%~1"=="" (
  echo Drag your TuinBooks repository folder onto this BAT file, or run:
  echo APPLY-STAGING-WINDOWS.bat C:\path\to\TUINBOOKS-main
  pause
  exit /b 1
)
py "%~dp0APPLY-STAGING.py" "%~1"
if errorlevel 1 python "%~dp0APPLY-STAGING.py" "%~1"
echo.
py "%~dp0VERIFY-STAGING.py" "%~1"
if errorlevel 1 python "%~dp0VERIFY-STAGING.py" "%~1"
pause
