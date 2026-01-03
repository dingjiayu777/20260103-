"""
银行智能体后端 - 使用 LangChain 构建
"""
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Optional
from bank_data import bank_db

# 定义余额查询工具
@tool
def check_balance(account_id: str) -> str:
    """
    查询账户余额
    
    Args:
        account_id: 账户ID，例如 "1001"
    
    Returns:
        账户余额信息字符串
    """
    account = bank_db.get_account(account_id)
    if not account:
        return f"账户 {account_id} 不存在"
    
    balance = bank_db.get_balance(account_id)
    return f"账户 {account_id} ({account.name}) 的当前余额为: {balance} 元"

# 定义转账工具
@tool
def transfer_money(from_account_id: str, to_account_id: str, amount: float) -> str:
    """
    执行转账操作
    
    Args:
        from_account_id: 源账户ID
        to_account_id: 目标账户ID
        amount: 转账金额（必须大于0）
    
    Returns:
        转账结果信息字符串
    """
    result = bank_db.transfer(from_account_id, to_account_id, amount)
    if result["success"]:
        return result["message"]
    else:
        return f"转账失败: {result['message']}"

# 定义账户列表工具
@tool
def list_accounts() -> str:
    """
    列出所有可用账户
    
    Returns:
        所有账户的列表信息
    """
    accounts = bank_db.list_accounts()
    if not accounts:
        return "没有可用账户"
    
    account_list = "\n".join([
        f"账户ID: {acc['account_id']}, 姓名: {acc['name']}, 余额: {acc['balance']} 元"
        for acc in accounts
    ])
    return f"可用账户列表:\n{account_list}"

def create_bank_agent(openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
    """
    创建银行智能体
    
    Args:
        openai_api_key: OpenAI API 密钥
        model_name: 使用的模型名称，默认为 gpt-3.5-turbo
    
    Returns:
        AgentExecutor 实例
    """
    # 初始化 LLM
    llm = ChatOpenAI(
        model=model_name,
        temperature=0,
        openai_api_key=openai_api_key
    )
    
    # 定义工具列表
    tools = [check_balance, transfer_money, list_accounts]
    
    # 定义提示词模板
    prompt = ChatPromptTemplate.from_messages([
        ("system", """你是一个专业的银行智能助手。你的职责是帮助用户查询账户余额和执行转账操作。

你可以使用的工具：
1. check_balance - 查询指定账户的余额
2. transfer_money - 执行转账操作
3. list_accounts - 列出所有可用账户

请始终：
- 使用友好的语气与用户交流
- 在执行转账前确认账户ID和金额
- 提供清晰的操作结果反馈
- 如果用户询问账户信息，可以使用 list_accounts 工具查看可用账户

当前可用账户示例：
- 账户ID: 1001, 姓名: 张三
- 账户ID: 1002, 姓名: 李四
- 账户ID: 1003, 姓名: 王五

请用中文回复用户。"""),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # 创建智能体
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # 创建执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor

