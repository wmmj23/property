# yfinance_data_source.py
import logging
import time
from datetime import datetime, timedelta
from typing import Optional, Tuple, List
import pandas as pd

from .base_data_source import DataSource, DataSourceType

logger = logging.getLogger(__name__)


class YFinanceDataSource(DataSource):
    """YFinance 数据源实现（主要用于美股）"""
    
    def __init__(self, max_retries: int = 5, retry_delay: int = 5):
        try:
            import yfinance as yf
            self.yf = yf
            self.max_retries = max_retries
            self.retry_delay = retry_delay
            self.request_delay = 1
            self.last_request_time = 0
            logger.info("YFinance 数据源初始化成功")
        except ImportError:
            logger.error("请先安装 yfinance 库: pip install yfinance")
            self.yf = None
    
    def get_name(self) -> str:
        return "YFinance (专业美股数据)"
    
    def get_data_source_type(self) -> DataSourceType:
        return DataSourceType.YFINANCE
    
    def get_supported_markets(self) -> List[str]:
        return ["US"]
    
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票价格（仅支持美股）"""
        if market_code != "US":
            logger.warning(f"YFinance仅支持美股，不支持市场: {market_code}")
            return None, None
        
        return self._get_us_security_price(code, "股票")
    
    def get_fund_nav(self, code: str, market_code: str = None) -> Tuple[Optional[float], Optional[str]]:
        """获取基金净值（仅支持美股ETF）"""
        if market_code != "US":
            logger.warning(f"YFinance仅支持美股基金，不支持市场: {market_code}")
            return None, None
        
        return self._get_us_security_price(code, "基金")
    
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取汇率（YFinance不提供汇率数据）"""
        logger.warning("YFinance不提供汇率数据，请使用其他数据源")
        return None, None
    
    # 私有方法
    def _get_us_security_price(self, code: str, security_type: str) -> Tuple[Optional[float], Optional[str]]:
        """获取美股证券价格"""
        for attempt in range(self.max_retries):
            try:
                if self.yf is None:
                    return None, None
                
                # 请求限流
                self._throttle_request()
                
                ticker = self.yf.Ticker(code)
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)
                
                hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
                
                if hist.empty:
                    logger.warning(f"未找到 {code} 的历史数据")
                    start_date = end_date - timedelta(days=365)
                    self._throttle_request()
                    hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
                
                if not hist.empty:
                    latest = hist.iloc[-1]
                    
                    if 'Close' in latest:
                        price = round(float(latest['Close']), 4)
                    elif 'close' in latest:
                        price = round(float(latest['close']), 4)
                    else:
                        for price_field in ['Close', 'close', 'Last', 'last', 'Price', 'price']:
                            if price_field in latest:
                                price = round(float(latest[price_field]), 4)
                                break
                        else:
                            return None, None
                    
                    date_index = hist.index[-1]
                    if isinstance(date_index, pd.Timestamp):
                        date = date_index.strftime('%Y-%m-%d')
                    elif hasattr(date_index, 'strftime'):
                        date = date_index.strftime('%Y-%m-%d')
                    else:
                        date_str = str(date_index)
                        date = date_str.split()[0] if ' ' in date_str else date_str
                    
                    logger.info(f"通过YFinance获取{security_type} {code} 成功: {date} 价格 ${price}")
                    return price, date
                else:
                    return None, None
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                if "too many requests" in error_msg or "rate limit" in error_msg:
                    wait_time = self.retry_delay * (attempt + 1)
                    logger.warning(f"请求频率过高，等待 {wait_time} 秒后重试")
                    time.sleep(wait_time)
                    continue
                elif "not found" in error_msg or "does not exist" in error_msg:
                    logger.error(f"{code} 不存在")
                    return None, None
                
                logger.error(f"获取 {code} 数据时出错: {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    return None, None
        
        return None, None
    
    def _throttle_request(self):
        """请求限流"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            logger.debug(f"请求限流，等待 {sleep_time:.2f} 秒")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()