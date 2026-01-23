# akshare_data_source.py
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict
import sys

# 使用相对导入
from .base_data_source import DataSource, DataSourceType

logger = logging.getLogger(__name__)


class AkshareDataSource(DataSource):
    """Akshare 数据源实现（支持A股和美股）"""
    
    def __init__(self, timeout: int = 30):
        try:
            import akshare as ak
            self.ak = ak
            self.timeout = timeout
            logger.info("Akshare 数据源初始化成功")
        except ImportError:
            logger.error("请先安装 akshare 库: pip install akshare")
            sys.exit(1)
    
    def get_name(self) -> str:
        return "Akshare (支持A股、美股、基金、汇率)"
    
    def get_data_source_type(self) -> DataSourceType:
        return DataSourceType.AKSHARE
    
    def get_supported_markets(self) -> List[str]:
        return ["SH", "SZ", "BJ", "US", "HK"]
    
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票价格"""
        if market_code in ["SH", "SZ", "BJ"]:
            return self._get_a_stock_price(code, market_code)
        elif market_code == "US":
            return self._get_us_stock_price(code)
        else:
            logger.warning(f"Akshare不支持市场: {market_code}")
            return None, None
    
    def get_fund_nav(self, code: str, market_code: str = None) -> Tuple[Optional[float], Optional[str]]:
        """获取基金净值"""
        if market_code == "US":
            return self._get_us_fund_nav(code)
        else:
            return self._get_domestic_fund_nav(code)
    
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取汇率"""
        try:
            df = self.ak.currency_boc_safe()
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                if currency == "USD":
                    rate = round(float(latest['美元']/100), 4)
                    date = latest['日期'].strftime('%Y-%m-%d')
                if currency == "HKD":
                    rate = round(float(latest['港元']/100), 4)
                    date = latest['日期'].strftime('%Y-%m-%d')
                logger.info(f"获取 {currency} 汇率成功: {date} 汇率 {rate}")
                return rate, date
            
            else:
                logger.warning(f"网络问题获取不到 {currency} 的汇率")
                return None, None
        except Exception as e:
            logger.error(f"获取汇率数据时出错: {e}")
            return None, None
        
    # 在 AkshareDataSource 类中添加一个新的方法
    def get_exchange_rates_batch(self, currencies: List[str]) -> Dict[str, Tuple[Optional[float], Optional[str]]]:
        """批量获取汇率数据"""
        try:
            df = self.ak.currency_boc_safe()
            if df is None or df.empty:
                logger.warning("网络问题获取不到汇率数据")
                return {}
            
            result = {}
            latest = df.iloc[-1]
            date = latest['日期'].strftime('%Y-%m-%d')
            
            # 映射币种代码到对应的列名
            currency_mapping = {
                "USD": "美元",
                "HKD": "港元",
                # 可以根据需要添加更多币种映射
            }
            
            for currency in currencies:
                if currency in currency_mapping:
                    column_name = currency_mapping[currency]
                    try:
                        rate = round(float(latest[column_name] / 100), 4)
                        result[currency] = (rate, date)
                        logger.debug(f"获取 {currency} 汇率成功: {date} 汇率 {rate}")
                    except (KeyError, ValueError) as e:
                        logger.warning(f"无法获取 {currency} 的汇率: {e}")
                        result[currency] = (None, None)
                else:
                    logger.warning(f"不支持的币种: {currency}")
                    result[currency] = (None, None)
            
            return result
        except Exception as e:
            logger.error(f"批量获取汇率数据时出错: {e}")
            return {}
    
    # 私有方法
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
    
    def _get_us_stock_price(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取美股价格"""
        try:
            # 确保代码大写
            code = code.upper()

            # 方法1: 使用 stock_us_hist
            try:
                df = self.ak.stock_us_hist(
                    symbol=code,
                    period="daily",
                    start_date=(datetime.now() - timedelta(days=7)).strftime('%Y%m%d'),
                    end_date=datetime.now().strftime('%Y%m%d'),
                    adjust="qfq"
                )
                
                if df is None:
                    logger.warning(f"stock_us_hist 返回 None，股票代码 {code} 可能不存在或无数据")

                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    price = round(float(latest['收盘']), 4)
                    date = str(latest['日期'])
                    logger.info(f"通过Akshare获取美股 {code} 成功: {date} 收盘价 ${price}")
                    return price, date
            except Exception as e1:
                logger.warning(f"方法1失败: {e1}")
            
            # 方法2: 尝试其他接口
            try:
                df = self.ak.stock_us_daily(symbol=code)
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    price = round(float(latest['close']), 4)
                    date = latest['date'].strftime('%Y-%m-%d')
                    logger.info(f"通过Akshare备用接口获取美股 {code} 成功: {date} 收盘价 ${price}")
                    return price, date
            except Exception as e2:
                logger.error(f"方法2失败: {e2}")
            
            # 方法3: 使用 stock_zh_a_spot_em 接口（有时可以获取美股）
            try:
                df = self.ak.stock_zh_a_spot_em()
                if df is not None and not df.empty:
                    # 查找美股代码（通常以.US结尾或大写字母）
                    for idx, row in df.iterrows():
                        if code in row['代码'] or code in row['名称']:
                            price = round(float(row['最新价']), 4)
                            date = datetime.now().strftime('%Y-%m-%d')
                            logger.info(f"通过Akshare spot接口获取美股 {code} 成功: ${price}")
                            return price, date
            except Exception as e3:
                logger.error(f"方法3失败: {e3}")
            
            logger.warning(f"无法获取美股 {code} 的数据")
            return None, None
        except Exception as e:
            logger.error(f"获取美股 {code} 数据时出错: {e}")
            return None, None
    
    def _get_domestic_fund_nav(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取国内基金净值"""
        try:
            # 方法1: 使用 fund_em_open_fund_info
            try:
                df = self.ak.fund_open_fund_info_em(symbol=code, indicator="单位净值走势")
                if df is not None and not df.empty:
                    latest = df.iloc[-1]
                    nav = round(float(latest['单位净值']), 4)
                    date = str(latest['净值日期'])
                    return nav, date
            except Exception as e1:
                logger.error(f"基金方法1失败: {e1}")
           
        except Exception as e:
            logger.error(f"获取基金 {code} 数据时出错: {e}")
            return None, None
    
    def _get_us_fund_nav(self, code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取美股基金净值"""
        try:
            # 美股基金通常是ETF，尝试使用股票接口获取
            return self._get_us_stock_price(code)
        except Exception as e:
            logger.warning(f"通过Akshare获取美股基金 {code} 失败: {e}")
            return None, None
    
    def _try_get_stock_price_methods(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
        """尝试多种方法获取股票价格"""
        methods = [
            self._get_stock_price_method1
            ,self._get_stock_price_method2
            # ,self._get_stock_price_method3
            # ,self._get_stock_price_method4
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
            yesterday = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
            today = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
            
            df = self.ak.stock_zh_a_hist(
                symbol=code, 
                period="daily", 
                start_date=yesterday,
                end_date=today,
                adjust="qfq"
            )
            
            if df is not None and not df.empty:
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
            
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                price = round(float(latest['close']), 4)
                if 'date' in latest.index:
                    date = str(latest['date'])
                else:
                    date = datetime.now().strftime('%Y-%m-%d')
                return price, date
        except Exception as e:
            logger.debug(f"方法2失败: {e}")
        
        return None, None
    
    # def _get_stock_price_method3(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
    #     """方法3: 使用 stock_zh_a_spot"""
    #     try:
    #         df = self.ak.stock_zh_a_spot()
    #         if df is not None and not df.empty:
    #             stock_data = df[df['代码'] == code]
    #             if not stock_data.empty:
    #                 price = round(float(stock_data.iloc[0]['最新价']), 4)
    #                 date = datetime.now().strftime('%Y-%m-%d')
    #                 return price, date
    #     except Exception as e:
    #         logger.debug(f"方法3失败: {e}")
        
    #     return None, None
    
    # def _get_stock_price_method4(self, code: str, symbol: str) -> Tuple[Optional[float], Optional[str]]:
    #     """方法4: 使用 stock_zh_a_spot_em"""
    #     try:
    #         df = self.ak.stock_zh_a_spot_em()
    #         if df is not None and not df.empty:
    #             stock_data = df[df['代码'] == code]
    #             if not stock_data.empty:
    #                 price = round(float(stock_data.iloc[0]['最新价']), 4)
    #                 date = datetime.now().strftime('%Y-%m-%d')
    #                 return price, date
    #     except Exception as e:
    #         logger.debug(f"方法4失败: {e}")
        
    #     return None, None

