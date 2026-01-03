# 银行智能体系统

一个基于 Streamlit 和 LangChain 的银行智能助手，支持余额查询和转账功能。

## 功能特性

- 💰 **余额查询**：查询指定账户的余额
- 🔄 **转账功能**：在账户之间执行转账操作
- 📋 **账户列表**：查看所有可用账户
- 💬 **自然语言交互**：使用自然语言与智能体对话

## 安装步骤

1. 克隆或下载项目到本地

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置 OpenAI API Key：
   - 在运行应用时，在侧边栏输入您的 OpenAI API Key
   - 或者设置环境变量：`export OPENAI_API_KEY=your_api_key_here`

## 运行应用

### 方法 1: 使用启动脚本（推荐）

**Windows 用户：**
双击运行 `run.bat` 文件

**Mac/Linux 用户：**
```bash
chmod +x run.sh
./run.sh
```

### 方法 2: 手动启动

```bash
streamlit run app.py
```

或

```bash
python -m streamlit run app.py
```

应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`

**注意：** 即使没有设置 OpenAI API Key，应用也能正常启动并显示界面。只有在与智能体对话时才需要 API Key。

## 使用示例

### 查询余额
```
查询账户1001的余额
```

### 转账操作
```
从账户1001向账户1002转账500元
```

### 列出账户
```
显示所有账户
```

## 项目结构

```
bank-agents/
├── app.py              # Streamlit 前端应用
├── bank_agent.py       # LangChain 智能体后端
├── bank_data.py        # 银行数据存储模块
├── requirements.txt    # Python 依赖包
└── README.md          # 项目说明文档
```

## 技术栈

- **前端**：Streamlit
- **后端**：LangChain
- **LLM**：OpenAI GPT-3.5-turbo / GPT-4
- **语言**：Python 3.8+

## 注意事项

- 本项目使用内存存储，重启应用后数据会重置
- 需要有效的 OpenAI API Key 才能使用
- 账户数据为示例数据，可根据需要修改 `bank_data.py` 中的初始化数据

## 许可证

MIT License

