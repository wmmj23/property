# menu_functions/insert_data.py
"""
数据插入模块 - 插入股票、基金等投资信息
"""
import logging
from typing import Optional, List, Dict, Any
from database import get_database

from utils import (
    print_header, print_success, print_error, print_warning, print_info,
    clear_screen, confirm_action
)

logger = logging.getLogger(__name__)


class DataInserter:
    """数据插入器"""
    
    def __init__(self, db):
        self.db = db
        self._cache_data()
    
    def _cache_data(self):
        """缓存所有外键表的数据供用户选择"""
        # 市场信息
        self.markets = {}
        markets_data = self.db.get_all_markets()
        for market in markets_data:
            self.markets[market['id']] = {
                'code': market.get('code', ''),
                'name': market.get('name', ''),
                'desc': market.get('desc', '')
            }
        
        # 货币信息
        self.currencies = {}
        currencies_data = self.db.get_all_currencies()
        for currency in currencies_data:
            self.currencies[currency['id']] = currency.get('currency', '')
        
        # 资金类型
        self.four_type_money = {}
        money_data = self.db.get_all_four_type_money()
        for money in money_data:
            self.four_type_money[money['id']] = money.get('name', '')
        
        # 资产类别
        self.class_assets = {}
        assets_data = self.db.get_all_class_assets()
        for asset in assets_data:
            self.class_assets[asset['id']] = {
                'code': asset.get('code', ''),
                'name': asset.get('name', ''),
                'desc': asset.get('desc', '')
            }
        
        # 资产类型
        self.type_assets = {}
        type_data = self.db.get_all_type_assets()
        for asset_type in type_data:
            self.type_assets[asset_type['id']] = asset_type.get('name', '')
        
        # 账户信息
        self.accounts = {}
        accounts_data = self.db.get_all_accounts()
        for account in accounts_data:
            self.accounts[account['id']] = account.get('name', '')
        
        # 交易类型
        self.transaction_types = {}
        trans_types = self.db.get_all_transaction_types()
        for trans_type in trans_types:
            self.transaction_types[trans_type['id']] = trans_type.get('name', '')
    
    def select_from_list(self, data_dict: Dict, title: str, 
                         display_field: Optional[str] = None) -> tuple:
        """让用户从列表中选择一项"""
        clear_screen()
        print_header(title)
        
        print(f"\n{title}:")
        print("-" * 50)
        
        items = []
        for idx, (key, value) in enumerate(data_dict.items(), 1):
            if display_field and isinstance(value, dict):
                display_value = value.get(display_field, str(value))
            else:
                display_value = str(value)
            print(f"{idx}. {display_value}")
            items.append((key, value))
        
        while True:
            try:
                choice = input(f"\n请选择 (1-{len(items)}), 输入0取消: ").strip()
                if choice == '0':
                    return None, None
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(items):
                    selected_key, selected_value = items[choice_num-1]
                    if display_field and isinstance(selected_value, dict):
                        return selected_key, selected_value.get(display_field)
                    return selected_key, selected_value
                else:
                    print_error(f"请输入1-{len(items)}之间的数字")
            except ValueError:
                print_error("请输入有效的数字")
    
    def check_duplicate(self, table: str, field: str, value: str) -> bool:
        """检查重复记录"""
        query = f"SELECT COUNT(*) as count FROM {table} WHERE {field} = ?"
        result = self.db.execute_query(query, (value,))
        return result and result[0]['count'] > 0
    
    def insert_stock(self):
        """插入股票信息"""
        clear_screen()
        print_header("插入股票信息")
        
        try:
            # 输入基本信息
            code = input("请输入股票代码: ").strip()
            if not code:
                print_error("股票代码不能为空")
                return
            
            # 检查重复
            if self.check_duplicate('stock', 'code', code):
                print_error(f"股票代码 '{code}' 已存在!")
                return
            
            name = input("请输入股票名称: ").strip()
            if not name:
                print_error("股票名称不能为空")
                return
            
            if self.check_duplicate('stock', 'name', name):
                print_error(f"股票名称 '{name}' 已存在!")
                return
            
            # 选择市场
            market_id, market_name = self.select_from_list(
                self.markets, "选择市场", 'name'
            )
            if market_id is None:
                print_info("已取消")
                return
            
            # 选择货币
            currency_id, currency = self.select_from_list(
                self.currencies, "选择货币"
            )
            if currency_id is None:
                print_info("已取消")
                return
            
            # 选择资金类型
            four_type_money_id, money_type = self.select_from_list(
                self.four_type_money, "选择资金类型"
            )
            if four_type_money_id is None:
                print_info("已取消")
                return
            
            # 选择资产类别
            class_assets_id, class_name = self.select_from_list(
                self.class_assets, "选择资产类别", 'name'
            )
            if class_assets_id is None:
                print_info("已取消")
                return
            
            # 股票默认type_assets_id=1
            type_assets_id = 1
            
            # 显示确认信息
            clear_screen()
            print_header("确认股票信息")
            
            print("\n请确认股票信息:")
            print(f"股票代码: {code}")
            print(f"股票名称: {name}")
            print(f"市场: {market_name}")
            print(f"货币: {currency}")
            print(f"资金类型: {money_type}")
            print(f"资产类别: {class_name}")
            print(f"资产类型: 股票")
            
            if not confirm_action("\n确认录入?"):
                print_info("已取消录入")
                return
            
            # 插入数据
            sql = """
                INSERT INTO stock 
                (market_id, code, name, currency_id, four_type_money_id, 
                 class_assets_id, type_assets_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            if self.db is None:
                self.db = get_database()
            if not self.db.connect():
                    print_error("无法连接数据库，请检查数据库文件")
                    return
    
            self.db.execute_update(sql, (
                market_id, code, name, currency_id, four_type_money_id,
                class_assets_id, type_assets_id
            ))
            
            stock_id = self.db.get_last_insert_id()
            print_success(f"股票录入成功! ID: {stock_id}")
            
            # 询问是否录入净值
            if confirm_action("是否录入股票净值?"):
                self.insert_stock_nav(stock_id)
            
            return stock_id
            
        except Exception as e:
            print_error(f"插入股票失败: {e}")
            logger.exception("插入股票失败")
            return None
    
    def insert_fund(self):
        """插入基金信息"""
        clear_screen()
        print_header("插入基金信息")
        
        try:
            # 输入基本信息
            code = input("请输入基金代码: ").strip()
            if not code:
                print_error("基金代码不能为空")
                return
            
            # 检查重复
            if self.check_duplicate('fund', 'code', code):
                print_error(f"基金代码 '{code}' 已存在!")
                return
            
            name = input("请输入基金名称: ").strip()
            if not name:
                print_error("基金名称不能为空")
                return
            
            if self.check_duplicate('fund', 'name', name):
                print_error(f"基金名称 '{name}' 已存在!")
                return
            
            # 选择市场
            market_id, market_name = self.select_from_list(
                self.markets, "选择市场", 'name'
            )
            if market_id is None:
                print_info("已取消")
                return
            
            # 选择货币
            currency_id, currency = self.select_from_list(
                self.currencies, "选择货币"
            )
            if currency_id is None:
                print_info("已取消")
                return
            
            # 选择资金类型
            four_type_money_id, money_type = self.select_from_list(
                self.four_type_money, "选择资金类型"
            )
            if four_type_money_id is None:
                print_info("已取消")
                return
            
            # 选择资产类别
            class_assets_id, class_name = self.select_from_list(
                self.class_assets, "选择资产类别", 'name'
            )
            if class_assets_id is None:
                print_info("已取消")
                return
            
            # 基金默认type_assets_id=2
            type_assets_id = 2
            
            # 显示确认信息
            clear_screen()
            print_header("确认基金信息")
            
            print("\n请确认基金信息:")
            print(f"基金代码: {code}")
            print(f"基金名称: {name}")
            print(f"市场: {market_name}")
            print(f"货币: {currency}")
            print(f"资金类型: {money_type}")
            print(f"资产类别: {class_name}")
            print(f"资产类型: 基金")
            
            if not confirm_action("\n确认录入?"):
                print_info("已取消录入")
                return
            
            # 插入数据
            sql = """
                INSERT INTO fund 
                (market_id, code, name, currency_id, four_type_money_id, 
                 class_assets_id, type_assets_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            if self.db is None:
                self.db = get_database()
            if not self.db.connect():
                    print_error("无法连接数据库，请检查数据库文件")
                    return
            
            self.db.execute_update(sql, (
                market_id, code, name, currency_id, four_type_money_id,
                class_assets_id, type_assets_id
            ))
            
            fund_id = self.db.get_last_insert_id()
            print_success(f"基金录入成功! ID: {fund_id}")
            
            # 询问是否录入净值
            if confirm_action("是否录入基金净值?"):
                self.insert_fund_nav(fund_id)
            
            return fund_id
            
        except Exception as e:
            print_error(f"插入基金失败: {e}")
            logger.exception("插入基金失败")
            return None
    
    def insert_stock_nav(self, stock_id=None):
        """插入股票净值"""
        clear_screen()
        print_header("插入股票净值")
        
        try:
            if not stock_id:
                # 选择股票
                stocks = self.db.get_all_stocks()
                if not stocks:
                    print_warning("没有可用的股票记录")
                    return
                
                print("\n选择股票:")
                print("-" * 50)
                for idx, stock in enumerate(stocks, 1):
                    print(f"{idx}. {stock.get('code', '')} - {stock.get('name', '')}")
                
                try:
                    choice = int(input(f"\n请选择股票 (1-{len(stocks)}), 输入0取消: "))
                    if choice == 0:
                        return
                    if 1 <= choice <= len(stocks):
                        stock_id = stocks[choice-1]['id']
                    else:
                        print_error("选择无效")
                        return
                except ValueError:
                    print_error("请输入有效的数字")
                    return
            
            # 输入净值信息
            date = input("请输入净值日期 (YYYY-MM-DD): ").strip()
            if not date:
                print_error("日期不能为空")
                return
            
            try:
                nav = float(input("请输入净值: ").strip())
                if nav <= 0:
                    print_error("净值必须大于0")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 确认信息
            print(f"\n股票ID: {stock_id}")
            print(f"日期: {date}")
            print(f"净值: {nav}")
            
            if not confirm_action("\n确认录入?"):
                print_info("已取消录入")
                return
            
            if self.db is None:
                self.db = get_database()
            if not self.db.connect():
                    print_error("无法连接数据库，请检查数据库文件")
                    return
            
            # 插入数据
            sql = "INSERT INTO stock_net_asset_value (stock_id, date, nav) VALUES (?, ?, ?)"
            self.db.execute_update(sql, (stock_id, date, nav))
            
            print_success("股票净值录入成功!")
            
        except Exception as e:
            print_error(f"插入股票净值失败: {e}")
            logger.exception("插入股票净值失败")
    
    def insert_fund_nav(self, fund_id=None):
        """插入基金净值"""
        clear_screen()
        print_header("插入基金净值")
        
        try:
            if not fund_id:
                # 选择基金
                funds = self.db.get_all_funds()
                if not funds:
                    print_warning("没有可用的基金记录")
                    return
                
                print("\n选择基金:")
                print("-" * 50)
                for idx, fund in enumerate(funds, 1):
                    print(f"{idx}. {fund.get('code', '')} - {fund.get('name', '')}")
                
                try:
                    choice = int(input(f"\n请选择基金 (1-{len(funds)}), 输入0取消: "))
                    if choice == 0:
                        return
                    if 1 <= choice <= len(funds):
                        fund_id = funds[choice-1]['id']
                    else:
                        print_error("选择无效")
                        return
                except ValueError:
                    print_error("请输入有效的数字")
                    return
            
            # 输入净值信息
            date = input("请输入净值日期 (YYYY-MM-DD): ").strip()
            if not date:
                print_error("日期不能为空")
                return
            
            try:
                nav = float(input("请输入净值: ").strip())
                if nav <= 0:
                    print_error("净值必须大于0")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 确认信息
            print(f"\n基金ID: {fund_id}")
            print(f"日期: {date}")
            print(f"净值: {nav}")
            
            if not confirm_action("\n确认录入?"):
                print_info("已取消录入")
                return
            
            if self.db is None:
                self.db = get_database()
            if not self.db.connect():
                    print_error("无法连接数据库，请检查数据库文件")
                    return
            
            # 插入数据
            sql = "INSERT INTO fund_net_asset_value (fund_id, date, nav) VALUES (?, ?, ?)"
            self.db.execute_update(sql, (fund_id, date, nav))
            
            print_success("基金净值录入成功!")
            
        except Exception as e:
            print_error(f"插入基金净值失败: {e}")
            logger.exception("插入基金净值失败")
    
    def insert_stock_transaction(self):
        """插入股票交易记录"""
        clear_screen()
        print_header("插入股票交易记录")
        
        try:
            # 选择股票
            stocks = self.db.get_all_stocks()
            if not stocks:
                print_warning("没有可用的股票记录")
                return
            
            print("\n选择股票:")
            print("-" * 50)
            for idx, stock in enumerate(stocks, 1):
                print(f"{idx}. {stock.get('code', '')} - {stock.get('name', '')}")
            
            try:
                choice = int(input(f"\n请选择股票 (1-{len(stocks)}), 输入0取消: "))
                if choice == 0:
                    return
                if 1 <= choice <= len(stocks):
                    stock_id = stocks[choice-1]['id']
                    stock_code = stocks[choice-1]['code']
                    stock_name = stocks[choice-1]['name']
                else:
                    print_error("选择无效")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 选择交易类型
            trans_type_id, trans_type_name = self.select_from_list(
                self.transaction_types, "选择交易类型"
            )
            if trans_type_id is None:
                return
            
            # 选择账户
            account_id, account_name = self.select_from_list(
                self.accounts, "选择账户"
            )
            if account_id is None:
                return
            
            # 输入交易详情
            transaction_date = input("请输入交易日期 (YYYY-MM-DD): ").strip()
            if not transaction_date:
                print_error("交易日期不能为空")
                return
            
            try:
                quantity = float(input("请输入交易数量: ").strip())
                if quantity <= 0:
                    print_error("交易数量必须大于0")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            try:
                price = float(input("请输入价格: ").strip())
                if price <= 0:
                    print_error("价格必须大于0")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 计算成交额
            turnover = quantity * price
            
            try:
                fee = float(input("请输入手续费 (默认为0): ").strip() or "0")
                if fee < 0:
                    print_error("手续费不能为负数")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 计算交易金额 (买入为负，卖出为正)
            if trans_type_name == "买入":
                transaction_amount = -(turnover + fee)
            elif trans_type_name == "卖出":
                transaction_amount = turnover - fee
            else:  # 分红/利息
                transaction_amount = turnover - fee
            
            notes = input("请输入备注 (可选): ").strip()
            
            # 显示确认信息
            clear_screen()
            print_header("确认股票交易记录")
            
            print("\n请确认交易记录:")
            print(f"股票: {stock_code} - {stock_name}")
            print(f"交易类型: {trans_type_name}")
            print(f"账户: {account_name}")
            print(f"交易日期: {transaction_date}")
            print(f"数量: {quantity}")
            print(f"价格: {price}")
            print(f"成交额: {turnover:.2f}")
            print(f"手续费: {fee:.2f}")
            print(f"交易金额: {transaction_amount:.2f}")
            if notes:
                print(f"备注: {notes}")
            
            if not confirm_action("\n确认录入?"):
                print_info("已取消录入")
                return
            
            # 插入数据
            sql = """
                INSERT INTO stock_transactions 
                (transaction_date, stock_id, type_transction_id, quantity, price, 
                 turnover, fee, transaction_amount, account_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            if self.db is None:
                self.db = get_database()
            if not self.db.connect():
                    print_error("无法连接数据库，请检查数据库文件")
                    return
            
            self.db.execute_update(sql, (
                transaction_date, stock_id, trans_type_id, quantity, price,
                turnover, fee, transaction_amount, account_id, notes or None
            ))
            
            trans_id = self.db.get_last_insert_id()
            print_success(f"股票交易记录录入成功! ID: {trans_id}")
            
        except Exception as e:
            print_error(f"插入股票交易记录失败: {e}")
            logger.exception("插入股票交易记录失败")
    
    def insert_fund_transaction(self):
        """插入基金交易记录"""
        clear_screen()
        print_header("插入基金交易记录")
        
        try:
            # 选择基金
            funds = self.db.get_all_funds()
            if not funds:
                print_warning("没有可用的基金记录")
                return
            
            print("\n选择基金:")
            print("-" * 50)
            for idx, fund in enumerate(funds, 1):
                print(f"{idx}. {fund.get('code', '')} - {fund.get('name', '')}")
            
            try:
                choice = int(input(f"\n请选择基金 (1-{len(funds)}), 输入0取消: "))
                if choice == 0:
                    return
                if 1 <= choice <= len(funds):
                    fund_id = funds[choice-1]['id']
                    fund_code = funds[choice-1]['code']
                    fund_name = funds[choice-1]['name']
                else:
                    print_error("选择无效")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 选择交易类型
            trans_type_id, trans_type_name = self.select_from_list(
                self.transaction_types, "选择交易类型"
            )
            if trans_type_id is None:
                return
            
            # 选择账户
            account_id, account_name = self.select_from_list(
                self.accounts, "选择账户"
            )
            if account_id is None:
                return
            
            # 输入交易详情
            transaction_date = input("请输入交易日期 (YYYY-MM-DD): ").strip()
            if not transaction_date:
                print_error("交易日期不能为空")
                return
            
            try:
                quantity = float(input("请输入交易数量: ").strip())
                if quantity <= 0:
                    print_error("交易数量必须大于0")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            try:
                price = float(input("请输入价格: ").strip())
                if price <= 0:
                    print_error("价格必须大于0")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 计算成交额
            turnover = quantity * price
            
            try:
                fee = float(input("请输入手续费 (默认为0): ").strip() or "0")
                if fee < 0:
                    print_error("手续费不能为负数")
                    return
            except ValueError:
                print_error("请输入有效的数字")
                return
            
            # 计算交易金额 (买入为负，卖出为正)
            if trans_type_name == "买入":
                transaction_amount = -(turnover + fee)
            elif trans_type_name == "卖出":
                transaction_amount = turnover - fee
            else:  # 分红/利息
                transaction_amount = turnover - fee
            
            notes = input("请输入备注 (可选): ").strip()
            
            # 显示确认信息
            clear_screen()
            print_header("确认基金交易记录")
            
            print("\n请确认交易记录:")
            print(f"基金: {fund_code} - {fund_name}")
            print(f"交易类型: {trans_type_name}")
            print(f"账户: {account_name}")
            print(f"交易日期: {transaction_date}")
            print(f"数量: {quantity}")
            print(f"价格: {price}")
            print(f"成交额: {turnover:.2f}")
            print(f"手续费: {fee:.2f}")
            print(f"交易金额: {transaction_amount:.2f}")
            if notes:
                print(f"备注: {notes}")
            
            if not confirm_action("\n确认录入?"):
                print_info("已取消录入")
                return
            
            # 插入数据
            sql = """
                INSERT INTO fund_transactions 
                (transaction_date, fund_id, type_transction_id, quantity, price, 
                 turnover, fee, transaction_amount, account_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            if self.db is None:
                self.db = get_database()
            if not self.db.connect():
                    print_error("无法连接数据库，请检查数据库文件")
                    return
            
            self.db.execute_update(sql, (
                transaction_date, fund_id, trans_type_id, quantity, price,
                turnover, fee, transaction_amount, account_id, notes or None
            ))
            
            trans_id = self.db.get_last_insert_id()
            print_success(f"基金交易记录录入成功! ID: {trans_id}")
            
        except Exception as e:
            print_error(f"插入基金交易记录失败: {e}")
            logger.exception("插入基金交易记录失败")


def insert_stock_info(db):
    """插入股票信息"""
    inserter = DataInserter(db)
    inserter.insert_stock()


def insert_fund_info(db):
    """插入基金信息"""
    inserter = DataInserter(db)
    inserter.insert_fund()


def insert_stock_transaction_info(db):
    """插入股票交易记录"""
    inserter = DataInserter(db)
    inserter.insert_stock_transaction()


def insert_fund_transaction_info(db):
    """插入基金交易记录"""
    inserter = DataInserter(db)
    inserter.insert_fund_transaction()


def insert_stock_nav_info(db):
    """插入股票净值"""
    inserter = DataInserter(db)
    inserter.insert_stock_nav()


def insert_fund_nav_info(db):
    """插入基金净值"""
    inserter = DataInserter(db)
    inserter.insert_fund_nav()


# 为向后兼容提供主函数
def main(db=None):
    """主函数"""
    from database import get_database
    if db is None:
        db = get_database()
    
    if not db.connect():
        print_error("无法连接数据库")
        return
    
    
    try:
        clear_screen()
        print_header("数据插入系统")
        
        while True:
            print("\n请选择操作:")
            print("1. 插入股票信息")
            print("2. 插入基金信息")
            print("3. 插入股票交易记录")
            print("4. 插入基金交易记录")
            print("5. 插入股票净值")
            print("6. 插入基金净值")
            print("0. 返回主菜单")
            
            choice = input("\n请选择 (0-6): ").strip()
            
            if choice == "1":
                insert_stock_info(db)
            elif choice == "2":
                insert_fund_info(db)
            elif choice == "3":
                insert_stock_transaction_info(db)
            elif choice == "4":
                insert_fund_transaction_info(db)
            elif choice == "5":
                insert_stock_nav_info(db)
            elif choice == "6":
                insert_fund_nav_info(db)
            elif choice == "0":
                break
            else:
                print_error("无效的选择")
            
            input("\n按回车键继续...")
            clear_screen()
            print_header("数据插入系统")
    
    except Exception as e:
        print_error(f"操作失败: {e}")
        logger.exception("数据插入失败")
    finally:
        db.close()


if __name__ == "__main__":
    main()