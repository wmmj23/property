# menu.py 
import logging
from typing import Optional, List, Dict, Any

from utils import (
    clear_screen, print_header, print_success, 
    print_error, print_warning, print_info,
    get_user_choice, confirm_action, safe_format,
    print_table, format_number
)
from fetcher import DataFetcher
from database import get_database

logger = logging.getLogger(__name__)


class MenuSystem:
    """菜单系统"""
    
    def __init__(self):
        self.db = get_database()
        self.fetcher = DataFetcher()
        self.running = True
    
    def display_main_menu(self):
        """显示主菜单"""
        clear_screen()
        print_header("个人资产数据管理系统")
        
        print("\n请选择功能:")
        print("1. 获取股票最新收盘价")
        print("2. 获取基金最新净值")
        print("3. 获取最新汇率")
        print("4. 获取美股数据")
        print("5. 一键更新所有数据")
        print("6. 查看股票信息")
        print("7. 查看基金信息")
        print("8. 查看汇率信息")
        print("9. 数据库管理")
        print("0. 退出程序")
        
        print("\n" + "-" * 40)
    
    def handle_choice(self, choice: str):
        """处理用户选择"""
        if choice == "1":
            self.fetch_stock_prices()
        elif choice == "2":
            self.fetch_fund_navs()
        elif choice == "3":
            self.fetch_exchange_rates()
        elif choice == "4":
            self.fetch_us_stocks()
        elif choice == "5":
            self.fetch_all_data()
        elif choice == "6":
            self.view_stock_info()
        elif choice == "7":
            self.view_fund_info()
        elif choice == "8":
            self.view_exchange_info()
        elif choice == "9":
            self.database_management()
        elif choice == "0":
            self.exit_program()
        else:
            print_error("无效的选择")
    
    def fetch_stock_prices(self):
        """获取股票价格"""
        print_header("获取股票最新收盘价")
        
        if confirm_action("确定要获取所有股票的最新收盘价吗？"):
            success, failure, failed_items = self.fetcher.fetch_stock_prices()
            
            print("\n" + "-" * 40)
            print(f"获取完成: 成功 {success} 只, 失败 {failure} 只")
            
            if failed_items:
                print("\n失败的股票:")
                for stock in failed_items:
                    print(f"  {stock.get('name')}({stock.get('code')})")
        
        input("\n按回车键返回主菜单...")
    
    def fetch_fund_navs(self):
        """获取基金净值"""
        print_header("获取基金最新净值")
        
        if confirm_action("确定要获取所有基金的最新净值吗？"):
            success, failure, failed_items = self.fetcher.fetch_fund_navs()
            
            print("\n" + "-" * 40)
            print(f"获取完成: 成功 {success} 只, 失败 {failure} 只")
            
            if failed_items:
                print("\n失败的基金:")
                for fund in failed_items:
                    print(f"  {fund.get('name')}({fund.get('code')})")
        
        input("\n按回车键返回主菜单...")
    
    def fetch_exchange_rates(self):
        """获取汇率"""
        print_header("获取最新汇率")
        
        if confirm_action("确定要获取所有货币的最新汇率吗？"):
            success, failure, failed_items = self.fetcher.fetch_exchange_rates()
            
            print("\n" + "-" * 40)
            print(f"获取完成: 成功 {success} 种, 失败 {failure} 种")
            
            if failed_items:
                print("\n失败的货币:")
                for currency in failed_items:
                    print(f"  {currency.get('currency')}")
        
        input("\n按回车键返回主菜单...")
    
    def fetch_us_stocks(self):
        """获取美股数据"""
        print_header("获取美股数据")
        
        if confirm_action("确定要获取所有美股的最新数据吗？"):
            success, failure, failed_items = self.fetcher.fetch_us_stocks_only()
            
            print("\n" + "-" * 40)
            print(f"获取完成: 成功 {success} 只, 失败 {failure} 只")
            
            if failed_items:
                print("\n失败的股票:")
                for stock in failed_items:
                    print(f"  {stock.get('name')}({stock.get('code')})")
        
        input("\n按回车键返回主菜单...")
    
    def fetch_all_data(self):
        """一键更新所有数据"""
        print_header("一键更新所有数据")
        
        if confirm_action("确定要一键更新所有数据吗？这可能需要几分钟"):
            results = self.fetcher.fetch_all_data()
            
            # 显示失败详情
            if results['stocks']['failure'] > 0:
                print("\n失败的股票:")
                for stock in results['stocks']['failed_items']:
                    print(f"  {stock.get('name')}({stock.get('code')})")
            
            if results['funds']['failure'] > 0:
                print("\n失败的基金:")
                for fund in results['funds']['failed_items']:
                    print(f"  {fund.get('name')}({fund.get('code')})")
        
        input("\n按回车键返回主菜单...")
    
    def view_stock_info(self):
        """查看股票信息"""
        print_header("查看股票信息")
        
        stocks = self.db.get_all_stocks()
        
        if not stocks:
            print_warning("未找到股票信息")
            input("\n按回车键返回主菜单...")
            return
        
        print(f"共找到 {len(stocks)} 只股票:")
        print("-" * 80)
        
        # 准备表格数据
        headers = ["代码", "名称", "市场", "最新净值", "日期"]
        rows = []
        
        for stock in stocks:
            code = stock.get('code', 'N/A')
            name = stock.get('name', 'N/A')
            market = stock.get('market_code', 'N/A')
            stock_id = stock.get('id')
            
            # 获取最新净值
            latest_nav = self.db.get_latest_stock_nav(stock_id)
            nav = latest_nav.get('nav') if latest_nav else None
            date = latest_nav.get('date') if latest_nav else None
            
            # 使用安全格式化
            nav_str = safe_format(nav, "{:.4f}", "N/A")
            date_str = safe_format(date, "{}", "N/A")
            
            rows.append([code, name, market, nav_str, date_str])
        
        # 使用新的表格打印函数
        print_table(headers, rows, [10, 25, 10, 15, 12])
        
        print("-" * 80)
        
        # 提供详细查看选项
        while True:
            print("\n操作:")
            print("1. 查看特定股票详情")
            print("2. 刷新列表")
            print("3. 返回主菜单")
            
            choice = input("\n请选择 (1-3): ").strip()
            
            if choice == "1":
                stock_code = input("请输入股票代码: ").strip()
                stock_info = self.db.get_stock_by_code(stock_code)
                
                if stock_info:
                    self._display_stock_detail(stock_info)
                else:
                    print_error(f"未找到股票代码为 {stock_code} 的股票")
            elif choice == "2":
                return self.view_stock_info()  # 递归刷新
            elif choice == "3":
                break
            else:
                print_error("无效选择")
    
    def _display_stock_detail(self, stock_info: dict):
        """显示股票详情"""
        stock_id = stock_info.get('id')
        code = stock_info.get('code', 'N/A')
        name = stock_info.get('name', 'N/A')
        
        print_header(f"股票详情 - {name} ({code})")
        
        # 基本信息
        print("\n基本信息:")
        print(f"  股票代码: {safe_format(code)}")
        print(f"  股票名称: {safe_format(name)}")
        print(f"  所属市场: {safe_format(stock_info.get('market_name'))}")
        print(f"  市场代码: {safe_format(stock_info.get('market_code'))}")
        
        # 最新净值信息
        latest_nav = self.db.get_latest_stock_nav(stock_id)
        if latest_nav:
            print("\n最新净值信息:")
            nav = latest_nav.get('nav')
            date = latest_nav.get('date')
            print(f"  最新净值: {safe_format(nav, '{:.4f}', 'N/A')}")
            print(f"  净值日期: {safe_format(date)}")
        else:
            print_warning("\n暂无净值数据")
        
        print("\n" + "-" * 40)
        input("按回车键继续...")
    
    def view_fund_info(self):
        """查看基金信息"""
        print_header("查看基金信息")
        
        funds = self.db.get_all_funds()
        
        if not funds:
            print_warning("未找到基金信息")
            input("\n按回车键返回主菜单...")
            return
        
        print(f"共找到 {len(funds)} 只基金:")
        print("-" * 70)
        
        # 准备表格数据
        headers = ["代码", "名称", "最新净值", "日期"]
        rows = []
        
        for fund in funds:
            code = fund.get('code', 'N/A')
            name = fund.get('name', 'N/A')
            fund_id = fund.get('id')
            
            # 获取最新净值（需要添加此方法到database.py）
            latest_nav = self.db.get_latest_fund_nav(fund_id)
            nav = latest_nav.get('nav') if latest_nav else None
            date = latest_nav.get('date') if latest_nav else None
            
            # 限制名称长度
            display_name = name
            if display_name and len(display_name) > 25:
                display_name = display_name[:22] + "..."
            
            rows.append([
                code,
                display_name or 'N/A',
                safe_format(nav, "{:.4f}", "N/A"),
                safe_format(date, "{}", "N/A")
            ])
        
        print_table(headers, rows, [10, 30, 15, 12])
        
        print("-" * 70)
        
        # 提供详细查看选项
        while True:
            print("\n操作:")
            print("1. 查看特定基金详情")
            print("2. 刷新列表")
            print("3. 返回主菜单")
            
            choice = input("\n请选择 (1-3): ").strip()
            
            if choice == "1":
                fund_code = input("请输入基金代码: ").strip()
                fund_info = self.db.get_fund_by_code(fund_code)
                
                if fund_info:
                    self._display_fund_detail(fund_info)
                else:
                    print_error(f"未找到基金代码为 {fund_code} 的基金")
            elif choice == "2":
                return self.view_fund_info()  # 递归刷新
            elif choice == "3":
                break
            else:
                print_error("无效选择")
    
    def _display_fund_detail(self, fund_info: dict):
        """显示基金详情"""
        fund_id = fund_info.get('id')
        code = fund_info.get('code', 'N/A')
        name = fund_info.get('name', 'N/A')
        
        print_header(f"基金详情 - {name} ({code})")
        
        # 基本信息
        print("\n基本信息:")
        print(f"  基金代码: {safe_format(code)}")
        print(f"  基金名称: {safe_format(name)}")
        print(f"  所属市场: {safe_format(fund_info.get('market_name'))}")
        print(f"  市场代码: {safe_format(fund_info.get('market_code'))}")
        
        # 最新净值信息
        latest_nav = self.db.get_latest_fund_nav(fund_id)
        if latest_nav:
            print("\n最新净值信息:")
            nav = latest_nav.get('nav')
            date = latest_nav.get('date')
            print(f"  最新净值: {safe_format(nav, '{:.4f}', 'N/A')}")
            print(f"  净值日期: {safe_format(date)}")
        else:
            print_warning("\n暂无净值数据")
        
        print("\n" + "-" * 40)
        input("按回车键继续...")
    
    def view_exchange_info(self):
        """查看汇率信息"""
        print_header("查看汇率信息")
        
        currencies = self.db.get_all_currencies()
        
        if not currencies:
            print_warning("未找到货币信息")
            input("\n按回车键返回主菜单...")
            return
        
        print(f"共找到 {len(currencies)} 种货币:")
        print("-" * 50)
        
        # 准备表格数据
        headers = ["货币", "最新汇率", "日期"]
        rows = []
        
        for currency in currencies:
            currency_code = currency.get('currency', 'N/A')
            currency_id = currency.get('id')
            
            # 使用 database.py 中的方法获取最新汇率
            latest_rate = self.db.get_latest_exchange_rate(currency_id)
            rate = latest_rate.get('rate') if latest_rate else None
            date = latest_rate.get('date') if latest_rate else None
            
            rows.append([
                currency_code,
                safe_format(rate, "{:.4f}", "N/A"),
                safe_format(date, "{}", "N/A")
            ])
        
        print_table(headers, rows, [10, 15, 12])
        
        print("-" * 50)
        
        # 提供详细查看选项
        while True:
            print("\n操作:")
            print("1. 查看特定货币详情")
            print("2. 刷新列表")
            print("3. 返回主菜单")
            
            choice = input("\n请选择 (1-3): ").strip()
            
            if choice == "1":
                currency_code = input("请输入货币代码 (如 USD): ").strip().upper()
                currency_info = self.db.get_currency_by_code(currency_code)
                
                if currency_info:
                    self._display_currency_detail(currency_info)
                else:
                    print_error(f"未找到货币代码为 {currency_code} 的货币")
            elif choice == "2":
                return self.view_exchange_info()  # 递归刷新
            elif choice == "3":
                break
            else:
                print_error("无效选择")
    
    def _display_currency_detail(self, currency_info: dict):
        """显示货币详情"""
        currency_id = currency_info.get('id')
        currency_code = currency_info.get('currency', 'N/A')
        
        print_header(f"货币详情 - {currency_code}")
        
        # 基本信息
        print("\n基本信息:")
        print(f"  货币代码: {safe_format(currency_code)}")
        
        # 最新汇率信息
        latest_rate = self.db.get_latest_exchange_rate(currency_id)
        if latest_rate:
            print("\n最新汇率信息:")
            rate = latest_rate.get('rate')
            date = latest_rate.get('date')
            print(f"  最新汇率: 1{currency_code} = {safe_format(rate, '{:.4f}', 'N/A')} CNY")
            print(f"  汇率日期: {safe_format(date)}")
        else:
            print_warning("\n暂无汇率数据")
        
        print("\n" + "-" * 40)
        input("按回车键继续...")
    
    def database_management(self):
        """数据库管理"""
        print_header("数据库管理")
        
        print("\n请选择操作:")
        print("1. 备份数据库")
        print("2. 查看数据库状态")
        print("3. 返回主菜单")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            if confirm_action("确定要备份数据库吗？"):
                if self.db.backup():
                    print_success("数据库备份成功")
                else:
                    print_error("数据库备份失败")
            input("\n按回车键继续...")
        elif choice == "2":
            self._show_database_status()
        elif choice == "3":
            return
        else:
            print_error("无效选择")
            input("\n按回车键继续...")
    
    def _show_database_status(self):
        """显示数据库状态"""
        print_header("数据库状态")
        
        # 检查表数量
        try:
            self.db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.db.cursor.fetchall()
            print(f"数据库表数量: {len(tables)}")
            
            # 主要表数据量
            tables_to_check = [
                'stock', 'fund', 'stock_net_asset_value', 
                'fund_net_asset_value', 'foreign_exchange_rate'
            ]
            
            print("\n表数据统计:")
            for table in tables_to_check:
                self.db.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
                result = self.db.cursor.fetchone()
                if result:
                    print(f"  {table}: {result['count']} 条记录")
            
            # 数据库文件大小
            import os
            if os.path.exists(self.db.db_file):
                size = os.path.getsize(self.db.db_file)
                size_mb = size / (1024 * 1024)
                print(f"\n数据库文件大小: {size_mb:.2f} MB")
            
        except Exception as e:
            print_error(f"获取数据库状态失败: {e}")
        
        input("\n按回车键继续...")
    
    def exit_program(self):
        """退出程序"""
        print_header("退出程序")
        
        if confirm_action("确定要退出程序吗？"):
            self.running = False
            print_success("程序已退出")
        else:
            print_info("取消退出")
            input("\n按回车键返回主菜单...")
    
    def run(self):
        """运行菜单系统"""
        print_success("程序启动成功")
        
        # 连接数据库
        if not self.db.connect():
            print_error("无法连接数据库，请检查数据库文件")
            return
        
        try:
            while self.running:
                self.display_main_menu()
                choice = input("请选择功能 (0-9): ").strip()
                self.handle_choice(choice)
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
        except Exception as e:
            print_error(f"程序运行出错: {e}")
            import traceback
            traceback.print_exc()
            input("\n按回车键退出...")
        finally:
            self.db.close()
            print_info("数据库连接已关闭")