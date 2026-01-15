# fetcher.py
import logging
import time
from typing import Tuple, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed

from data_source import get_data_source, HybridDataSource
from database import get_database
from config import DECIMAL_PLACES

logger = logging.getLogger(__name__)


class DataFetcher:
    """数据获取功能类"""
    
    def __init__(self, max_workers: int = 5):
        self.data_source = get_data_source()
        self.db = get_database()
        self.max_workers = max_workers
        logger.info(f"数据获取器初始化成功，最大线程数: {max_workers}")
    
    def fetch_stock_prices(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """获取所有股票的最新收盘价"""
        stocks = self.db.get_all_stocks()
        success_count = 0
        failure_count = 0
        failed_stocks = []
        
        if not stocks:
            logger.warning("未找到任何股票信息")
            return 0, 0, []
        
        print(f"\n开始获取 {len(stocks)} 只股票的收盘价...")
        logger.info(f"开始获取 {len(stocks)} 只股票的收盘价")
        
        # 使用线程池并行获取
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for stock in stocks:
                future = executor.submit(self._fetch_single_stock_price, stock)
                futures[future] = stock
            
            for future in as_completed(futures):
                stock = futures[future]
                try:
                    success = future.result()
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                        failed_stocks.append(stock)
                except Exception as e:
                    logger.error(f"获取股票 {stock.get('code')} 数据时出现异常: {e}")
                    failure_count += 1
                    failed_stocks.append(stock)
        
        logger.info(f"股票获取完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        return success_count, failure_count, failed_stocks
    
    def _fetch_single_stock_price(self, stock: Dict[str, Any]) -> bool:
        """获取单只股票价格"""
        stock_id = stock['id']
        code = stock['code']
        name = stock['name']
        market_code = stock.get('market_code', 'SH')
        
        print(f"正在获取 {name}({code}) [{market_code}] 的收盘价...")
        
        # 获取股票价格
        price, date = self.data_source.get_stock_price(code, market_code)
        
        if price is not None and date is not None:
            if self.db.insert_stock_nav(stock_id, date, price):
                # 如果是美股，获取详细信息
                if market_code == "US":
                    self._fetch_us_stock_info(stock_id, code)
                
                print(f"  √ 成功: {date} 收盘价 {price}")
                return True
            else:
                print(f"  × 失败: 数据库插入失败")
                return False
        else:
            print(f"  × 失败: 无法获取数据")
            return False
    
    def _fetch_us_stock_info(self, stock_id: int, code: str):
        """获取美股详细信息"""
        try:
            if isinstance(self.data_source, HybridDataSource):
                info = self.data_source.get_us_stock_info(code)
                if info:
                    self.db.update_us_stock_info(stock_id, info)
                    logger.debug(f"美股 {code} 详细信息已更新")
        except Exception as e:
            logger.error(f"获取美股 {code} 信息失败: {e}")
    
    def fetch_fund_navs(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """获取所有基金的最新净值"""
        funds = self.db.get_all_funds()
        success_count = 0
        failure_count = 0
        failed_funds = []
        
        if not funds:
            logger.warning("未找到任何基金信息")
            return 0, 0, []
        
        print(f"\n开始获取 {len(funds)} 只基金的净值...")
        logger.info(f"开始获取 {len(funds)} 只基金的净值")
        
        # 使用线程池并行获取
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            for fund in funds:
                future = executor.submit(self._fetch_single_fund_nav, fund)
                futures[future] = fund
            
            for future in as_completed(futures):
                fund = futures[future]
                try:
                    success = future.result()
                    if success:
                        success_count += 1
                    else:
                        failure_count += 1
                        failed_funds.append(fund)
                except Exception as e:
                    logger.error(f"获取基金 {fund.get('code')} 数据时出现异常: {e}")
                    failure_count += 1
                    failed_funds.append(fund)
        
        logger.info(f"基金获取完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        return success_count, failure_count, failed_funds
    
    def _fetch_single_fund_nav(self, fund: Dict[str, Any]) -> bool:
        """获取单只基金净值"""
        fund_id = fund['id']
        code = fund['code']
        name = fund['name']
        
        print(f"正在获取 {name}({code}) 的净值...")
        
        # 获取基金净值
        nav, date = self.data_source.get_fund_nav(code)
        
        if nav is not None and date is not None:
            if self.db.insert_fund_nav(fund_id, date, nav):
                print(f"  √ 成功: {date} 净值 {nav}")
                return True
            else:
                print(f"  × 失败: 数据库插入失败")
                return False
        else:
            print(f"  × 失败: 无法获取数据")
            return False
    
    def fetch_exchange_rates(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """获取所有货币的最新汇率"""
        currencies = self.db.get_all_currencies()
        success_count = 0
        failure_count = 0
        failed_currencies = []
        
        if not currencies:
            logger.warning("未找到任何货币信息")
            return 0, 0, []
        
        print(f"\n开始获取 {len(currencies)} 种货币的汇率...")
        logger.info(f"开始获取 {len(currencies)} 种货币的汇率")
        
        for currency in currencies:
            currency_id = currency['id']
            currency_code = currency['currency']
            
            print(f"正在获取 {currency_code}/CNY 的汇率...")
            
            rate, date = self.data_source.get_exchange_rate(currency_code)
            
            if rate is not None and date is not None:
                if self.db.insert_exchange_rate(currency_id, rate, date):
                    print(f"  √ 成功: {date} 汇率 {rate}")
                    success_count += 1
                else:
                    print(f"  × 失败: 数据库插入失败")
                    failure_count += 1
                    failed_currencies.append(currency)
            else:
                print(f"  × 失败: 无法获取数据")
                failure_count += 1
                failed_currencies.append(currency)
        
        logger.info(f"汇率获取完成: 成功 {success_count} 种, 失败 {failure_count} 种")
        return success_count, failure_count, failed_currencies
    
    def fetch_us_stocks_only(self) -> Tuple[int, int, List[Dict[str, Any]]]:
        """仅获取美股数据"""
        us_stocks = self.db.get_us_stocks()
        success_count = 0
        failure_count = 0
        failed_stocks = []
        
        if not us_stocks:
            logger.warning("未找到任何美股信息")
            return 0, 0, []
        
        print(f"\n开始获取 {len(us_stocks)} 只美股的收盘价...")
        logger.info(f"开始获取 {len(us_stocks)} 只美股的收盘价")
        
        for stock in us_stocks:
            stock_id = stock['id']
            code = stock['code']
            name = stock['name']
            
            print(f"正在获取美股 {name}({code}) 的收盘价...")
            
            # 获取美股价格
            price, date = self.data_source.get_stock_price(code, "US")
            
            if price is not None and date is not None:
                if self.db.insert_stock_nav(stock_id, date, price):
                    # 获取美股详细信息
                    self._fetch_us_stock_info(stock_id, code)
                    
                    print(f"  √ 成功: {date} 收盘价 ${price}")
                    success_count += 1
                else:
                    print(f"  × 失败: 数据库插入失败")
                    failure_count += 1
                    failed_stocks.append(stock)
            else:
                print(f"  × 失败: 无法获取数据")
                failure_count += 1
                failed_stocks.append(stock)
        
        logger.info(f"美股获取完成: 成功 {success_count} 只, 失败 {failure_count} 只")
        return success_count, failure_count, failed_stocks
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """一键获取所有数据"""
        results = {}
        
        print("\n" + "="*60)
        print("开始一键更新所有数据")
        print("="*60)
        
        # 1. 备份数据库
        print("\n1. 备份数据库...")
        if self.db.backup():
            print("  √ 数据库备份成功")
        else:
            print("  × 数据库备份失败，继续执行...")
        
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