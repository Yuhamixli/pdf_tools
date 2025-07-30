@echo off
chcp 65001 >nul
echo ========================================
echo PDF工具一键启动
echo ========================================
echo.

:: 尝试查找Python
set "PYTHON_CMD="
set "PYTHON_FOUND="

:: 首先尝试Anaconda Python
if exist "%USERPROFILE%\anaconda3\python.exe" (
    set "PYTHON_CMD=%USERPROFILE%\anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "%USERPROFILE%\Anaconda3\python.exe" (
    set "PYTHON_CMD=%USERPROFILE%\Anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "C:\anaconda3\python.exe" (
    set "PYTHON_CMD=C:\anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "C:\Anaconda3\python.exe" (
    set "PYTHON_CMD=C:\Anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "C:\ProgramData\Anaconda3\python.exe" (
    set "PYTHON_CMD=C:\ProgramData\Anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "C:\ProgramData\anaconda3\python.exe" (
    set "PYTHON_CMD=C:\ProgramData\anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "D:\anaconda3\python.exe" (
    set "PYTHON_CMD=D:\anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "D:\Anaconda3\python.exe" (
    set "PYTHON_CMD=D:\Anaconda3\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else if exist "D:\Anaconda\python.exe" (
    set "PYTHON_CMD=D:\Anaconda\python.exe"
    set "PYTHON_FOUND=1"
    echo [信息] 找到Anaconda Python: %PYTHON_CMD%
) else (
    :: 尝试系统Python
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_CMD=python"
        set "PYTHON_FOUND=1"
        echo [信息] 找到系统Python: %PYTHON_CMD%
    ) else (
        echo [错误] 未找到Python环境
        echo.
        echo 请选择以下解决方案之一：
        echo.
        echo 方案1：安装Anaconda（推荐）
        echo   下载地址: https://www.anaconda.com/download
        echo   安装后重新运行此脚本
        echo.
        echo 方案2：安装Python
        echo   下载地址: https://www.python.org/downloads/
        echo   安装时请勾选"Add Python to PATH"
        echo.
        echo 方案3：如果已安装Python但未添加到PATH
        echo   请手动设置环境变量或使用完整路径
        echo.
        pause
        exit /b 1
    )
)

if "%PYTHON_FOUND%"=="" (
    echo [错误] Python环境检测失败
    pause
    exit /b 1
)

:: 显示Python版本
echo [信息] Python版本信息：
%PYTHON_CMD% --version

:: 检查依赖是否已安装
echo.
echo [信息] 检查依赖...
%PYTHON_CMD% -c "import PyPDF2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [信息] 安装依赖包...
    echo [信息] 正在安装 PyPDF2, tkinterdnd2, pyinstaller...
    %PYTHON_CMD% -m pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败，请检查网络连接
        pause
        exit /b 1
    )
    echo [信息] 依赖安装完成
) else (
    echo [信息] 依赖已安装
)

:: 启动PDF工具
echo.
echo [信息] 启动PDF工具...
%PYTHON_CMD% pdf_tools.py

if %errorlevel% neq 0 (
    echo.
    echo [错误] 启动失败，可能的原因：
    echo   1. Python版本过低（需要3.7+）
    echo   2. 依赖安装不完整
    echo   3. 文件损坏或缺失
    echo   4. 权限问题
    echo.
    echo 请尝试以下解决方案：
    echo   1. 升级Python到3.7或更高版本
    echo   2. 以管理员身份运行此脚本
    echo   3. 检查网络连接后重新运行
    echo.
    pause
) 