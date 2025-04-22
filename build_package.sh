#!/bin/bash

echo "正在为PDF合并工具创建打包环境..."

# 检查是否安装了Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python。请先安装Python 3。"
    exit 1
fi

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "正在创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "错误: 无法创建虚拟环境。请确保已安装venv模块。"
        exit 1
    fi
fi

# 激活虚拟环境并安装依赖
echo "正在激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -r requirements.txt

# 执行打包操作
echo "正在打包应用..."
python package.py all --version 1.0.0 --clean

# 返回结果
if [ $? -eq 0 ]; then
    echo "构建成功! 请查看dist目录获取可执行文件。"
else
    echo "构建失败! 请检查错误信息。"
fi

# 禁用虚拟环境
deactivate

echo "打包过程完成。"
read -p "按Enter键继续..." 