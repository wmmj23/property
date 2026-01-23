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
    
    def ask_for_us_data_source(self, function_name: str) -> bool:
        """询问用户选择美股数据源"""
        print(f"\n{function_name} - 选择美股数据源")
        print("-" * 40)
        
        data_source_manager = get_data_source_manager()
        return data_source_manager.select_us_data_source_interactive()
    
    def handle_choice(self, choice: str):
        """处理用户选择"""
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
        elif choice == "6":
            view_stock_info.main(self.db)
        elif choice == "7":
            view_fund_info.main(self.db)
        elif choice == "8":
            view_exchange_info.main(self.db)
        elif choice == "9":
            database_management.main(self.db)
        elif choice == "0":
            self.exit_program()
        else:
            print_error("无效的选择")
    
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