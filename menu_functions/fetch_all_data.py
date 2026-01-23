# menu_functions/fetch_all_data.py
import logging
from database import get_database
from fetcher import DataFetcher
from utils import print_header, confirm_action, print_error

logger = logging.getLogger(__name__)


def fetch_all_data_function(db, fetcher):
    """一键更新所有数据"""
    print_header("一键更新所有数据")
    
    if confirm_action("确定要一键更新所有数据吗？这可能需要几分钟"):
        results = fetcher.fetch_all_data()
        
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


def main(db=None):
    """主函数，可以独立运行"""
    if db is None:
        db = get_database()
    if not db.connect():
            print_error("无法连接数据库，请检查数据库文件")
            return
    close_db = True
    
    try:
        fetcher = DataFetcher()
        fetch_all_data_function(db, fetcher)
    except Exception as e:
        logger.error(f"一键更新数据失败: {e}")
        print_error(f"一键更新数据失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()