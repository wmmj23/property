# menu_functions/view_fund_info.py
import logging
from database import get_database
from utils import (
    print_header, print_warning, print_error, 
    safe_format, print_table, clear_screen
)

logger = logging.getLogger(__name__)


def _display_fund_detail(db, fund_info: dict):
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
    latest_nav = db.get_latest_fund_nav(fund_id)
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


def view_fund_info_function(db):
    """查看基金信息"""
    print_header("查看基金信息")
    
    funds = db.get_all_funds()
    
    if not funds:
        print_warning("未找到基金信息")
        input("\n按回车键返回...")
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
        
        # 获取最新净值
        latest_nav = db.get_latest_fund_nav(fund_id)
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
        print("3. 返回")
        
        choice = input("\n请选择 (1-3): ").strip()
        
        if choice == "1":
            fund_code = input("请输入基金代码: ").strip()
            fund_info = db.get_fund_by_code(fund_code)
            
            if fund_info:
                _display_fund_detail(db, fund_info)
                clear_screen()
                # 重新显示列表
                print_header("查看基金信息")
                print_table(headers, rows, [10, 30, 15, 12])
                print("-" * 70)
            else:
                print_error(f"未找到基金代码为 {fund_code} 的基金")
        elif choice == "2":
            return view_fund_info_function(db)  # 递归刷新
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
        view_fund_info_function(db)
    except Exception as e:
        logger.error(f"查看基金信息失败: {e}")
        print_error(f"查看基金信息失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()