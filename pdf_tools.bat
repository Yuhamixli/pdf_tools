@echo off
echo 正在启动 PDF 工具集...
python pdf_tools.py
if %ERRORLEVEL% NEQ 0 (
    echo 启动失败，请检查是否已安装所需依赖。
    echo 如果尚未安装依赖，请运行以下命令：
    echo pip install -r requirements.txt
    pause
) 