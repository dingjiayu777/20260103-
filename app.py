"""
银行智能体 Streamlit 前端
"""
import streamlit as st
import os
import sys

# 延迟导入，避免在没有 API Key 时出错
try:
    from bank_agent import create_bank_agent
    from bank_data import bank_db
except Exception as e:
    st.error(f"导入模块时出错: {str(e)}")
    st.stop()

# 页面配置
st.set_page_config(
    page_title="银行智能助手",
    page_icon="🏦",
    layout="wide"
)

# 初始化 session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "api_key_set" not in st.session_state:
    st.session_state.api_key_set = False

def initialize_agent(api_key: str):
    """初始化智能体"""
    if not api_key or not api_key.strip():
        return False
    
    try:
        st.session_state.agent = create_bank_agent(api_key.strip())
        st.session_state.api_key_set = True
        return True
    except Exception as e:
        error_msg = str(e)
        if "api" in error_msg.lower() or "key" in error_msg.lower():
            st.error(f"API Key 无效或格式错误: {error_msg}")
        else:
            st.error(f"初始化智能体失败: {error_msg}")
        return False

# 侧边栏 - API 配置和账户信息
with st.sidebar:
    st.title("🏦 银行智能助手")
    st.divider()
    
    # API Key 配置
    st.subheader("API 配置")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="请输入您的 OpenAI API Key"
    )
    
    if st.button("设置 API Key", type="primary"):
        if api_key:
            with st.spinner("正在初始化智能体..."):
                if initialize_agent(api_key):
                    st.success("智能体初始化成功！")
                    st.rerun()
        else:
            st.error("请输入有效的 API Key")
    
    # 显示当前状态
    if st.session_state.api_key_set:
        st.success("✅ API Key 已设置")
    else:
        st.warning("⚠️ 请先设置 API Key")
    
    st.divider()
    
    # 账户信息
    st.subheader("账户信息")
    accounts = bank_db.list_accounts()
    for acc in accounts:
        st.info(f"**{acc['name']}** ({acc['account_id']})\n余额: ¥{acc['balance']:,.2f}")
    
    st.divider()
    
    # 快速操作示例
    st.subheader("💡 使用示例")
    st.markdown("""
    你可以尝试以下操作：
    
    - 查询余额：查询账户1001的余额
    - 转账：从账户1001向账户1002转账500元
    - 列出账户：显示所有账户
    """)

# 主界面
st.title("🏦 银行智能助手")
st.markdown("---")

# 显示聊天历史
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 检查 API Key 是否已设置
    if not st.session_state.api_key_set:
        st.error("请先在侧边栏设置 OpenAI API Key")
        st.stop()
    
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 获取智能体响应
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            try:
                response = st.session_state.agent.invoke({"input": prompt})
                answer = response.get("output", "抱歉，我无法处理您的请求。")
                
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                error_msg = f"发生错误: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# 底部说明
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        <small>银行智能助手 - 使用 LangChain 和 Streamlit 构建</small>
    </div>
    """,
    unsafe_allow_html=True
)

