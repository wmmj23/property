# menu_functions/fetch_stock_prices.py
import logging
from database import get_database
from fetcher import DataFetcher
from utils import print_header, confirm_action, print_error, print_warning, print_info

logger = logging.getLogger(__name__)


def fetch_stock_prices_function(db, fetcher):
    """获取股票价格"""
    print_header("获取股票最新收盘价")
    
    if confirm_action("确定要获取所有股票的最新收盘价吗？"):
        success, failure, failed_items = fetcher.fetch_stock_prices()
        
        print("\n" + "-" * 40)
        print(f"获取完成: 成功 {success} 只, 失败 {failure} 只")
        
        if failed_items:
            print("\n失败的股票:")
            for stock in failed_items:
                print(f"  {stock.get('name')}({stock.get('code')})")
    
    input("\n按回车键返回主菜单...")


def main(db=None):
    """主函数，可以独立运行"""
    # 如果db没有传入，则创建新的连接
    if db is None:
        db = get_database()
        if not db.connect():
            print_error("无法连接数据库，请检查数据库文件")
            return
        close_db = True
    else:
        close_db = False
    
    try:
        fetcher = DataFetcher()
        fetch_stock_prices_function(db, fetcher)
    except Exception as e:
        logger.error(f"获取股票价格失败: {e}")
        print_error(f"获取股票价格失败: {e}")
    finally:
        if close_db:
            db.close()


if __name__ == "__main__":
    main()