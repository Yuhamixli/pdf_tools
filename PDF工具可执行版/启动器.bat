@echo off
chcp 65001 >nul
echo ========================================
echo PDF Tools Launcher
echo ========================================
echo.
echo Please select a tool to launch:
echo.
echo 1. PDF Tools (Main Launcher)
echo 2. PDF Merger (Folder Mode)
echo 3. PDF Drag Drop (Drag Drop Mode)
echo 4. PDF CLI Merger (Command Line Mode)
echo 5. PDF Files Merger (File List Mode)
echo 6. Exit
echo.
set /p choice=Enter your choice (1-6): 

if "%choice%"=="1" goto tool1
if "%choice%"=="2" goto tool2
if "%choice%"=="3" goto tool3
if "%choice%"=="4" goto tool4
if "%choice%"=="5" goto tool5
if "%choice%"=="6" goto exit
goto invalid

:tool1
echo Launching PDF Tools...
start "" "PDF工具.exe"
goto end

:tool2
echo Launching PDF Merger...
start "" "PDF合并工具.exe"
goto end

:tool3
echo Launching PDF Drag Drop...
start "" "PDF拖放合并.exe"
goto end

:tool4
echo Launching PDF CLI Merger...
start "" "PDF命令行合并.exe"
goto end

:tool5
echo Launching PDF Files Merger...
start "" "PDF文件合并.exe"
goto end

:invalid
echo Invalid choice, please try again
goto end

:exit
echo Exiting

:end
pause
