@echo off
echo 正在启动银行智能助手...
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查依赖是否安装
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动 Streamlit 应用
echo 正在启动应用...
echo 应用将在浏览器中自动打开
echo 如果没有自动打开，请访问: http://localhost:8501
echo.
python -m streamlit run app.py

pause

