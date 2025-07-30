@echo off
chcp 65001 >nul
echo ========================================
echo PDF Tools Executable Package Builder
echo ========================================
echo.

:: Set Python path
set "PYTHON_CMD=D:\Anaconda\python.exe"

:: Create executable directory
set "EXE_DIR=PDF工具可执行版"
if exist "%EXE_DIR%" (
    echo [INFO] Cleaning old executable directory...
    rmdir /s /q "%EXE_DIR%"
)

echo [INFO] Creating executable directory...
mkdir "%EXE_DIR%"

:: Check PyInstaller
echo [INFO] Checking PyInstaller...
%PYTHON_CMD% -c "import PyInstaller" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Installing PyInstaller...
    %PYTHON_CMD% -m pip install pyinstaller
)

:: Package main program
echo [INFO] Packaging PDF tools main program...
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name "PDF工具" pdf_tools.py

:: Package individual tools
echo [INFO] Packaging individual tools...
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name "PDF合并工具" pdf_merger.py
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name "PDF拖放合并" pdf_drag_drop.py
%PYTHON_CMD% -m PyInstaller --onefile --name "PDF命令行合并" pdf_merger_cli.py
%PYTHON_CMD% -m PyInstaller --onefile --name "PDF文件合并" pdf_merger_files.py

:: Copy executable files
echo [INFO] Copying executable files...
copy "dist\PDF工具.exe" "%EXE_DIR%\"
copy "dist\PDF合并工具.exe" "%EXE_DIR%\"
copy "dist\PDF拖放合并.exe" "%EXE_DIR%\"
copy "dist\PDF命令行合并.exe" "%EXE_DIR%\"
copy "dist\PDF文件合并.exe" "%EXE_DIR%\"

:: Create launcher script
echo [INFO] Creating launcher script...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo PDF Tools Launcher
echo echo ========================================
echo echo.
echo echo Please select a tool to launch:
echo echo.
echo echo 1. PDF Tools ^(Main Launcher^)
echo echo 2. PDF Merger ^(Folder Mode^)
echo echo 3. PDF Drag Drop ^(Drag Drop Mode^)
echo echo 4. PDF CLI Merger ^(Command Line Mode^)
echo echo 5. PDF Files Merger ^(File List Mode^)
echo echo 6. Exit
echo echo.
echo set /p choice=Enter your choice ^(1-6^): 
echo.
echo if "%%choice%%"=="1" goto tool1
echo if "%%choice%%"=="2" goto tool2
echo if "%%choice%%"=="3" goto tool3
echo if "%%choice%%"=="4" goto tool4
echo if "%%choice%%"=="5" goto tool5
echo if "%%choice%%"=="6" goto exit
echo goto invalid
echo.
echo :tool1
echo echo Launching PDF Tools...
echo start "" "PDF工具.exe"
echo goto end
echo.
echo :tool2
echo echo Launching PDF Merger...
echo start "" "PDF合并工具.exe"
echo goto end
echo.
echo :tool3
echo echo Launching PDF Drag Drop...
echo start "" "PDF拖放合并.exe"
echo goto end
echo.
echo :tool4
echo echo Launching PDF CLI Merger...
echo start "" "PDF命令行合并.exe"
echo goto end
echo.
echo :tool5
echo echo Launching PDF Files Merger...
echo start "" "PDF文件合并.exe"
echo goto end
echo.
echo :invalid
echo echo Invalid choice, please try again
echo goto end
echo.
echo :exit
echo echo Exiting
echo.
echo :end
echo pause
) > "%EXE_DIR%\启动器.bat"

:: Create usage instructions
(
echo # PDF Tools Executable Version Usage
echo.
echo ## Usage Methods
echo.
echo ### Method 1: Use Launcher ^(Recommended^)
echo 1. Double-click `启动器.bat`
echo 2. Select the tool you want to use
echo.
echo ### Method 2: Direct Launch
echo - Double-click `PDF工具.exe` - Main Launcher
echo - Double-click `PDF合并工具.exe` - Folder Mode
echo - Double-click `PDF拖放合并.exe` - Drag Drop Mode
echo - Double-click `PDF命令行合并.exe` - Command Line Mode
echo - Double-click `PDF文件合并.exe` - File List Mode
echo.
echo ## System Requirements
echo - Windows 7/8/10/11
echo - No Python installation required
echo - No dependencies required
echo.
echo ## File Description
echo - PDF工具.exe - Main Launcher ^(Recommended^)
echo - PDF合并工具.exe - Folder Mode Merger
echo - PDF拖放合并.exe - Drag Drop Mode Merger
echo - PDF命令行合并.exe - Command Line Mode
echo - PDF文件合并.exe - File List Mode
echo - 启动器.bat - Tool Selection Launcher
echo.
echo ## Features
echo - Completely independent, no software installation required
echo - Plug and play, double-click to run
echo - Supports all Windows systems
echo - Green and environmentally friendly, no residue
) > "%EXE_DIR%\使用说明.txt"

:: Clean temporary files
echo [INFO] Cleaning temporary files...
rmdir /s /q "build"
rmdir /s /q "dist"
del "*.spec"

:: Create zip package
echo [INFO] Creating zip package...
powershell -command "Compress-Archive -Path '%EXE_DIR%' -DestinationPath 'PDF工具可执行版.zip' -Force"

echo.
echo ========================================
echo Executable package creation completed!
echo ========================================
echo.
echo Generated files:
echo - PDF工具可执行版.zip ^(Complete executable package^)
echo - %EXE_DIR% ^(Extracted directory^)
echo.
echo Usage:
echo 1. Copy PDF工具可执行版.zip to target machine
echo 2. Extract to any directory
echo 3. Double-click 启动器.bat or directly double-click exe files
echo.
echo Features:
echo - Completely independent, no software installation required
echo - Plug and play, double-click to run
echo - Supports all Windows systems
echo - Green and environmentally friendly, no residue
echo.
pause 