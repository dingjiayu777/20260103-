#!/bin/bash

echo "正在启动银行智能助手..."
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python，请先安装 Python 3.8 或更高版本"
    exit 1
fi

# 检查依赖是否安装
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "正在安装依赖包..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误: 依赖安装失败"
        exit 1
    fi
fi

# 启动 Streamlit 应用
echo "正在启动应用..."
echo "应用将在浏览器中自动打开"
echo "如果没有自动打开，请访问: http://localhost:8501"
echo ""
python3 -m streamlit run app.py

