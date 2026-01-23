# alpha_vantage_data_source.py
import logging
import os
from datetime import datetime
from typing import Optional, Tuple, List

from .base_data_source import DataSource, DataSourceType

logger = logging.getLogger(__name__)


class AlphaVantageDataSource(DataSource):
    """Alpha Vantage 数据源实现（用于美股）"""
    
    def __init__(self, api_key: str = None, timeout: int = 30):
        self.api_key = api_key or self._get_api_key()
        self.timeout = timeout
        self.base_url = "https://www.alphavantage.co/query"
        logger.info("Alpha Vantage 数据源初始化成功")
    
    def get_name(self) -> str:
        return "Alpha Vantage (专业金融API)"
    
    def get_data_source_type(self) -> DataSourceType:
        return DataSourceType.ALPHA_VANTAGE
    
    def get_supported_markets(self) -> List[str]:
        return ["US"]
    
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票价格"""
        if market_code != "US":
            logger.warning(f"Alpha Vantage仅支持美股，不支持市场: {market_code}")
            return None, None
        
        if not self.api_key:
            logger.error("未设置Alpha Vantage API密钥")
            return None, None
        
        return self._get_alpha_vantage_data(code, 'TIME_SERIES_DAILY', '股票')
    
    def get_fund_nav(self, code: str, market_code: str = None) -> Tuple[Optional[float], Optional[str]]:
        """获取基金净值"""
        logger.warning("Alpha Vantage不提供基金数据，请使用其他数据源")
        return None, None
    
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取汇率"""
        if not self.api_key:
            logger.error("未设置Alpha Vantage API密钥")
            return None, None
        
        try:
            import requests
            params = {
                'function': 'CURRENCY_EXCHANGE_RATE',
                'from_currency': currency,
                'to_currency': 'CNY',
                'apikey': self.api_key
            }
            
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            data = response.json()
            
            if "Realtime Currency Exchange Rate" in data:
                exchange_data = data["Realtime Currency Exchange Rate"]
                rate = round(float(exchange_data["5. Exchange Rate"]), 4)
                date = exchange_data.get("6. Last Refreshed", datetime.now().strftime('%Y-%m-%d'))
                
                logger.info(f"通过Alpha Vantage获取 {currency}/CNY 汇率成功: {date} 汇率 {rate}")
                return rate, date
            else:
                logger.warning(f"Alpha Vantage未返回有效汇率数据")
                return None, None
                
        except Exception as e:
            logger.error(f"通过Alpha Vantage获取汇率数据时出错: {e}")
            return None, None
    
    # 私有方法
    def _get_api_key(self) -> str:
        """获取API密钥"""
        api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            logger.warning("未设置Alpha Vantage API密钥，请在环境变量中设置ALPHA_VANTAGE_API_KEY")
        return api_key
    
    def _get_alpha_vantage_data(self, symbol: str, function: str, data_type: str) -> Tuple[Optional[float], Optional[str]]:
        """获取Alpha Vantage数据"""
        try:
            import requests
            params = {
                'function': function,
                'symbol': symbol,
                'apikey': self.api_key,
                'outputsize': 'compact'
            }
            
            response = requests.get(self.base_url, params=params, timeout=self.timeout)
            data = response.json()
            
            if "Time Series (Daily)" in data:
                time_series = data["Time Series (Daily)"]
                latest_date = list(time_series.keys())[0]
                latest_data = time_series[latest_date]
                price = round(float(latest_data["4. close"]), 4)
                
                logger.info(f"通过Alpha Vantage获取{data_type} {symbol} 成功: {latest_date} 收盘价 ${price}")
                return price, latest_date
            else:
                logger.warning(f"Alpha Vantage未返回有效数据: {data.get('Note', 'Unknown error')}")
                return None, None
                
        except Exception as e:
            logger.error(f"通过Alpha Vantage获取数据时出错: {e}")
            return None, None