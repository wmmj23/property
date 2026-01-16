# menu_functions/database_management.py
import logging
import os
from database import get_database
from utils import (
    print_header, print_success, print_error, 
    print_warning, print_info, confirm_action
)

logger = logging.getLogger(__name__)


def _show_database_status(db):
    """显示数据库状态"""
    print_header("数据库状态")
    
    # 检查表数量
    try:
        db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = db.cursor.fetchall()
        print(f"数据库表数量: {len(tables)}")
        
        # 主要表数据量
        tables_to_check = [
            'stock', 'fund', 'stock_net_asset_value', 
            'fund_net_asset_value', 'foreign_exchange_rate'
        ]
        
        print("\n表数据统计:")
        for table in tables_to_check:
            db.cursor.execute(f"SELECT COUNT(*) as count FROM {table}")
            result = db.cursor.fetchone()
            if result:
                print(f"  {table}: {result['count']} 条记录")
        
        # 数据库文件大小
        if os.path.exists(db.db_file):
            size = os.path.getsize(db.db_file)
            size_mb = size / (1024 * 1024)
            print(f"\n数据库文件大小: {size_mb:.2f} MB")
        
    except Exception as e:
        print_error(f"获取数据库状态失败: {e}")
    
    input("\n按回车键继续...")


def database_management_function(db):
    """数据库管理"""
    print_header("数据库管理")
    
    print("\n请选择操作:")
    print("1. 备份数据库")
    print("2. 查看数据库状态")
    print("3. 返回")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    if choice == "1":
        if confirm_action("确定要备份数据库吗？"):
            if db.backup():
                print_success("数据库备份成功")
            else:
                print_error("数据库备份失败")
        input("\n按回车键继续...")
    elif choice == "2":
        _show_database_status(db)
    elif choice == "3":
        return
    else:
        print_error("无效选择")
        input("\n按回车键继续...")


def main(db=None):
    """主函数，可以独立运行"""
    if db is None:
        db = get_database()
        if not db.connect():
            print_error("无法连接数据库，请检查数据库文件")
            return
        close_db = True
    else:
        close_db = False
    
    try:
        database_management_function(db)
    except Exception as e:
        logger.error(f"数据库管理失败: {e}")
        print_error(f"数据库管理失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()