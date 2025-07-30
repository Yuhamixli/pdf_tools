@echo off
chcp 65001 >nul
echo ========================================
echo PDF工具离线包制作脚本
echo ========================================
echo.

:: 设置Python路径
set "PYTHON_CMD=D:\Anaconda\python.exe"

:: 创建离线包目录
set "OFFLINE_DIR=PDF工具离线包"
if exist "%OFFLINE_DIR%" (
    echo [信息] 清理旧的离线包目录...
    rmdir /s /q "%OFFLINE_DIR%"
)

echo [信息] 创建离线包目录...
mkdir "%OFFLINE_DIR%"
mkdir "%OFFLINE_DIR%\packages"
mkdir "%OFFLINE_DIR%\tools"

:: 下载所有依赖包到本地
echo [信息] 下载依赖包到本地...
%PYTHON_CMD% -m pip download -r requirements.txt -d "%OFFLINE_DIR%\packages"

:: 复制所有工具文件
echo [信息] 复制工具文件...
copy "*.py" "%OFFLINE_DIR%\tools\"
copy "*.bat" "%OFFLINE_DIR%\tools\"
copy "*.txt" "%OFFLINE_DIR%\tools\"
copy "*.md" "%OFFLINE_DIR%\tools\"

:: 创建离线安装脚本
echo [信息] 创建离线安装脚本...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo PDF工具离线安装
echo echo ========================================
echo echo.
echo.
echo :: 检测Python环境
echo set "PYTHON_CMD="
echo.
echo :: 尝试查找Python
echo if exist "python.exe" ^(
echo     set "PYTHON_CMD=python.exe"
echo ^) else if exist "python3.exe" ^(
echo     set "PYTHON_CMD=python3.exe"
echo ^) else ^(
echo     echo [错误] 未找到Python，请确保Python已安装并添加到PATH
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] 使用Python: %%PYTHON_CMD%%
echo %%PYTHON_CMD%% --version
echo.
echo :: 安装依赖包
echo echo [信息] 安装依赖包...
echo %%PYTHON_CMD%% -m pip install --no-index --find-links packages -r requirements.txt
echo.
echo if %%errorlevel%% neq 0 ^(
echo     echo [错误] 依赖安装失败
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] 依赖安装完成
echo echo [信息] 启动PDF工具...
echo.
echo %%PYTHON_CMD%% pdf_tools.py
echo.
echo if %%errorlevel%% neq 0 ^(
echo     echo [错误] 启动失败
echo     pause
echo ^)
) > "%OFFLINE_DIR%\install_and_run.bat"

:: 创建快速启动脚本
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo PDF工具快速启动
echo echo ========================================
echo echo.
echo.
echo :: 检测Python环境
echo set "PYTHON_CMD="
echo.
echo :: 尝试查找Python
echo if exist "python.exe" ^(
echo     set "PYTHON_CMD=python.exe"
echo ^) else if exist "python3.exe" ^(
echo     set "PYTHON_CMD=python3.exe"
echo ^) else ^(
echo     echo [错误] 未找到Python，请确保Python已安装并添加到PATH
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] 使用Python: %%PYTHON_CMD%%
echo.
echo :: 检查依赖
echo %%PYTHON_CMD%% -c "import PyPDF2" ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo [信息] 依赖未安装，正在安装...
echo     call install_and_run.bat
echo     exit /b
echo ^)
echo.
echo echo [信息] 启动PDF工具...
echo %%PYTHON_CMD%% pdf_tools.py
) > "%OFFLINE_DIR%\start.bat"

:: 创建使用说明
(
echo # PDF工具离线包使用说明
echo.
echo ## 使用方法
echo.
echo ### 方法一：首次使用（推荐）
echo 1. 双击 `install_and_run.bat`
echo 2. 等待安装完成，工具会自动启动
echo.
echo ### 方法二：后续使用
echo 1. 双击 `start.bat` 直接启动
echo.
echo ## 系统要求
echo - Python 3.7 或更高版本
echo - Windows 7/8/10/11
echo.
echo ## 注意事项
echo - 首次使用需要安装依赖包，请耐心等待
echo - 确保Python已正确安装并添加到系统PATH
echo - 如遇问题，请查看错误信息或重新运行安装脚本
) > "%OFFLINE_DIR%\使用说明.txt"

:: 创建Python环境检测脚本
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo Python环境检测
echo echo ========================================
echo echo.
echo.
echo :: 检测Python版本
echo python --version 2^>nul
echo if %%errorlevel%% neq 0 ^(
echo     echo [错误] 未找到Python
echo     echo 请安装Python 3.7+并添加到PATH
echo     pause
echo     exit /b 1
echo ^)
echo.
echo :: 检测pip
echo python -m pip --version 2^>nul
echo if %%errorlevel%% neq 0 ^(
echo     echo [错误] pip不可用
echo     echo 请重新安装Python
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] Python环境正常
echo echo 可以运行 install_and_run.bat 安装依赖
echo.
echo pause
) > "%OFFLINE_DIR%\check_python.bat"

:: 创建压缩包
echo [信息] 创建压缩包...
powershell -command "Compress-Archive -Path '%OFFLINE_DIR%' -DestinationPath 'PDF工具离线包.zip' -Force"

echo.
echo ========================================
echo 离线包制作完成！
echo ========================================
echo.
echo 生成的文件：
echo - PDF工具离线包.zip （完整离线包）
echo - %OFFLINE_DIR% （解压后的目录）
echo.
echo 使用方法：
echo 1. 将 PDF工具离线包.zip 复制到目标机器
echo 2. 解压到任意目录
echo 3. 双击 install_and_run.bat 开始使用
echo.
pause 