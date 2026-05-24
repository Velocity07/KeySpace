@echo off
setlocal EnableDelayedExpansion
title Updating KeySpace to V2.0...

for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

echo %ESC%[96m==================================================%ESC%[0m
echo %ESC%[96m                KeySpace Updater                  %ESC%[0m
echo %ESC%[96m==================================================%ESC%[0m
echo %ESC%[90mMade by Velocity7%ESC%[0m
echo.

echo %ESC%[33m[*] Updating dependencies (customtkinter)...%ESC%[0m
pip install customtkinter -U -q
if %ERRORLEVEL% NEQ 0 (
    echo %ESC%[91m[X] Failed to update dependencies. Make sure Python is installed.%ESC%[0m
) else (
    echo %ESC%[92m[+] Dependencies updated successfully.%ESC%[0m
)
echo.

echo %ESC%[33m[*] Updating application files...%ESC%[0m
set "SRC_DIR=%~dp0"
if "%SRC_DIR:~-1%"=="\" set "SRC_DIR=%SRC_DIR:~0,-1%"
set "APP_DIR=%AppData%\KeySpace"
if exist "%SRC_DIR%\KeySpace.py" (
    xcopy /Y /Q /H /R "%SRC_DIR%\KeySpace.py" "%APP_DIR%\" >nul 2>&1
    if exist "%SRC_DIR%\ShortCut" xcopy /E /Y /I /Q /H /R "%SRC_DIR%\ShortCut" "%APP_DIR%\ShortCut" >nul 2>&1
    attrib +h "%APP_DIR%\KeySpace.py"   
    echo %ESC%[92m[+] Application files updated to V2.0 successfully.%ESC%[0m
) else (
    echo %ESC%[91m[X] Source update package not found! Please run this script from the update folder.%ESC%[0m
)
echo.

echo %ESC%[33m[*] Updating Start Menu shortcuts...%ESC%[0m
del /f /q /a "%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\*KeySpace*.lnk" >nul 2>&1
if exist "%APP_DIR%\ShortCut" (
    copy /y "%APP_DIR%\ShortCut\*.*" "%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs" >nul 2>&1
    echo %ESC%[92m[+] Start Menu shortcuts updated to V2.0.%ESC%[0m
) else (
    echo %ESC%[90m[-] No new shortcuts found to update.%ESC%[0m
)
echo.

echo %ESC%[96m==================================================%ESC%[0m
echo %ESC%[92m           Update Finished Successfully!          %ESC%[0m
echo %ESC%[96m==================================================%ESC%[0m
timeout /t 3 >nul