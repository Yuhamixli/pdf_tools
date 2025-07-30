@echo off
chcp 65001 >nul
echo ========================================
echo PDF Tools Test Build
echo ========================================
echo.

:: Set Python path
set "PYTHON_CMD=D:\Anaconda\python.exe"

:: Create test directory
set "TEST_DIR=PDF工具测试版"
if exist "%TEST_DIR%" (
    echo [INFO] Cleaning old test directory...
    rmdir /s /q "%TEST_DIR%"
)

echo [INFO] Creating test directory...
mkdir "%TEST_DIR%"

:: Test PyInstaller
echo [INFO] Testing PyInstaller...
%PYTHON_CMD% -c "import PyInstaller; print('PyInstaller is available')"

:: Try to build one simple exe
echo [INFO] Building test executable...
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name "PDF工具测试" pdf_tools.py

:: Check if build was successful
if exist "dist\PDF工具测试.exe" (
    echo [INFO] Build successful!
    copy "dist\PDF工具测试.exe" "%TEST_DIR%\"
    echo [INFO] Test executable copied to %TEST_DIR%
) else (
    echo [ERROR] Build failed!
)

:: Clean up
rmdir /s /q "build"
rmdir /s /q "dist"
del "*.spec"

echo.
echo ========================================
echo Test build completed!
echo ========================================
echo.
pause 