import sqlite3
import sys

class InvestmentDataEntry:
    def __init__(self, db_path='property.db'):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        
        # 缓存数据供选择
        self.cache_data()
    
    def cache_data(self):
        """缓存所有外键表的数据"""
        # 市场信息
        self.markets = {}
        markets_data = self.cursor.execute("SELECT id, code, name FROM market").fetchall()
        for row in markets_data:
            self.markets[row['id']] = {
                'code': row['code'],
                'name': row['name']
            }
        
        # 货币信息
        self.currencies = {}
        currencies_data = self.cursor.execute("SELECT id, currency FROM foreign_exchange").fetchall()
        for row in currencies_data:
            self.currencies[row['id']] = row['currency']
        
        # 资金类型
        self.four_type_money = {}
        money_data = self.cursor.execute("SELECT id, name FROM four_type_money").fetchall()
        for row in money_data:
            self.four_type_money[row['id']] = row['name']
        
        # 资产类别
        self.class_assets = {}
        assets_data = self.cursor.execute("SELECT id, code, name FROM class_assets").fetchall()
        for row in assets_data:
            self.class_assets[row['id']] = {
                'code': row['code'],
                'name': row['name']
            }
        
        # 资产类型
        self.type_assets = {}
        type_data = self.cursor.execute("SELECT id, name FROM type_assets").fetchall()
        for row in type_data:
            self.type_assets[row['id']] = row['name']
        
        # 账户信息
        self.accounts = {}
        accounts_data = self.cursor.execute("SELECT id, name FROM account").fetchall()
        for row in accounts_data:
            self.accounts[row['id']] = row['name']
    
    def display_menu(self):
        """显示主菜单"""
        print("\n" + "="*50)
        print("投资数据录入系统")
        print("="*50)
        print("1. 录入基金信息")
        print("2. 录入股票信息")
        print("3. 录入基金交易记录")
        print("4. 录入股票交易记录")
        print("5. 录入基金净值")
        print("6. 录入股票净值")
        print("7. 退出")
        print("="*50)
        
        choice = input("请选择操作 (1-7): ").strip()
        return choice
    
    def select_from_list(self, data_dict, title, value_field=None):
        """让用户从列表中选择一项"""
        print(f"\n{title}:")
        print("-"*50)
        
        items = []
        for idx, (key, value) in enumerate(data_dict.items(), 1):
            if value_field:
                display_value = value[value_field]
            else:
                display_value = value
            print(f"{idx}. {display_value}")
            items.append((key, value))
        
        while True:
            try:
                choice = int(input(f"\n请选择 (1-{len(items)}): "))
                if 1 <= choice <= len(items):
                    selected_key, selected_value = items[choice-1]
                    if value_field:
                        return selected_key, selected_value[value_field]
                    else:
                        return selected_key, selected_value
                else:
                    print(f"请输入1-{len(items)}之间的数字")
            except ValueError:
                print("请输入有效的数字")
    
    def insert_fund(self):
        """录入基金信息"""
        print("\n" + "="*50)
        print("录入基金信息")
        print("="*50)
        
        # 基本信息
        code = input("请输入基金代码: ").strip()
        name = input("请输入基金名称: ").strip()
        
        # 检查是否已存在
        existing = self.cursor.execute(
            "SELECT id FROM fund WHERE code = ? OR name = ?", 
            (code, name)
        ).fetchone()
        if existing:
            print(f"错误: 基金代码 '{code}' 或名称 '{name}' 已存在!")
            return
        
        # 选择市场
        market_id, market_info = self.select_from_list(
            self.markets, "选择市场", 'name'
        )
        
        # 选择货币
        currency_id, currency = self.select_from_list(
            self.currencies, "选择货币"
        )
        
        # 选择资金类型
        four_type_money_id, money_type = self.select_from_list(
            self.four_type_money, "选择资金类型"
        )
        
        # 选择资产类别
        class_assets_id, class_info = self.select_from_list(
            self.class_assets, "选择资产类别", 'name'
        )
        
        # 基金默认type_assets_id=2
        type_assets_id = 2
        
        # 确认信息
        print("\n请确认基金信息:")
        print(f"基金代码: {code}")
        print(f"基金名称: {name}")
        print(f"市场: {market_info}")
        print(f"货币: {currency}")
        print(f"资金类型: {money_type}")
        print(f"资产类别: {class_info}")
        print(f"资产类型: 基金")
        
        confirm = input("\n确认录入? (y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消录入")
            return
        
        # 插入数据
        try:
            self.cursor.execute("""
                INSERT INTO fund 
                (market_id, code, name, currency_id, four_type_money_id, class_assets_id, type_assets_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (market_id, code, name, currency_id, four_type_money_id, class_assets_id, type_assets_id))
            
            self.conn.commit()
            fund_id = self.cursor.lastrowid
            print(f"✅ 基金录入成功! ID: {fund_id}")
            
            # 询问是否录入净值
            if input("是否录入基金净值? (y/n): ").lower().strip() == 'y':
                self.insert_fund_nav(fund_id)
                
        except Exception as e:
            print(f"❌ 录入失败: {e}")
            self.conn.rollback()
    
    def insert_stock(self):
        """录入股票信息"""
        print("\n" + "="*50)
        print("录入股票信息")
        print("="*50)
        
        # 基本信息
        code = input("请输入股票代码: ").strip()
        name = input("请输入股票名称: ").strip()
        
        # 检查是否已存在
        existing = self.cursor.execute(
            "SELECT id FROM stock WHERE code = ? OR name = ?", 
            (code, name)
        ).fetchone()
        if existing:
            print(f"错误: 股票代码 '{code}' 或名称 '{name}' 已存在!")
            return
        
        # 选择市场
        market_id, market_info = self.select_from_list(
            self.markets, "选择市场", 'name'
        )
        
        # 选择货币
        currency_id, currency = self.select_from_list(
            self.currencies, "选择货币"
        )
        
        # 选择资金类型
        four_type_money_id, money_type = self.select_from_list(
            self.four_type_money, "选择资金类型"
        )
        
        # 选择资产类别
        class_assets_id, class_info = self.select_from_list(
            self.class_assets, "选择资产类别", 'name'
        )
        
        # 股票默认type_assets_id=1
        type_assets_id = 1
        
        # 确认信息
        print("\n请确认股票信息:")
        print(f"股票代码: {code}")
        print(f"股票名称: {name}")
        print(f"市场: {market_info}")
        print(f"货币: {currency}")
        print(f"资金类型: {money_type}")
        print(f"资产类别: {class_info}")
        print(f"资产类型: 股票")
        
        confirm = input("\n确认录入? (y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消录入")
            return
        
        # 插入数据
        try:
            self.cursor.execute("""
                INSERT INTO stock 
                (market_id, code, name, currency_id, four_type_money_id, class_assets_id, type_assets_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (market_id, code, name, currency_id, four_type_money_id, class_assets_id, type_assets_id))
            
            self.conn.commit()
            stock_id = self.cursor.lastrowid
            print(f"✅ 股票录入成功! ID: {stock_id}")
            
            # 询问是否录入净值
            if input("是否录入股票净值? (y/n): ").lower().strip() == 'y':
                self.insert_stock_nav(stock_id)
                
        except Exception as e:
            print(f"❌ 录入失败: {e}")
            self.conn.rollback()
    
    def insert_fund_transaction(self):
        """录入基金交易记录"""
        print("\n" + "="*50)
        print("录入基金交易记录")
        print("="*50)
        
        # 选择基金
        funds = self.cursor.execute("SELECT id, code, name FROM fund ORDER BY code").fetchall()
        if not funds:
            print("没有可用的基金记录")
            return
            
        print("\n选择基金:")
        print("-"*50)
        for idx, fund in enumerate(funds, 1):
            print(f"{idx}. {fund['code']} - {fund['name']}")
        
        try:
            choice = int(input(f"\n请选择基金 (1-{len(funds)}): "))
            if 1 <= choice <= len(funds):
                fund_id = funds[choice-1]['id']
                fund_code = funds[choice-1]['code']
                fund_name = funds[choice-1]['name']
            else:
                print("选择无效")
                return
        except ValueError:
            print("请输入有效的数字")
            return
        
        # 选择交易类型
        transaction_types = self.cursor.execute("SELECT id, name FROM type_transaction").fetchall()
        print("\n选择交易类型:")
        print("-"*50)
        for idx, ttype in enumerate(transaction_types, 1):
            print(f"{idx}. {ttype['name']}")
        
        try:
            t_choice = int(input(f"\n请选择交易类型 (1-{len(transaction_types)}): "))
            if 1 <= t_choice <= len(transaction_types):
                type_transction_id = transaction_types[t_choice-1]['id']
                type_name = transaction_types[t_choice-1]['name']
            else:
                print("选择无效")
                return
        except ValueError:
            print("请输入有效的数字")
            return
        
        # 选择账户
        account_id, account_name = self.select_from_list(
            self.accounts, "选择账户"
        )
        
        # 输入交易日期
        transaction_date = input("请输入交易日期 (YYYY-MM-DD): ").strip()
        
        # 输入交易数量
        quantity = float(input("请输入交易数量: ").strip())
        
        # 输入价格
        price = float(input("请输入价格: ").strip())
        
        # 计算成交额
        turnover = quantity * price
        
        # 输入手续费
        fee = float(input("请输入手续费 (0表示无手续费): ").strip() or "0")
        
        # 计算交易金额 (买入为负，卖出为正)
        if type_name == "买入":
            transaction_amount = -(turnover + fee)
        elif type_name == "卖出":
            transaction_amount = turnover - fee
        else:  # 分红/利息
            transaction_amount = turnover - fee
        
        # 输入备注
        notes = input("请输入备注 (可选): ").strip()
        
        # 确认信息
        print("\n请确认交易记录:")
        print(f"基金: {fund_code} - {fund_name}")
        print(f"交易类型: {type_name}")
        print(f"账户: {account_name}")
        print(f"交易日期: {transaction_date}")
        print(f"数量: {quantity}")
        print(f"价格: {price}")
        print(f"成交额: {turnover:.2f}")
        print(f"手续费: {fee:.2f}")
        print(f"交易金额: {transaction_amount:.2f}")
        if notes:
            print(f"备注: {notes}")
        
        confirm = input("\n确认录入? (y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消录入")
            return
        
        # 插入数据
        try:
            self.cursor.execute("""
                INSERT INTO fund_transactions 
                (transaction_date, fund_id, type_transction_id, quantity, price, 
                 turnover, fee, transaction_amount, account_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (transaction_date, fund_id, type_transction_id, quantity, price,
                  turnover, fee, transaction_amount, account_id, notes or None))
            
            self.conn.commit()
            trans_id = self.cursor.lastrowid
            print(f"✅ 基金交易记录录入成功! ID: {trans_id}")
                
        except Exception as e:
            print(f"❌ 录入失败: {e}")
            self.conn.rollback()
    
    def insert_stock_transaction(self):
        """录入股票交易记录"""
        print("\n" + "="*50)
        print("录入股票交易记录")
        print("="*50)
        
        # 选择股票
        stocks = self.cursor.execute("SELECT id, code, name FROM stock ORDER BY code").fetchall()
        if not stocks:
            print("没有可用的股票记录")
            return
            
        print("\n选择股票:")
        print("-"*50)
        for idx, stock in enumerate(stocks, 1):
            print(f"{idx}. {stock['code']} - {stock['name']}")
        
        try:
            choice = int(input(f"\n请选择股票 (1-{len(stocks)}): "))
            if 1 <= choice <= len(stocks):
                stock_id = stocks[choice-1]['id']
                stock_code = stocks[choice-1]['code']
                stock_name = stocks[choice-1]['name']
            else:
                print("选择无效")
                return
        except ValueError:
            print("请输入有效的数字")
            return
        
        # 选择交易类型
        transaction_types = self.cursor.execute("SELECT id, name FROM type_transaction").fetchall()
        print("\n选择交易类型:")
        print("-"*50)
        for idx, ttype in enumerate(transaction_types, 1):
            print(f"{idx}. {ttype['name']}")
        
        try:
            t_choice = int(input(f"\n请选择交易类型 (1-{len(transaction_types)}): "))
            if 1 <= t_choice <= len(transaction_types):
                type_transction_id = transaction_types[t_choice-1]['id']
                type_name = transaction_types[t_choice-1]['name']
            else:
                print("选择无效")
                return
        except ValueError:
            print("请输入有效的数字")
            return
        
        # 选择账户
        account_id, account_name = self.select_from_list(
            self.accounts, "选择账户"
        )
        
        # 输入交易日期
        transaction_date = input("请输入交易日期 (YYYY-MM-DD): ").strip()
        
        # 输入交易数量
        quantity = float(input("请输入交易数量: ").strip())
        
        # 输入价格
        price = float(input("请输入价格: ").strip())
        
        # 计算成交额
        turnover = quantity * price
        
        # 输入手续费
        fee = float(input("请输入手续费 (0表示无手续费): ").strip() or "0")
        
        # 计算交易金额 (买入为负，卖出为正)
        if type_name == "买入":
            transaction_amount = -(turnover + fee)
        elif type_name == "卖出":
            transaction_amount = turnover - fee
        else:  # 分红/利息
            transaction_amount = turnover - fee
        
        # 输入备注
        notes = input("请输入备注 (可选): ").strip()
        
        # 确认信息
        print("\n请确认交易记录:")
        print(f"股票: {stock_code} - {stock_name}")
        print(f"交易类型: {type_name}")
        print(f"账户: {account_name}")
        print(f"交易日期: {transaction_date}")
        print(f"数量: {quantity}")
        print(f"价格: {price}")
        print(f"成交额: {turnover:.2f}")
        print(f"手续费: {fee:.2f}")
        print(f"交易金额: {transaction_amount:.2f}")
        if notes:
            print(f"备注: {notes}")
        
        confirm = input("\n确认录入? (y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消录入")
            return
        
        # 插入数据
        try:
            self.cursor.execute("""
                INSERT INTO stock_transactions 
                (transaction_date, stock_id, type_transction_id, quantity, price, 
                 turnover, fee, transaction_amount, account_id, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (transaction_date, stock_id, type_transction_id, quantity, price,
                  turnover, fee, transaction_amount, account_id, notes or None))
            
            self.conn.commit()
            trans_id = self.cursor.lastrowid
            print(f"✅ 股票交易记录录入成功! ID: {trans_id}")
                
        except Exception as e:
            print(f"❌ 录入失败: {e}")
            self.conn.rollback()
    
    def insert_fund_nav(self, fund_id=None):
        """录入基金净值"""
        print("\n" + "="*50)
        print("录入基金净值")
        print("="*50)
        
        if not fund_id:
            # 选择基金
            funds = self.cursor.execute("SELECT id, code, name FROM fund ORDER BY code").fetchall()
            if not funds:
                print("没有可用的基金记录")
                return
                
            print("\n选择基金:")
            print("-"*50)
            for idx, fund in enumerate(funds, 1):
                print(f"{idx}. {fund['code']} - {fund['name']}")
            
            try:
                choice = int(input(f"\n请选择基金 (1-{len(funds)}): "))
                if 1 <= choice <= len(funds):
                    fund_id = funds[choice-1]['id']
                    fund_code = funds[choice-1]['code']
                    fund_name = funds[choice-1]['name']
                else:
                    print("选择无效")
                    return
            except ValueError:
                print("请输入有效的数字")
                return
        else:
            fund = self.cursor.execute("SELECT code, name FROM fund WHERE id = ?", (fund_id,)).fetchone()
            fund_code = fund['code']
            fund_name = fund['name']
        
        # 输入日期
        date = input("请输入净值日期 (YYYY-MM-DD): ").strip()
        
        # 输入净值
        nav = float(input("请输入净值: ").strip())
        
        # 确认信息
        print("\n请确认净值信息:")
        print(f"基金: {fund_code} - {fund_name}")
        print(f"日期: {date}")
        print(f"净值: {nav}")
        
        confirm = input("\n确认录入? (y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消录入")
            return
        
        # 插入数据
        try:
            self.cursor.execute("""
                INSERT INTO fund_net_asset_value (fund_id, date, nav)
                VALUES (?, ?, ?)
            """, (fund_id, date, nav))
            
            self.conn.commit()
            nav_id = self.cursor.lastrowid
            print(f"✅ 基金净值录入成功! ID: {nav_id}")
                
        except Exception as e:
            print(f"❌ 录入失败: {e}")
            self.conn.rollback()
    
    def insert_stock_nav(self, stock_id=None):
        """录入股票净值"""
        print("\n" + "="*50)
        print("录入股票净值")
        print("="*50)
        
        if not stock_id:
            # 选择股票
            stocks = self.cursor.execute("SELECT id, code, name FROM stock ORDER BY code").fetchall()
            if not stocks:
                print("没有可用的股票记录")
                return
                
            print("\n选择股票:")
            print("-"*50)
            for idx, stock in enumerate(stocks, 1):
                print(f"{idx}. {stock['code']} - {stock['name']}")
            
            try:
                choice = int(input(f"\n请选择股票 (1-{len(stocks)}): "))
                if 1 <= choice <= len(stocks):
                    stock_id = stocks[choice-1]['id']
                    stock_code = stocks[choice-1]['code']
                    stock_name = stocks[choice-1]['name']
                else:
                    print("选择无效")
                    return
            except ValueError:
                print("请输入有效的数字")
                return
        else:
            stock = self.cursor.execute("SELECT code, name FROM stock WHERE id = ?", (stock_id,)).fetchone()
            stock_code = stock['code']
            stock_name = stock['name']
        
        # 输入日期
        date = input("请输入净值日期 (YYYY-MM-DD): ").strip()
        
        # 输入净值
        nav = float(input("请输入净值: ").strip())
        
        # 确认信息
        print("\n请确认净值信息:")
        print(f"股票: {stock_code} - {stock_name}")
        print(f"日期: {date}")
        print(f"净值: {nav}")
        
        confirm = input("\n确认录入? (y/n): ").lower().strip()
        if confirm != 'y':
            print("已取消录入")
            return
        
        # 插入数据
        try:
            self.cursor.execute("""
                INSERT INTO stock_net_asset_value (stock_id, date, nav)
                VALUES (?, ?, ?)
            """, (stock_id, date, nav))
            
            self.conn.commit()
            nav_id = self.cursor.lastrowid
            print(f"✅ 股票净值录入成功! ID: {nav_id}")
                
        except Exception as e:
            print(f"❌ 录入失败: {e}")
            self.conn.rollback()
    
    def run(self):
        """运行主程序"""
        print("投资数据录入系统已启动...")
        
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                self.insert_fund()
            elif choice == '2':
                self.insert_stock()
            elif choice == '3':
                self.insert_fund_transaction()
            elif choice == '4':
                self.insert_stock_transaction()
            elif choice == '5':
                self.insert_fund_nav()
            elif choice == '6':
                self.insert_stock_nav()
            elif choice == '7':
                print("感谢使用，再见!")
                break
            else:
                print("无效的选择，请重新输入")
            
            input("\n按回车键继续...")
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()

def main():
    # 检查数据库是否存在，如果不存在则创建
    import os
    if not os.path.exists('property.db'):
        print("警告: 数据库文件不存在!")
        create_db = input("是否从SQL文件创建数据库? (y/n): ").lower().strip()
        if create_db == 'y':
            try:
                # 读取SQL文件并创建数据库
                with open('property.db.sql', 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                conn = sqlite3.connect('property.db')
                conn.executescript(sql_content)
                conn.close()
                print("✅ 数据库创建成功!")
            except Exception as e:
                print(f"❌ 数据库创建失败: {e}")
                return
        else:
            print("请确保数据库文件存在")
            return
    
    # 运行程序
    app = InvestmentDataEntry('property.db')
    try:
        app.run()
    finally:
        app.close()

if __name__ == "__main__":
    main()