# data_source.py
import asyncio
import aiohttp
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import logging
from abc import ABC, abstractmethod
import akshare as ak
import sys
import time 

# 设置日志
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSource(ABC):
    """数据源抽象基类"""
    
    @abstractmethod
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票最新收盘价和日期"""
        pass
    
    @abstractmethod
    def get_fund_nav(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取基金最新净值和日期"""
        pass
    
    @abstractmethod
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取货币兑换人民币的汇率和日期"""
        pass


class AkshareDataSource(DataSource):
    """Akshare 数据源实现（主要用于A股和国内基金）"""
    
    def __init__(self, timeout: int = 30):
        try:
            import akshare as ak
            self.ak = ak
            self.timeout = timeout
            logger.info("Akshare 数据源初始化成功")
        except ImportError:
            logger.error("请先安装 akshare 库: pip install akshare")
            sys.exit(1)
    
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票最新收盘价和日期（主要用于A股）"""
        try:
            # 处理不同市场
            if market_code in ["SH", "SZ", "BJ"]:
                return self._get_a_stock_price(code, market_code)
            elif market_code == "US":
                # 美股交给专门的美股数据源处理
                logger.info(f"股票 {code} 为美股，将使用美股数据源")
                return None, None
            else:
                logger.warning(f"不支持的A股市场代码: {market_code}")
                return None, None
                
        except Exception as e:
            logger.error(f"获取股票 {code} 数据时出错: {e}")
            return None, None
    
    def _get_a_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取A股股票价格"""
        try:
            # 根据市场代码确定前缀
            if market_code == "SH":
                symbol = f"sh{code}"
            elif market_code == "SZ":
                symbol = f"sz{code}"
            elif market_code == "BJ":
                symbol = f"bj{code}"
            else:
                return None, None
            
            # 尝试多种获取方式
            price, date = self._try_get_stock_price_methods(code, symbol)
            
            if price is not None and date is not None:
                logger.info(f"获取股票 {code} 成功: {date} 收盘价 {price}")
                return price, date
            
            logger.warning(f"所有方法都无法获取股票 {code} 的数据")
            return None, None
            
        except Exception as e:
            logger.error(f"获取A股 {code} 数据时出错: {e}")
            return None, None
    
    def _try_get_stock_price_methods(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
        """尝试多种方法获取股票价格"""
        methods = [
            self._get_stock_price_method1,
            self._get_stock_price_method2,
            self._get_stock_price_method3
        ]
        
        for method in methods:
            try:
                price, date = method(code, symbol)
                if price is not None and date is not None:
                    return price, date
            except Exception as e:
                logger.debug(f"方法 {method.__name__} 失败: {e}")
                continue
        
        return None, None
    
    def _get_stock_price_method1(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
        """方法1: 使用 stock_zh_a_hist"""
        try:
            # 获取前一天的日期
            yesterday = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
            today = datetime.now().strftime('%Y%m%d')
            
            df = self.ak.stock_zh_a_hist(
                symbol=code, 
                period="daily", 
                start_date=yesterday,
                end_date=today,
                adjust="qfq"
            )
            
            if not df.empty:
                latest = df.iloc[-1]
                price = round(float(latest['收盘']), 4)
                date = str(latest['日期'])
                return price, date
        except Exception as e:
            logger.debug(f"方法1失败: {e}")
        
        return None, None
    
    def _get_stock_price_method2(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
        """方法2: 使用 stock_zh_a_daily"""
        try:
            df = self.ak.stock_zh_a_daily(symbol=symbol, adjust="qfq")
            
            if not df.empty:
                latest = df.iloc[-1]
                price = round(float(latest['close']), 4)
                # 尝试获取日期
                if 'date' in latest.index:
                    date = str(latest['date'])
                else:
                    date = datetime.now().strftime('%Y-%m-%d')
                return price, date
        except Exception as e:
            logger.debug(f"方法2失败: {e}")
        
        return None, None
    
    def _get_stock_price_method3(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
        """方法3: 使用 stock_zh_a_spot"""
        try:
            df = self.ak.stock_zh_a_spot()
            if not df.empty:
                stock_data = df[df['代码'] == code]
                if not stock_data.empty:
                    price = round(float(stock_data.iloc[0]['最新价']), 4)
                    date = datetime.now().strftime('%Y-%m-%d')
                    return price, date
        except Exception as e:
            logger.debug(f"方法3失败: {e}")
        
        return None, None
    
    def get_fund_nav(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取基金最新净值和日期"""
        try:
            # 尝试多种基金数据获取方法
            nav, date = self._try_get_fund_nav_methods(code)
            
            if nav is not None and date is not None:
                logger.info(f"获取基金 {code} 成功: {date} 净值 {nav}")
                return nav, date
            
            logger.warning(f"所有方法都无法获取基金 {code} 的数据")
            return None, None
            
        except Exception as e:
            logger.error(f"获取基金 {code} 数据时出错: {e}")
            return None, None
    
    def _try_get_fund_nav_methods(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """尝试多种方法获取基金净值"""
        methods = [
            self._get_fund_nav_method1,
            self._get_fund_nav_method2
        ]
        
        for method in methods:
            try:
                nav, date = method(code)
                if nav is not None and date is not None:
                    return nav, date
            except Exception as e:
                logger.debug(f"基金方法 {method.__name__} 失败: {e}")
                continue
        
        return None, None
    
    def _get_fund_nav_method1(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """方法1: 使用 fund_em_open_fund_info"""
        try:
            df = self.ak.fund_em_open_fund_info(fund=code, indicator="单位净值走势")
            
            if not df.empty:
                latest = df.iloc[-1]
                nav = round(float(latest['单位净值']), 4)
                date = str(latest['净值日期'])
                return nav, date
        except Exception as e:
            logger.debug(f"基金方法1失败: {e}")
        
        return None, None
    
    def _get_fund_nav_method2(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """方法2: 使用 fund_em_value_estimation"""
        try:
            df = self.ak.fund_em_value_estimation(symbol=code)
            
            if not df.empty:
                latest = df.iloc[-1]
                if '估算净值' in latest.index:
                    nav = round(float(latest['估算净值']), 4)
                    date = datetime.now().strftime('%Y-%m-%d')
                    return nav, date
        except Exception as e:
            logger.debug(f"基金方法2失败: {e}")
        
        return None, None
    
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取货币兑换人民币的汇率和日期"""
        try:
            if currency == "USD":
                # 获取美元兑人民币汇率
                df = self.ak.fx_spot_quote()
                if df is not None and not df.empty:
                    usd_row = df[df['名称'] == '美元兑人民币']
                    
                    if not usd_row.empty:
                        rate = round(float(usd_row.iloc[0]['中间价']), 4)
                        # 获取最近交易日
                        date_df = self.ak.tool_trade_date_hist_sina()
                        if not date_df.empty:
                            latest_date = date_df.iloc[-1]['trade_date']
                            logger.info(f"获取 USD/CNY 汇率成功: {latest_date} 汇率 {rate}")
                            return rate, str(latest_date)
                        else:
                            date = datetime.now().strftime('%Y-%m-%d')
                            return rate, date
                
                logger.warning("未找到美元兑人民币汇率数据")
                return None, None
            elif currency == "CNY":
                return 1.0, datetime.now().strftime('%Y-%m-%d')  # 人民币自身汇率为1
            elif currency == "HKD":
                # 获取港币汇率
                df = self.ak.fx_spot_quote()
                if df is not None and not df.empty:
                    hkd_row = df[df['名称'] == '港币兑人民币']
                    if not hkd_row.empty:
                        rate = round(float(hkd_row.iloc[0]['中间价']), 4)
                        date = datetime.now().strftime('%Y-%m-%d')
                        return rate, date
                
                logger.warning("未找到港币兑人民币汇率数据")
                return None, None
            else:
                logger.warning(f"暂不支持获取 {currency} 的汇率")
                return None, None
                
        except Exception as e:
            logger.error(f"获取汇率数据时出错: {e}")
            return None, None


class USStockDataSource:
    """美股数据源专用类"""

    def __init__(self, max_retries: int = 5, retry_delay: int = 5):
        try:
            import yfinance as yf
            self.yf = yf
            self.max_retries = max_retries
            self.retry_delay = retry_delay
            self.request_delay = 1  # 请求之间的延迟（秒）
            self.last_request_time = 0  # 记录上次请求时间
            logger.info("美股数据源初始化成功（使用 yfinance）")
        except ImportError:
            logger.error("请先安装 yfinance 库: pip install yfinance")
            logger.info("尝试使用备选数据源...")
            self.yf = None
    
    def _throttle_request(self):
        """请求限流，避免请求过于频繁"""
        import time
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            logger.debug(f"请求限流，等待 {sleep_time:.2f} 秒")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def get_us_stock_price(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取美股最新收盘价和日期"""
        for attempt in range(self.max_retries):
            try:
                if self.yf is None:
                    logger.error("yfinance 未安装，无法获取美股数据")
                    return None, None
                
                # 请求限流
                self._throttle_request()
                
                # 创建ticker对象
                ticker = self.yf.Ticker(code)
                
                # 获取历史数据（最近10天）
                import pandas as pd
                end_date = datetime.now()
                start_date = end_date - timedelta(days=30)  # 获取30天数据确保有交易日
                
                hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
                
                if hist.empty:
                    logger.warning(f"未找到美股 {code} 的历史数据")
                    # 尝试使用更长时间范围
                    start_date = end_date - timedelta(days=365)
                    
                    # 再次请求限流
                    self._throttle_request()
                    
                    hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
                
                if not hist.empty:
                    # 获取最新收盘价
                    latest = hist.iloc[-1]
                    
                    # 优先使用收盘价，如果没有则使用最后交易价
                    if 'Close' in latest:
                        price = round(float(latest['Close']), 4)
                    elif 'close' in latest:
                        price = round(float(latest['close']), 4)
                    else:
                        # 尝试获取其他价格字段
                        for price_field in ['Close', 'close', 'Last', 'last', 'Price', 'price']:
                            if price_field in latest:
                                price = round(float(latest[price_field]), 4)
                                break
                        else:
                            logger.error(f"美股 {code} 数据中没有找到价格字段")
                            return None, None
                    
                    # 获取日期
                    date_index = hist.index[-1]
                    if isinstance(date_index, pd.Timestamp):
                        date = date_index.strftime('%Y-%m-%d')
                    elif hasattr(date_index, 'strftime'):
                        date = date_index.strftime('%Y-%m-%d')
                    else:
                        date_str = str(date_index)
                        # 尝试从字符串中提取日期
                        if ' ' in date_str:
                            date = date_str.split()[0]
                        else:
                            date = date_str
                    
                    logger.info(f"获取美股 {code} 成功: {date} 收盘价 ${price}")
                    return price, date
                else:
                    logger.warning(f"美股 {code} 没有可用的历史数据")
                    return None, None
                    
            except Exception as e:
                error_msg = str(e).lower()
                
                # 处理特定错误
                if "too many requests" in error_msg or "rate limit" in error_msg:
                    wait_time = self.retry_delay * (attempt + 1)  # 指数退避
                    logger.warning(f"美股 {code}请求频率过高，等待 {wait_time} 秒后重试 (尝试 {attempt+1}/{self.max_retries})")
                    time.sleep(wait_time)
                    continue
                elif "not found" in error_msg or "does not exist" in error_msg:
                    logger.error(f"美股 {code} 不存在")
                    return None, None
                
                logger.error(f"获取美股 {code} 数据时出错 (尝试 {attempt+1}/{self.max_retries}): {e}")
                
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    return None, None
        
        return None, None
    
    def get_us_stock_info(self, code: str) -> Optional[Dict[str, Any]]:
        """获取美股详细信息"""
        for attempt in range(self.max_retries):
            try:
                if self.yf is None:
                    return None
                
                ticker = self.yf.Ticker(code)
                info = ticker.info
                
                if info:
                    # 安全地获取字段
                    result = {
                        'symbol': info.get('symbol', code),
                        'name': info.get('longName') or info.get('shortName', code),
                        'sector': info.get('sector', 'N/A'),
                        'industry': info.get('industry', 'N/A'),
                        'market_cap': info.get('marketCap', 0),
                        'pe_ratio': info.get('trailingPE') or info.get('forwardPE', 0),
                        'dividend_yield': info.get('dividendYield', 0),
                        'currency': info.get('currency', 'USD'),
                        'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0),
                        'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                        'beta': info.get('beta', 0),
                        'volume': info.get('volume', 0),
                        'average_volume': info.get('averageVolume', 0)
                    }
                    
                    # 清理结果，确保所有值都是可序列化的
                    for key, value in result.items():
                        if isinstance(value, (float, int)):
                            # 保留原样
                            pass
                        elif value is None:
                            result[key] = 'N/A'
                        else:
                            # 确保是字符串
                            result[key] = str(value)
                    
                    return result
                
                return None
                
            except Exception as e:
                logger.error(f"获取美股 {code} 信息时出错 (尝试 {attempt+1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    return None
        
        return None


class HybridDataSource(DataSource):
    """混合数据源：整合Akshare和美股数据源"""
    
    def __init__(self):
        self.akshare_ds = AkshareDataSource()
        self.us_ds = USStockDataSource()
        logger.info("混合数据源初始化成功")
    
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票价格，根据市场自动选择数据源"""
        if market_code == "US":
            # 使用美股数据源
            return self.us_ds.get_us_stock_price(code)
        else:
            # 使用Akshare数据源（A股）
            return self.akshare_ds.get_stock_price(code, market_code)
    
    def get_fund_nav(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取基金净值（使用Akshare）"""
        return self.akshare_ds.get_fund_nav(code)
    
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取汇率（使用Akshare）"""
        return self.akshare_ds.get_exchange_rate(currency)
    
    def get_us_stock_info(self, code: str) -> Optional[Dict[str, Any]]:
        """获取美股详细信息"""
        return self.us_ds.get_us_stock_info(code)


# 全局数据源实例
_data_source_instance = None

def get_data_source() -> DataSource:
    """获取数据源实例（单例模式）"""
    global _data_source_instance
    if _data_source_instance is None:
        _data_source_instance = HybridDataSource()
    return _data_source_instance