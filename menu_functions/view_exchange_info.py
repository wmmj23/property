# menu_functions/view_exchange_info.py
import logging
from database import get_database
from utils import (
    print_header, print_warning, print_error, 
    safe_format, print_table, clear_screen
)

logger = logging.getLogger(__name__)


def _display_currency_detail(db, currency_info: dict):
    """显示货币详情"""
    currency_id = currency_info.get('id')
    currency_code = currency_info.get('currency', 'N/A')
    
    print_header(f"货币详情 - {currency_code}")
    
    # 基本信息
    print("\n基本信息:")
    print(f"  货币代码: {safe_format(currency_code)}")
    
    # 最新汇率信息
    latest_rate = db.get_latest_exchange_rate(currency_id)
    if latest_rate:
        print("\n最新汇率信息:")
        rate = latest_rate.get('rate')
        date = latest_rate.get('date')
        print(f"  最新汇率: 1{currency_code} = {safe_format(rate, '{:.4f}', 'N/A')} CNY")
        print(f"  汇率日期: {safe_format(date)}")
    else:
        print("\n暂无汇率数据")
    
    print("\n" + "-" * 40)
    input("按回车键继续...")


def view_exchange_info_function(db):
    """查看汇率信息"""
    print_header("查看汇率信息")
    
    currencies = db.get_all_currencies()
    
    if not currencies:
        print_warning("未找到货币信息")
        input("\n按回车键返回...")
        return
    
    print(f"共找到 {len(currencies)} 种货币:")
    print("-" * 50)
    
    # 准备表格数据
    headers = ["货币", "最新汇率", "日期"]
    rows = []
    
    for currency in currencies:
        currency_code = currency.get('currency', 'N/A')
        currency_id = currency.get('id')
        
        # 获取最新汇率
        latest_rate = db.get_latest_exchange_rate(currency_id)
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
        print("3. 返回")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            currency_code = input("请输入货币代码 (如 USD): ").strip().upper()
            currency_info = db.get_currency_by_code(currency_code)
            
            if currency_info:
                _display_currency_detail(db, currency_info)
                clear_screen()
                # 重新显示列表
                print_header("查看汇率信息")
                print_table(headers, rows, [10, 15, 12])
                print("-" * 50)
            else:
                print_error(f"未找到货币代码为 {currency_code} 的货币")
        elif choice == "2":
            return view_exchange_info_function(db)  # 递归刷新
        elif choice == "3":
            break
        else:
            print_error("无效选择")


def main(db=None):
    """主函数，可以独立运行"""
    if db is None:
        db = get_database()
    if not db.connect():
            print_error("无法连接数据库，请检查数据库文件")
            return
    close_db = True
    
    try:
        view_exchange_info_function(db)
    except Exception as e:
        logger.error(f"查看汇率信息失败: {e}")
        print_error(f"查看汇率信息失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()