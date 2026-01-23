# menu_functions/fetch_us_stocks.py
import logging
from database import get_database
from fetcher import DataFetcher
from utils import print_header, confirm_action, print_error

logger = logging.getLogger(__name__)


def fetch_us_stocks_function(db, fetcher):
    """获取美股数据"""
    print_header("获取美股数据")
    
    if confirm_action("确定要获取所有美股的最新数据吗？"):
        success, failure, failed_items = fetcher.fetch_us_stocks_only()
        
        print("\n" + "-" * 40)
        print(f"获取完成: 成功 {success} 只, 失败 {failure} 只")
        
        if failed_items:
            print("\n失败的股票:")
            for stock in failed_items:
                print(f"  {stock.get('name')}({stock.get('code')})")
    
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
        fetch_us_stocks_function(db, fetcher)
    except Exception as e:
        logger.error(f"获取美股数据失败: {e}")
        print_error(f"获取美股数据失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()