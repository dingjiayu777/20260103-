"""
银行数据存储模块 - 模拟银行账户数据
"""
from typing import Dict, Optional
from datetime import datetime
import json

class BankAccount:
    """银行账户类"""
    def __init__(self, account_id: str, name: str, balance: float):
        self.account_id = account_id
        self.name = name
        self.balance = balance
        self.transactions = []
    
    def add_transaction(self, transaction_type: str, amount: float, to_account: Optional[str] = None):
        """添加交易记录"""
        transaction = {
            "timestamp": datetime.now().isoformat(),
            "type": transaction_type,
            "amount": amount,
            "to_account": to_account,
            "balance_after": self.balance
        }
        self.transactions.append(transaction)
        return transaction

class BankDatabase:
    """银行数据库（内存存储）"""
    def __init__(self):
        self.accounts: Dict[str, BankAccount] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """初始化示例账户数据"""
        # 创建几个示例账户
        accounts_data = [
            {"account_id": "1001", "name": "张三", "balance": 10000.0},
            {"account_id": "1002", "name": "李四", "balance": 5000.0},
            {"account_id": "1003", "name": "王五", "balance": 8000.0},
        ]
        
        for acc_data in accounts_data:
            account = BankAccount(
                account_id=acc_data["account_id"],
                name=acc_data["name"],
                balance=acc_data["balance"]
            )
            self.accounts[acc_data["account_id"]] = account
    
    def get_account(self, account_id: str) -> Optional[BankAccount]:
        """获取账户信息"""
        return self.accounts.get(account_id)
    
    def get_balance(self, account_id: str) -> Optional[float]:
        """查询账户余额"""
        account = self.get_account(account_id)
        if account:
            return account.balance
        return None
    
    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> Dict:
        """执行转账操作"""
        from_account = self.get_account(from_account_id)
        to_account = self.get_account(to_account_id)
        
        if not from_account:
            return {"success": False, "message": f"源账户 {from_account_id} 不存在"}
        
        if not to_account:
            return {"success": False, "message": f"目标账户 {to_account_id} 不存在"}
        
        if from_account_id == to_account_id:
            return {"success": False, "message": "不能向自己转账"}
        
        if amount <= 0:
            return {"success": False, "message": "转账金额必须大于0"}
        
        if from_account.balance < amount:
            return {"success": False, "message": f"余额不足，当前余额: {from_account.balance}"}
        
        # 执行转账
        from_account.balance -= amount
        to_account.balance += amount
        
        # 记录交易
        from_transaction = from_account.add_transaction("转出", amount, to_account_id)
        to_transaction = to_account.add_transaction("转入", amount, from_account_id)
        
        return {
            "success": True,
            "message": f"转账成功！从 {from_account.name}({from_account_id}) 向 {to_account.name}({to_account_id}) 转账 {amount} 元",
            "from_balance": from_account.balance,
            "to_balance": to_account.balance,
            "transaction": from_transaction
        }
    
    def list_accounts(self) -> list:
        """列出所有账户"""
        return [
            {
                "account_id": acc.account_id,
                "name": acc.name,
                "balance": acc.balance
            }
            for acc in self.accounts.values()
        ]

# 全局银行数据库实例
bank_db = BankDatabase()

