import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferMemory
import os

# --- 1. 配置页面 ---
st.set_page_config(page_title="AI 银行智能体 (MVP)", page_icon="🏦")
st.title("🏦 AI 银行柜员 (MVP版)")
st.caption("我是您的智能理财助手，可以帮您查询余额、转账或提供理财建议。")

# --- 2. 获取 API Key ---
# 在本地开发时从 .env 获取，在 Zeabur 部署时从环境变量获取
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("请输入 OpenAI API Key", type="password")

# --- 3. 模拟银行数据库 (Mock Data) ---
# 使用 session_state 保持数据在对话中持久化
if "db" not in st.session_state:
    st.session_state["db"] = {
        "balance": 50000.0,  # 初始余额
        "history": ["存款: +50000"]
    }

# --- 4. 定义工具函数 (Tools) ---
def get_balance(query=""):
    """查询当前账户余额"""
    return f"您当前的账户余额为: ¥{st.session_state['db']['balance']}"

def transfer_money(input_str):
    """
    转账功能。
    输入格式应为: '收款人,金额' (例如: 张三,100)
    """
    try:
        parts = input_str.split(",")
        if len(parts) < 2:
            return "转账失败：请提供收款人和金额，中间用逗号分隔。"
        
        receiver = parts[0].strip()
        amount = float(parts[1].strip())
        
        if amount > st.session_state['db']['balance']:
            return f"转账失败：余额不足。当前余额: {st.session_state['db']['balance']}"
        
        st.session_state['db']['balance'] -= amount
        st.session_state['db']['history'].append(f"转账给 {receiver}: -{amount}")
        return f"转账成功！已向 {receiver} 转账 ¥{amount}。剩余余额: ¥{st.session_state['db']['balance']}"
    except Exception as e:
        return f"转账处理出错: {str(e)}"

def get_history(query=""):
    """查询最近的交易记录"""
    return "\n".join(st.session_state['db']['history'])

# --- 5. 初始化 LangChain Agent ---
if api_key:
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=api_key)

    tools = [
        Tool(
            name="CheckBalance",
            func=get_balance,
            description="当用户询问余额、有多少钱时使用此工具。"
        ),
        Tool(
            name="TransferMoney",
            func=transfer_money,
            description="当用户想要转账时使用。输入必须是'收款人,金额'的格式。如果在对话中用户只说了金额和人，你需要自行格式化参数。"
        ),
        Tool(
            name="TransactionHistory",
            func=get_history,
            description="当用户询问交易记录、历史记录、流水时使用此工具。"
        )
    ]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory,
        handle_parsing_errors=True
    )

    # --- 6. 聊天界面逻辑 ---
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "您好！我是您的银行AI助手。请问有什么可以帮您？\n(试着问：'我有多少钱？' 或 '转账100元给Alice')"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st_callback = st.container()
            response = agent.run(prompt)
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.warning("请在侧边栏输入 OpenAI API Key 以启动服务。")