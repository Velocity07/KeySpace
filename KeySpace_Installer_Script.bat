@echo off
setlocal EnableDelayedExpansion
title Installing KeySpace...
for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

echo %ESC%[96m==================================================%ESC%[0m
echo %ESC%[96m               KeySpace Installer                 %ESC%[0m
echo %ESC%[96m==================================================%ESC%[0m
echo %ESC%[90mMade by Velocity7%ESC%[0m
echo.

echo %ESC%[33m[*] Installing required dependencies (customtkinter)...%ESC%[0m
pip install customtkinter -q
if %ERRORLEVEL% NEQ 0 (
    echo %ESC%[91m[X] Failed to install dependencies. Make sure Python is installed.%ESC%[0m
    pause
    exit /b
)
echo %ESC%[92m[+] Dependencies installed successfully.%ESC%[0m
echo.

echo %ESC%[33m[*] Copying application files to AppData...%ESC%[0m
set "SRC_DIR=%~dp0"
if "%SRC_DIR:~-1%"=="\" set "SRC_DIR=%SRC_DIR:~0,-1%"
if exist "%AppData%\KeySpace" rmdir /s /q "%AppData%\KeySpace"
mkdir "%AppData%\KeySpace"
xcopy /E /Y /I /Q /H /R "%SRC_DIR%\*" "%AppData%\KeySpace\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo %ESC%[92m[+] Files copied successfully.%ESC%[0m
) else (
    echo %ESC%[91m[X] Failed to copy files.%ESC%[0m
)
echo.

echo %ESC%[33m[*] Creating Start Menu shortcuts...%ESC%[0m
if exist "%AppData%\KeySpace\ShortCut" (
    move /y "%AppData%\KeySpace\ShortCut\*.*" "%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" >nul 2>&1
    echo %ESC%[92m[+] Shortcuts added successfully.%ESC%[0m
) else (
    echo %ESC%[90m[-] No shortcuts found to add.%ESC%[0m
)
echo.
echo %ESC%[96m==================================================%ESC%[0m
echo %ESC%[92m        Installation Finished Successfully!       %ESC%[0m
echo %ESC%[96m==================================================%ESC%[0m
timeout /t 3 >nul