@echo off
echo 正在为PDF合并工具创建打包环境...

REM 检查是否安装了Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到Python。请先安装Python并确保将其添加到系统PATH中。
    exit /b 1
)

REM 创建虚拟环境
if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo 错误: 无法创建虚拟环境。请确保已安装venv模块。
        exit /b 1
    )
)

REM 激活虚拟环境并安装依赖
echo 正在激活虚拟环境并安装依赖...
call venv\Scripts\activate
pip install -r requirements.txt
pip install pyinstaller

REM 执行打包操作
echo 正在打包应用...

REM 单独打包每个应用，并记录详细日志
echo 打包pdf_merger...
pyinstaller --onefile --windowed --name pdf_merger_1_0_0 pdf_merger.py --log-level=DEBUG > logs_pdf_merger.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo pdf_merger打包成功!
) else (
    echo pdf_merger打包失败，请查看logs_pdf_merger.txt获取详细信息
)

echo 打包pdf_merger_cli...
pyinstaller --onefile --name pdf_merger_cli_1_0_0 pdf_merger_cli.py --log-level=DEBUG > logs_pdf_merger_cli.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo pdf_merger_cli打包成功!
) else (
    echo pdf_merger_cli打包失败，请查看logs_pdf_merger_cli.txt获取详细信息
)

echo 打包pdf_merger_files...
pyinstaller --onefile --name pdf_merger_files_1_0_0 pdf_merger_files.py --log-level=DEBUG > logs_pdf_merger_files.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo pdf_merger_files打包成功!
) else (
    echo pdf_merger_files打包失败，请查看logs_pdf_merger_files.txt获取详细信息
)

echo 打包pdf_tools...
pyinstaller --onefile --windowed --name pdf_tools_1_0_0 pdf_tools.py --log-level=DEBUG > logs_pdf_tools.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo pdf_tools打包成功!
) else (
    echo pdf_tools打包失败，请查看logs_pdf_tools.txt获取详细信息
)

echo 打包pdf_drag_drop...
pyinstaller --onefile --windowed --name pdf_drag_drop_1_0_0 pdf_drag_drop.py --log-level=DEBUG > logs_pdf_drag_drop.txt 2>&1
if %ERRORLEVEL% EQU 0 (
    echo pdf_drag_drop打包成功!
) else (
    echo pdf_drag_drop打包失败，请查看logs_pdf_drag_drop.txt获取详细信息
)

REM 检查dist目录中的文件
echo.
echo 检查生成的可执行文件...
dir dist

REM 返回结果
if exist "dist\pdf_merger_1_0_0.exe" (
    echo pdf_merger构建成功!
) else (
    echo pdf_merger构建失败!
)

if exist "dist\pdf_merger_cli_1_0_0.exe" (
    echo pdf_merger_cli构建成功!
) else (
    echo pdf_merger_cli构建失败!
)

if exist "dist\pdf_merger_files_1_0_0.exe" (
    echo pdf_merger_files构建成功!
) else (
    echo pdf_merger_files构建失败!
)

if exist "dist\pdf_tools_1_0_0.exe" (
    echo pdf_tools构建成功!
) else (
    echo pdf_tools构建失败!
)

if exist "dist\pdf_drag_drop_1_0_0.exe" (
    echo pdf_drag_drop构建成功!
) else (
    echo pdf_drag_drop构建失败!
)

REM 禁用虚拟环境
call venv\Scripts\deactivate

echo 打包过程完成。
pause 