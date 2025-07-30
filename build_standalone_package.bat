@echo off
chcp 65001 >nul
echo ========================================
echo PDF工具独立绿色包制作脚本
echo ========================================
echo.

:: 设置Python路径
set "PYTHON_CMD=D:\Anaconda\python.exe"

:: 创建独立包目录
set "STANDALONE_DIR=PDF工具绿色版"
if exist "%STANDALONE_DIR%" (
    echo [信息] 清理旧的绿色包目录...
    rmdir /s /q "%STANDALONE_DIR%"
)

echo [信息] 创建绿色包目录...
mkdir "%STANDALONE_DIR%"
mkdir "%STANDALONE_DIR%\python"
mkdir "%STANDALONE_DIR%\packages"
mkdir "%STANDALONE_DIR%\tools"

:: 复制Python解释器（如果使用Anaconda）
echo [信息] 复制Python解释器...
xcopy "D:\Anaconda\python.exe" "%STANDALONE_DIR%\python\" /Y
xcopy "D:\Anaconda\pythonw.exe" "%STANDALONE_DIR%\python\" /Y
xcopy "D:\Anaconda\python3.exe" "%STANDALONE_DIR%\python\" /Y
xcopy "D:\Anaconda\python3w.exe" "%STANDALONE_DIR%\python\" /Y

:: 复制Python库文件
echo [信息] 复制Python库文件...
xcopy "D:\Anaconda\Lib" "%STANDALONE_DIR%\python\Lib\" /E /I /Y
xcopy "D:\Anaconda\DLLs" "%STANDALONE_DIR%\python\DLLs\" /E /I /Y
xcopy "D:\Anaconda\Scripts" "%STANDALONE_DIR%\python\Scripts\" /E /I /Y

:: 下载所有依赖包到本地
echo [信息] 下载依赖包到本地...
%PYTHON_CMD% -m pip download -r requirements.txt -d "%STANDALONE_DIR%\packages"

:: 复制所有工具文件
echo [信息] 复制工具文件...
copy "*.py" "%STANDALONE_DIR%\tools\"
copy "*.txt" "%STANDALONE_DIR%\tools\"
copy "*.md" "%STANDALONE_DIR%\tools\"

:: 创建独立启动脚本
echo [信息] 创建独立启动脚本...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo PDF工具绿色版
echo echo ========================================
echo echo.
echo.
echo :: 设置Python路径
echo set "PYTHON_CMD=python\python.exe"
echo.
echo :: 检查Python是否存在
echo if not exist "%%PYTHON_CMD%%" ^(
echo     echo [错误] 未找到Python解释器
echo     echo 请确保文件完整
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] 使用内置Python: %%PYTHON_CMD%%
echo %%PYTHON_CMD%% --version
echo.
echo :: 检查依赖
echo %%PYTHON_CMD%% -c "import PyPDF2" ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo [信息] 安装依赖包...
echo     %%PYTHON_CMD%% -m pip install --no-index --find-links packages -r tools\requirements.txt
echo     if %%errorlevel%% neq 0 ^(
echo         echo [错误] 依赖安装失败
echo         pause
echo         exit /b 1
echo     ^)
echo     echo [信息] 依赖安装完成
echo ^) else ^(
echo     echo [信息] 依赖已安装
echo ^)
echo.
echo echo [信息] 启动PDF工具...
echo %%PYTHON_CMD%% tools\pdf_tools.py
echo.
echo if %%errorlevel%% neq 0 ^(
echo     echo [错误] 启动失败
echo     pause
echo ^)
) > "%STANDALONE_DIR%\启动PDF工具.bat"

:: 创建安装脚本
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo PDF工具依赖安装
echo echo ========================================
echo echo.
echo.
echo :: 设置Python路径
echo set "PYTHON_CMD=python\python.exe"
echo.
echo :: 检查Python是否存在
echo if not exist "%%PYTHON_CMD%%" ^(
echo     echo [错误] 未找到Python解释器
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] 安装依赖包...
echo %%PYTHON_CMD%% -m pip install --no-index --find-links packages -r tools\requirements.txt
echo.
echo if %%errorlevel%% neq 0 ^(
echo     echo [错误] 依赖安装失败
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [信息] 依赖安装完成
echo echo 现在可以运行 启动PDF工具.bat
echo.
echo pause
) > "%STANDALONE_DIR%\安装依赖.bat"

:: 创建使用说明
(
echo # PDF工具绿色版使用说明
echo.
echo ## 使用方法
echo.
echo ### 首次使用
echo 1. 双击 `安装依赖.bat` 安装依赖包
echo 2. 双击 `启动PDF工具.bat` 启动工具
echo.
echo ### 后续使用
echo 直接双击 `启动PDF工具.bat` 即可启动
echo.
echo ## 系统要求
echo - Windows 7/8/10/11
echo - 无需安装Python（已内置）
echo.
echo ## 文件说明
echo - python\ - Python解释器和库文件
echo - packages\ - 依赖包文件
echo - tools\ - PDF工具源代码
echo - 启动PDF工具.bat - 主启动脚本
echo - 安装依赖.bat - 依赖安装脚本
echo.
echo ## 注意事项
echo - 首次使用需要安装依赖包，请耐心等待
echo - 确保所有文件完整，不要删除任何文件
echo - 如遇问题，请重新运行安装依赖脚本
) > "%STANDALONE_DIR%\使用说明.txt"

:: 创建压缩包
echo [信息] 创建压缩包...
powershell -command "Compress-Archive -Path '%STANDALONE_DIR%' -DestinationPath 'PDF工具绿色版.zip' -Force"

echo.
echo ========================================
echo 独立绿色包制作完成！
echo ========================================
echo.
echo 生成的文件：
echo - PDF工具绿色版.zip （完整独立包）
echo - %STANDALONE_DIR% （解压后的目录）
echo.
echo 使用方法：
echo 1. 将 PDF工具绿色版.zip 复制到目标机器
echo 2. 解压到任意目录
echo 3. 双击 安装依赖.bat 安装依赖
echo 4. 双击 启动PDF工具.bat 启动工具
echo.
echo 特点：
echo - 完全独立，无需安装Python
echo - 包含所有依赖包
echo - 即插即用，绿色环保
echo.
pause 