# menu.py - 主菜单文件
import logging
from typing import Optional, List, Dict, Any

from utils import (
    clear_screen, print_header, print_success, 
    print_error, print_warning, print_info,
    get_user_choice, confirm_action
)
from database import get_database
from menu_functions import (
    fetch_stock_prices, fetch_fund_navs, fetch_exchange_rates,
    fetch_us_stocks, fetch_all_data, view_stock_info,
    view_fund_info, view_exchange_info, database_management
)
from data_sources.data_source_manager import get_data_source_manager

logger = logging.getLogger(__name__)


class MenuSystem:
    """菜单系统"""
    
    def __init__(self):
        self.db = get_database()
        self.running = True
        self.current_menu = "main"  # 当前菜单状态：main, update, query, settings
    
    def display_main_menu(self):
        """显示主菜单"""
        clear_screen()
        print_header("个人资产数据管理系统")
        
        print("\n请选择功能:")
        print("1. 更新数据")
        print("2. 查询数据")
        print("3. 参数设置")
        print("0. 退出程序")
        
        print("\n" + "-" * 40)
    
    def display_update_menu(self):
        """显示更新数据菜单"""
        clear_screen()
        print_header("更新数据")
        
        print("\n请选择要更新的数据:")
        print("1. 获取股票最新收盘价")
        print("2. 获取基金最新净值")
        print("3. 获取最新汇率")
        print("4. 获取美股数据")
        print("5. 一键更新所有数据")
        print("0. 返回主菜单")
        
        print("\n" + "-" * 40)
    
    def display_query_menu(self):
        """显示查询数据菜单"""
        clear_screen()
        print_header("查询数据")
        
        print("\n请选择要查询的数据:")
        print("1. 查看股票信息")
        print("2. 查看基金信息")
        print("3. 查看汇率信息")
        print("0. 返回主菜单")
        
        print("\n" + "-" * 40)
    
    def display_settings_menu(self):
        """显示参数设置菜单"""
        clear_screen()
        print_header("参数设置")
        
        print("\n请选择设置项:")
        print("1. 数据库管理")
        print("0. 返回主菜单")
        
        print("\n" + "-" * 40)
    
    def ask_for_us_data_source(self, function_name: str) -> bool:
        """询问用户选择美股数据源"""
        print(f"\n{function_name} - 选择美股数据源")
        print("-" * 40)
        
        data_source_manager = get_data_source_manager()
        return data_source_manager.select_us_data_source_interactive()
    
    def handle_main_menu_choice(self, choice: str):
        """处理主菜单选择"""
        if choice == "1":
            self.current_menu = "update"
        elif choice == "2":
            self.current_menu = "query"
        elif choice == "3":
            self.current_menu = "settings"
        elif choice == "0":
            self.exit_program()
        else:
            print_error("无效的选择")
            input("\n按回车键继续...")
    
    def handle_update_menu_choice(self, choice: str):
        """处理更新数据菜单选择"""
        if choice == "1":
            # 获取股票数据前先询问美股数据源
            if self.ask_for_us_data_source("获取股票最新收盘价"):
                fetch_stock_prices.main(self.db)
        elif choice == "2":
            # 获取基金数据前先询问美股数据源
            if self.ask_for_us_data_source("获取基金最新净值"):
                fetch_fund_navs.main(self.db)
        elif choice == "3":
            # 获取汇率数据前先询问美股数据源
            if self.ask_for_us_data_source("获取最新汇率"):
                fetch_exchange_rates.main(self.db)
        elif choice == "4":
            # 获取美股数据前先询问美股数据源
            if self.ask_for_us_data_source("获取美股数据"):
                fetch_us_stocks.main(self.db)
        elif choice == "5":
            # 一键更新所有数据前先询问美股数据源
            if self.ask_for_us_data_source("一键更新所有数据"):
                fetch_all_data.main(self.db)
        elif choice == "0":
            self.current_menu = "main"
        else:
            print_error("无效的选择")
            input("\n按回车键继续...")
    
    def handle_query_menu_choice(self, choice: str):
        """处理查询数据菜单选择"""
        if choice == "1":
            view_stock_info.main(self.db)
        elif choice == "2":
            view_fund_info.main(self.db)
        elif choice == "3":
            view_exchange_info.main(self.db)
        elif choice == "0":
            self.current_menu = "main"
        else:
            print_error("无效的选择")
            input("\n按回车键继续...")
    
    def handle_settings_menu_choice(self, choice: str):
        """处理参数设置菜单选择"""
        if choice == "1":
            database_management.main(self.db)
        elif choice == "0":
            self.current_menu = "main"
        else:
            print_error("无效的选择")
            input("\n按回车键继续...")
    
    def handle_choice(self, choice: str):
        """根据当前菜单状态处理用户选择"""
        if self.current_menu == "main":
            self.handle_main_menu_choice(choice)
        elif self.current_menu == "update":
            self.handle_update_menu_choice(choice)
        elif self.current_menu == "query":
            self.handle_query_menu_choice(choice)
        elif self.current_menu == "settings":
            self.handle_settings_menu_choice(choice)
    
    def exit_program(self):
        """退出程序"""
        print_header("退出程序")
        
        if confirm_action("确定要退出程序吗？"):
            self.running = False
            print_success("程序已退出")
        else:
            print_info("取消退出")
    
    def run(self):
        """运行菜单系统"""
        print_success("程序启动成功")
        
        # 连接数据库
        if not self.db.connect():
            print_error("无法连接数据库，请检查数据库文件")
            return
        
        try:
            while self.running:
                # 根据当前菜单状态显示不同的菜单
                if self.current_menu == "main":
                    self.display_main_menu()
                elif self.current_menu == "update":
                    self.display_update_menu()
                elif self.current_menu == "query":
                    self.display_query_menu()
                elif self.current_menu == "settings":
                    self.display_settings_menu()
                
                # 获取用户输入
                if self.current_menu == "main":
                    choice = input("请选择功能 (0-3): ").strip()
                elif self.current_menu == "update":
                    choice = input("请选择更新选项 (0-5): ").strip()
                elif self.current_menu == "query":
                    choice = input("请选择查询选项 (0-3): ").strip()
                elif self.current_menu == "settings":
                    choice = input("请选择设置选项 (0-1): ").strip()
                
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