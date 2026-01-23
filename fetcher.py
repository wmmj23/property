# fetcher.py
import logging
import time
from typing import Tuple, List, Dict, Any, Optional  # 添加了 Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

#from data_source import get_data_source, HybridDataSource
from database import get_database
from config import DECIMAL_PLACES
from data_sources import get_data_source 


logger = logging.getLogger(__name__)


class DataFetcher:
    """数据获取功能类"""
    
    def __init__(self, max_workers: int = 1):
        self.data_source = get_data_source()  # 获取数据源管理器
        self.max_workers = max_workers
        logger.info(f"数据获取器初始化成功，最大线程数: {max_workers}")
    
    def fetch_stock_prices(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """获取所有股票的最新收盘价"""
        # 在主线程中获取数据
        db = get_database()
        if not db.connect():
            logger.error("无法连接数据库")
            return 0, 0, []
        
        try:
            stocks = db.get_all_stocks()
        finally:
            db.close()
            
        if not stocks:
            logger.warning("未找到任何股票信息")
            return 0, 0, []
        
        success_count = 0
        failure_count = 0
        failed_stocks = []
        
        print(f"\n开始获取 {len(stocks)} 只股票的收盘价...")
        logger.info(f"开始获取 {len(stocks)} 只股票的收盘价")
        
        # 使用线程池并行获取数据，但每个线程使用独立的数据库连接
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for stock in stocks:
                future = executor.submit(self._fetch_single_stock_price_thread, stock)
                futures[future] = stock
            
            for future in as_completed(futures):
                stock = futures[future]
                try:
                    success, price, date = future.result()
                    if success:
                        success_count += 1
                        # 在主线程中保存数据
                        self._save_stock_data_thread_safe(
                            stock['id'], 
                            price, 
                            date, 
                            stock.get('market_code', 'SH'), #默认SH
                            stock['code']  # 添加股票代码参数 - 这是更新部分
                        )
                    else:
                        failure_count += 1
                        failed_stocks.append(stock)
                except Exception as e:
                    logger.error(f"获取股票 {stock.get('code')} 数据时出现异常: {e}")
                    failure_count += 1
                    failed_stocks.append(stock)
        
        logger.info(f"股票获取完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        return success_count, failure_count, failed_stocks
    
    def _fetch_single_stock_price_thread(self, stock: Dict[str, Any]) -> Tuple[bool, Optional[float], Optional[str]]:
        """在线程中获取单只股票价格"""
        code = stock['code']
        name = stock['name']
        market_code = stock.get('market_code', 'SH')
        
        print(f"正在获取 {name}({code}) [{market_code}] 的收盘价...")
        
        # 获取股票价格 - 使用数据源管理器
        price, date = self.data_source.get_stock_price(code, market_code)
        
        if price is not None and date is not None:
            print(f"  √ 获取成功: {date} 收盘价 {price}")
            return True, price, date
        else:
            print(f"  × 获取失败: 无法获取数据")
            return False, None, None
    
    def _save_stock_data_thread_safe(self, stock_id: int, price: float, date: str, market_code: str, code: str):
        """在主线程中安全保存股票数据"""
        db = get_database()
        if not db.connect():
            logger.error(f"保存股票 {stock_id}， {code} 数据时无法连接数据库")
            return False
        
        try:
            if db.insert_stock_nav(stock_id, date, price):
                # 如果是美股，获取详细信息
                # if market_code == "US":
                #     info = self.data_source.get_us_stock_info(code)
                #     if info:
                #         db.update_us_stock_info(stock_id, info)
                #         logger.debug(f"美股 {code} 详细信息已更新")
                return True
            else:
                logger.error(f"保存股票 {stock_id}， {code} 数据失败")
                return False
        finally:
            db.close()
    
    def fetch_us_stocks_only(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """仅获取美股数据"""
        # 在主线程中获取数据
        db = get_database()
        if not db.connect():
            logger.error("无法连接数据库")
            return 0, 0, []
        
        try:
            us_stocks = db.get_us_stocks()
        finally:
            db.close()
            
        if not us_stocks:
            logger.warning("未找到任何美股信息")
            return 0, 0, []
        
        success_count = 0
        failure_count = 0
        failed_stocks = []
        
        print(f"\n开始获取 {len(us_stocks)} 只美股的收盘价...")
        logger.info(f"开始获取 {len(us_stocks)} 只美股的收盘价")
        
        # 使用线程池并行获取数据
        with ThreadPoolExecutor(max_workers=min(2, self.max_workers)) as executor:  # 美股最多使用2个线程
            futures = {}
            for stock in us_stocks:
                future = executor.submit(self._fetch_single_us_stock_price_thread, stock)
                futures[future] = stock
            
            for future in as_completed(futures):
                stock = futures[future]
                try:
                    success, price, date = future.result()
                    if success:
                        success_count += 1
                        # 在主线程中保存数据
                        self._save_us_stock_data_thread_safe(stock['id'], price, date, stock['code'])
                    else:
                        failure_count += 1
                        failed_stocks.append(stock)
                except Exception as e:
                    logger.error(f"获取美股 {stock.get('code')} 数据时出现异常: {e}")
                    failure_count += 1
                    failed_stocks.append(stock)
        
        logger.info(f"美股获取完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        return success_count, failure_count, failed_stocks
    
    def _fetch_single_us_stock_price_thread(self, stock: Dict[str, Any]) -> Tuple[bool, Optional[float], Optional[str]]:
        """在线程中获取单只美股价格"""
        code = stock['code']
        name = stock['name']
        
        print(f"正在获取美股 {name}({code}) 的收盘价...")
        
        # 获取美股价格
        price, date = self.data_source.get_stock_price(code, "US")
        
        if price is not None and date is not None:
            print(f"  √ 获取成功: {date} 收盘价 ${price}")
            return True, price, date
        else:
            print(f"  × 获取失败: 无法获取数据")
            return False, None, None
    
    def _save_us_stock_data_thread_safe(self, stock_id: int, price: float, date: str, code: str):
        """在主线程中安全保存美股数据"""
        db = get_database()
        if not db.connect():
            logger.error(f"保存美股 {stock_id} 数据时无法连接数据库")
            return False
        
        try:
            if db.insert_stock_nav(stock_id, date, price):
                # 获取美股详细信息
                info = self.data_source.get_us_stock_info(code)
                if info:
                    db.update_us_stock_info(stock_id, info)
                    logger.debug(f"美股 {code} 详细信息已更新")
                return True
            else:
                logger.error(f"保存美股 {stock_id} 数据失败")
                return False
        finally:
            db.close()
    
    # fetch_exchange_rates也需要类似修改
    
    def fetch_fund_navs(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """获取所有基金的最新净值"""
        # 在主线程中获取数据
        db = get_database()
        if not db.connect():
            logger.error("无法连接数据库")
            return 0, 0, []
        
        try:
            funds = db.get_all_funds()
        finally:
            db.close()
            
        if not funds:
            logger.warning("未找到任何基金信息")
            return 0, 0, []
        
        success_count = 0
        failure_count = 0
        failed_funds = []
        
        print(f"\n开始获取 {len(funds)} 只基金的净值...")
        logger.info(f"开始获取 {len(funds)} 只基金的净值")
        
        # 使用线程池并行获取数据
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for fund in funds:
                future = executor.submit(self._fetch_single_fund_nav_thread, fund)
                futures[future] = fund
            
            for future in as_completed(futures):
                fund = futures[future]
                try:
                    success, nav, date = future.result()
                    if success:
                        success_count += 1
                        # 在主线程中保存数据
                        self._save_fund_data_thread_safe(fund['id'], nav, date)
                    else:
                        failure_count += 1
                        failed_funds.append(fund)
                except Exception as e:
                    logger.error(f"获取基金 {fund.get('code')} 数据时出现异常: {e}")
                    failure_count += 1
                    failed_funds.append(fund)
        
        logger.info(f"基金获取完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        return success_count, failure_count, failed_funds
    
    def _fetch_single_fund_nav_thread(self, fund: Dict[str, Any]) -> Tuple[bool, Optional[float], Optional[str]]:
        """在线程中获取单只基金净值"""
        code = fund['code']
        name = fund['name']
        market_code = fund.get('market_code', None)  # 获取市场代码
        
        print(f"正在获取 {name}({code}) 的净值...")
        
        # 获取基金净值 - 传递市场代码
        nav, date = self.data_source.get_fund_nav(code, market_code)
        
        if nav is not None and date is not None:
            print(f"  √ 获取成功: {date} 净值 {nav}")
            return True, nav, date
        else:
            print(f"  × 获取失败: 无法获取数据")
            return False, None, None
    
    def _save_fund_data_thread_safe(self, fund_id: int, nav: float, date: str):
        """在主线程中安全保存基金数据"""
        db = get_database()
        if not db.connect():
            logger.error(f"保存基金 {fund_id} 数据时无法连接数据库")
            return False
        
        try:
            if db.insert_fund_nav(fund_id, date, nav):
                return True
            else:
                logger.error(f"保存基金 {fund_id} 数据失败")
                return False
        finally:
            db.close()
    
    def fetch_exchange_rates(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """获取所有货币的最新汇率"""
        # 在主线程中获取数据
        db = get_database()
        if not db.connect():
            logger.error("无法连接数据库")
            return 0, 0, []
        
        try:
            currencies = db.get_all_currencies()
        finally:
            db.close()
            
        if not currencies:
            logger.warning("未找到任何货币信息")
            return 0, 0, []
        
        success_count = 0
        failure_count = 0
        failed_currencies = []
        
        print(f"\n开始获取 {len(currencies)} 种货币的汇率...")
        logger.info(f"开始获取 {len(currencies)} 种货币的汇率")
        
        # 使用线程池并行获取数据
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for currency in currencies:
                future = executor.submit(self._fetch_single_exchange_rate_thread, currency)
                futures[future] = currency
            
            for future in as_completed(futures):
                currency = futures[future]
                try:
                    success, rate, date = future.result()
                    if success:
                        success_count += 1
                        # 在主线程中保存数据
                        self._save_exchange_data_thread_safe(currency['id'], rate, date)
                    else:
                        failure_count += 1
                        failed_currencies.append(currency)
                except Exception as e:
                    logger.error(f"获取货币 {currency.get('currency')} 数据时出现异常: {e}")
                    failure_count += 1
                    failed_currencies.append(currency)
        
        logger.info(f"汇率获取完成: 成功 {success_count} 种, 失败 {failure_count} 种")
        return success_count, failure_count, failed_currencies
    
    def _fetch_single_exchange_rate_thread(self, currency: Dict[str, Any]) -> Tuple[bool, Optional[float], Optional[str]]:
        """在线程中获取单个汇率"""
        currency_code = currency['currency']
        
        print(f"正在获取 {currency_code}/CNY 的汇率...")
        
        # 获取汇率
        rate, date = self.data_source.get_exchange_rate(currency_code)
        
        if rate is not None and date is not None:
            print(f"  √ 获取成功: {date} 汇率 {rate}")
            return True, rate, date
        else:
            print(f"  × 获取失败: 无法获取数据")
            return False, None, None
    
    def _save_exchange_data_thread_safe(self, currency_id: int, rate: float, date: str):
        """在主线程中安全保存汇率数据"""
        db = get_database()
        if not db.connect():
            logger.error(f"保存货币 {currency_id} 数据时无法连接数据库")
            return False
        
        try:
            if db.insert_exchange_rate(currency_id, rate, date):
                return True
            else:
                logger.error(f"保存货币 {currency_id} 数据失败")
                return False
        finally:
            db.close()
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """一键获取所有数据"""
        results = {}
        
        print("\n" + "="*60)
        print("开始一键更新所有数据")
        print("="*60)
        
        # 1. 备份数据库
        print("\n1. 备份数据库...")
        db = get_database()
        if db.connect():
            if db.backup():
                print("  √ 数据库备份成功")
            else:
                print("  × 数据库备份失败，继续执行...")
            db.close()
        else:
            print("  × 无法连接数据库，跳过备份...")
        
        # 2. 获取股票数据
        print("\n2. 获取股票最新收盘价...")
        stock_success, stock_failure, failed_stocks = self.fetch_stock_prices()
        results['stocks'] = {
            'success': stock_success,
            'failure': stock_failure,
            'failed_items': failed_stocks
        }
        
        # 3. 获取基金数据
        print("\n3. 获取基金最新净值...")
        fund_success, fund_failure, failed_funds = self.fetch_fund_navs()
        results['funds'] = {
            'success': fund_success,
            'failure': fund_failure,
            'failed_items': failed_funds
        }
        
        # 4. 获取汇率数据
        print("\n4. 获取最新汇率...")
        rate_success, rate_failure, failed_rates = self.fetch_exchange_rates()
        results['rates'] = {
            'success': rate_success,
            'failure': rate_failure,
            'failed_items': failed_rates
        }
        
        # 汇总结果
        total_success = stock_success + fund_success + rate_success
        total_failure = stock_failure + fund_failure + rate_failure
        
        results['total'] = {
            'success': total_success,
            'failure': total_failure
        }
        
        print("\n" + "="*60)
        print("数据更新完成")
        print("="*60)
        print(f"股票: 成功 {stock_success} 只, 失败 {stock_failure} 只")
        print(f"基金: 成功 {fund_success} 只, 失败 {fund_failure} 只")
        print(f"汇率: 成功 {rate_success} 种, 失败 {rate_failure} 种")
        print(f"总计: 成功 {total_success} 项, 失败 {total_failure} 项")
        print("="*60)
        
        return results