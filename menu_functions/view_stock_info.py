# menu_functions/view_stock_info.py
import logging
from database import get_database
from utils import (
    print_header, print_warning, print_error, 
    safe_format, print_table, clear_screen
)

logger = logging.getLogger(__name__)


def _display_stock_detail(db, stock_info: dict):
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
    latest_nav = db.get_latest_stock_nav(stock_id)
    if latest_nav:
        print("\n最新净值信息:")
        nav = latest_nav.get('nav')
        date = latest_nav.get('date')
        print(f"  最新净值: {safe_format(nav, '{:.4f}', 'N/A')}")
        print(f"  净值日期: {safe_format(date)}")
    else:
        print("\n暂无净值数据")
    
    print("\n" + "-" * 40)
    input("按回车键继续...")


def view_stock_info_function(db):
    """查看股票信息"""
    print_header("查看股票信息")
    
    stocks = db.get_all_stocks()
    
    if not stocks:
        print_warning("未找到股票信息")
        input("\n按回车键返回...")
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
        latest_nav = db.get_latest_stock_nav(stock_id)
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
        print("3. 返回")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            stock_code = input("请输入股票代码: ").strip()
            stock_info = db.get_stock_by_code(stock_code)
            
            if stock_info:
                _display_stock_detail(db, stock_info)
                clear_screen()
                # 重新显示列表
                print_header("查看股票信息")
                print_table(headers, rows, [10, 25, 10, 15, 12])
                print("-" * 80)
            else:
                print_error(f"未找到股票代码为 {stock_code} 的股票")
        elif choice == "2":
            return view_stock_info_function(db)  # 递归刷新
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
        view_stock_info_function(db)
    except Exception as e:
        logger.error(f"查看股票信息失败: {e}")
        print_error(f"查看股票信息失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()