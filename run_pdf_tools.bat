@echo off
echo ========================================
echo PDF工具快速启动器
echo ========================================
echo.

:: 尝试查找Anaconda安装路径
set "ANACONDA_FOUND="

:: 常见的Anaconda安装路径
if exist "%USERPROFILE%\anaconda3\python.exe" (
    set "ANACONDA_PATH=%USERPROFILE%\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "%USERPROFILE%\Anaconda3\python.exe" (
    set "ANACONDA_PATH=%USERPROFILE%\Anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\anaconda3\python.exe" (
    set "ANACONDA_PATH=C:\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\Anaconda3\python.exe" (
    set "ANACONDA_PATH=C:\Anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set "ANACONDA_PATH=C:\ProgramData\Anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\ProgramData\anaconda3\python.exe" (
    set "ANACONDA_PATH=C:\ProgramData\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "D:\anaconda3\python.exe" (
    set "ANACONDA_PATH=D:\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "D:\Anaconda3\python.exe" (
    set "ANACONDA_PATH=D:\Anaconda3"
    set "ANACONDA_FOUND=1"
)

if "%ANACONDA_FOUND%"=="" (
    echo [错误] 未找到Anaconda Python，请先运行 setup_anaconda.bat 配置环境
    pause
    exit /b 1
)

echo [信息] 使用Anaconda Python: %ANACONDA_PATH%\python.exe

:: 检查PDF工具文件是否存在
if not exist "pdf_tools.py" (
    echo [错误] 未找到 pdf_tools.py 文件
    pause
    exit /b 1
)

:: 启动PDF工具
echo [信息] 启动PDF工具...
"%ANACONDA_PATH%\python.exe" pdf_tools.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 启动失败，可能的原因：
    echo   1. 依赖未安装，请先运行 setup_anaconda.bat
    echo   2. Python版本不兼容
    echo   3. 文件损坏
    echo.
    pause
) 