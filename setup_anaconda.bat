@echo off
echo ========================================
echo PDF工具 - Anaconda环境配置脚本
echo ========================================
echo.

:: 尝试查找Anaconda安装路径
set "ANACONDA_FOUND="
set "ANACONDA_PATHS="

:: 常见的Anaconda安装路径
if exist "%USERPROFILE%\anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=%USERPROFILE%\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "%USERPROFILE%\Anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=%USERPROFILE%\Anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=C:\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\Anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=C:\Anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\ProgramData\Anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=C:\ProgramData\Anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "C:\ProgramData\anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=C:\ProgramData\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "D:\anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=D:\anaconda3"
    set "ANACONDA_FOUND=1"
) else if exist "D:\Anaconda3\Scripts\conda.exe" (
    set "ANACONDA_PATH=D:\Anaconda3"
    set "ANACONDA_FOUND=1"
)

if "%ANACONDA_FOUND%"=="" (
    echo [错误] 未找到Anaconda安装，请检查以下路径：
    echo   %USERPROFILE%\anaconda3
    echo   %USERPROFILE%\Anaconda3
    echo   C:\anaconda3
    echo   C:\Anaconda3
    echo   C:\ProgramData\Anaconda3
    echo   C:\ProgramData\anaconda3
    echo   D:\anaconda3
    echo   D:\Anaconda3
    echo.
    echo 如果Anaconda安装在其他位置，请手动设置环境变量或运行：
    echo   set ANACONDA_PATH=你的Anaconda安装路径
    pause
    exit /b 1
)

echo [信息] 找到Anaconda安装: %ANACONDA_PATH%

:: 设置Anaconda环境变量
set "PATH=%ANACONDA_PATH%;%ANACONDA_PATH%\Scripts;%ANACONDA_PATH%\Library\bin;%PATH%"

:: 检查conda是否可用
"%ANACONDA_PATH%\Scripts\conda.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] conda命令不可用
    pause
    exit /b 1
)

echo [信息] conda可用
"%ANACONDA_PATH%\Scripts\conda.exe" --version

:: 检查Python是否可用
"%ANACONDA_PATH%\python.exe" --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] Python不可用
    pause
    exit /b 1
)

echo [信息] Python可用
"%ANACONDA_PATH%\python.exe" --version

:: 升级pip
echo.
echo [信息] 升级pip到最新版本...
"%ANACONDA_PATH%\python.exe" -m pip install --upgrade pip

:: 安装依赖
echo.
echo [信息] 安装项目依赖...
"%ANACONDA_PATH%\python.exe" -m pip install -r requirements.txt

:: 验证安装
echo.
echo [信息] 验证安装结果...
"%ANACONDA_PATH%\python.exe" -c "import PyPDF2; print('PyPDF2版本:', PyPDF2.__version__)"
"%ANACONDA_PATH%\python.exe" -c "import tkinterdnd2; print('tkinterdnd2安装成功')" 2>nul || echo [警告] tkinterdnd2安装可能有问题，但不影响基本功能

echo.
echo ========================================
echo 环境配置完成！
echo ========================================
echo.
echo 现在你可以运行以下命令启动PDF工具：
echo   "%ANACONDA_PATH%\python.exe" pdf_tools.py
echo.
echo 或者运行其他工具：
echo   "%ANACONDA_PATH%\python.exe" pdf_merger.py
echo   "%ANACONDA_PATH%\python.exe" pdf_drag_drop.py
echo   "%ANACONDA_PATH%\python.exe" pdf_merger_cli.py
echo.
echo 提示：为了更方便使用，建议将以下路径添加到系统PATH：
echo   %ANACONDA_PATH%
echo   %ANACONDA_PATH%\Scripts
echo.
pause 