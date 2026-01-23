# data_source_manager.py
import logging
from typing import Optional, Tuple, Dict, List
from datetime import datetime

# 修改为相对导入
from .base_data_source import DataSource, DataSourceType, DataSourceFactory

logger = logging.getLogger(__name__)


class DataSourceManager:
    """数据源管理器 - 智能选择和管理数据源"""
    
    def __init__(self):
        self.data_sources = {}
        self.us_data_source_preference = None
        self._init_data_sources()
        logger.info("数据源管理器初始化成功")
    
    def _init_data_sources(self):
        """初始化所有可用的数据源"""    
        # 尝试加载各个数据源
        data_sources_to_try = [
            (DataSourceType.AKSHARE, "AkshareDataSource"),
            (DataSourceType.YFINANCE, "YFinanceDataSource"),
            (DataSourceType.ALPHA_VANTAGE, "AlphaVantageDataSource"),
        ]
        
        for source_type, class_name in data_sources_to_try:
            try:
                # 动态导入
                if source_type == DataSourceType.AKSHARE:
                    from .akshare_data_source import AkshareDataSource
                    data_source = AkshareDataSource()
                elif source_type == DataSourceType.YFINANCE:
                    from .yfinance_data_source import YFinanceDataSource
                    data_source = YFinanceDataSource()
                elif source_type == DataSourceType.ALPHA_VANTAGE:
                    from .alpha_vantage_data_source import AlphaVantageDataSource
                    data_source = AlphaVantageDataSource()
                else:
                    continue
                    
                self.data_sources[source_type] = data_source
                logger.info(f"数据源 {source_type.value} 加载成功")
            except ImportError as e:
                logger.warning(f"数据源 {source_type.value} 导入失败: {e}")
            except Exception as e:
                logger.warning(f"数据源 {source_type.value} 初始化失败: {e}")
    
    def get_available_data_sources(self, market_code: str = None) -> Dict[DataSourceType, DataSource]:
        """获取可用的数据源"""
        if not market_code:
            return self.data_sources
        
        # 过滤支持指定市场的数据源
        return {
            source_type: source 
            for source_type, source in self.data_sources.items()
            if market_code in source.get_supported_markets()
        }
    
    def get_data_source_for_market(self, market_code: str) -> Optional[DataSource]:
        """根据市场获取数据源"""
        # 国内市场使用Akshare
        if market_code in ["SH", "SZ", "BJ", "OF"]:
            return self.data_sources.get(DataSourceType.AKSHARE)
        
        # 美股使用用户设置的数据源
        elif market_code == "US":
            return self.get_us_data_source()
        
        else:
            logger.warning(f"不支持的市场代码: {market_code}")
            return None
    
    def get_us_data_source(self) -> Optional[DataSource]:
        """获取美股数据源，如果未设置则询问用户"""
        if self.us_data_source_preference:
            return self.data_sources.get(self.us_data_source_preference)
        else:
            return self._ask_for_us_data_source()
    
    def _ask_for_us_data_source(self) -> Optional[DataSource]:
        """交互式询问用户选择美股数据源"""
        available_sources = self.get_available_data_sources("US")
        
        if not available_sources:
            print("没有可用的美股数据源")
            return None
        
        print("\n" + "="*50)
        print("请选择美股数据源:")
        
        source_list = list(available_sources.items())
        for i, (source_type, source) in enumerate(source_list, 1):
            print(f"{i}. {source.get_name()}")
        
        print("="*50)
        
        try:
            choice = input(f"请选择 (1-{len(source_list)}, 默认1): ").strip()
            choice_idx = int(choice) - 1 if choice.isdigit() else 0
            
            if 0 <= choice_idx < len(source_list):
                selected_type, selected_source = source_list[choice_idx]
                self.us_data_source_preference = selected_type
                print(f"已选择美股数据源: {selected_source.get_name()}")
                return selected_source
            else:
                selected_type, selected_source = source_list[0]
                self.us_data_source_preference = selected_type
                print(f"已选择默认数据源: {selected_source.get_name()}")
                return selected_source
                
        except Exception as e:
            logger.error(f"选择数据源时出错: {e}")
            # 返回第一个可用的数据源
            first_source = list(available_sources.values())[0] if available_sources else None
            return first_source
    
    def set_us_data_source_preference(self, source_type: DataSourceType):
        """设置美股数据源偏好"""
        self.us_data_source_preference = source_type
        logger.info(f"设置美股数据源偏好为: {source_type.value}")
    
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票价格"""
        data_source = self.get_data_source_for_market(market_code)
        if data_source:
            return data_source.get_stock_price(code, market_code)
        
        logger.warning(f"没有找到适合市场 {market_code} 的数据源")
        return None, None
    
    def get_fund_nav(self, code: str, market_code: str = None) -> Tuple[Optional[float], Optional[str]]:
        """获取基金净值"""
        if not market_code:
            market_code = self._guess_market_from_code(code)
        
        data_source = self.get_data_source_for_market(market_code)
        if data_source:
            return data_source.get_fund_nav(code, market_code)
        
        logger.warning(f"没有找到适合市场 {market_code} 的数据源")
        return None, None
    
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取汇率（优先使用Akshare）"""
        data_source = self.data_sources.get(DataSourceType.AKSHARE)
        if data_source:
            rate, date = data_source.get_exchange_rate(currency)
            if rate is not None:
                return rate, date
        
        # 如果没有Akshare，尝试其他数据源
        for source_type, source in self.data_sources.items():
            if source_type != DataSourceType.AKSHARE:
                try:
                    rate, date = source.get_exchange_rate(currency)
                    if rate is not None:
                        return rate, date
                except Exception as e:
                    logger.debug(f"数据源 {source_type} 获取汇率失败: {e}")
                    continue
        
        logger.warning(f"没有可用的汇率数据源")
        return None, None
    
    def _guess_market_from_code(self, code: str) -> str:
        """根据代码猜测市场"""
        if not code:
            return "UNKNOWN"
        
        code = str(code).strip()
        
        if code.isdigit() and len(code) == 6:
            if code.startswith(('6', '9', '5')):
                return "SH"
            elif code.startswith(('0', '2', '3')):
                return "SZ"
            elif code.startswith('4'):
                return "BJ"
            elif code.startswith('8'):
                return "OF"  # 场外基金
        elif 1 <= len(code) <= 5 and code.isalpha():
            return "US"
        elif code.isdigit() and len(code) == 5:
            return "HK"
        elif code.endswith('.OF') or (code.isdigit() and len(code) == 6):
            return "OF"  # 场外基金
        
        return "UNKNOWN"
    
    def get_data_source_info(self) -> Dict[str, List[str]]:
        """获取所有数据源信息"""
        info = {}
        for source_type, source in self.data_sources.items():
            info[source.get_name()] = {
                'type': source_type.value,
                'supported_markets': source.get_supported_markets()
            }
        return info
    
    def select_us_data_source_interactive(self) -> bool:
        """交互式选择美股数据源，返回是否选择成功"""
        available_sources = self.get_available_data_sources("US")
        
        if not available_sources:
            print("没有可用的美股数据源")
            return False
        
        print("\n" + "="*50)
        print("请选择美股数据源:")
        
        source_list = list(available_sources.items())
        for i, (source_type, source) in enumerate(source_list, 1):
            print(f"{i}. {source.get_name()}")
        
        print("="*50)
        
        try:
            choice = input(f"请选择 (1-{len(source_list)}, 输入0取消): ").strip()
            
            if choice == "0":
                print("已取消选择")
                return False
            
            choice_idx = int(choice) - 1 if choice.isdigit() else 0
            
            if 0 <= choice_idx < len(source_list):
                selected_type, selected_source = source_list[choice_idx]
                self.us_data_source_preference = selected_type
                print(f"已选择美股数据源: {selected_source.get_name()}")
                return True
            else:
                print("无效的选择")
                return False
                
        except Exception as e:
            logger.error(f"选择数据源时出错: {e}")
            return False
    
    def get_current_us_data_source_info(self) -> str:
        """获取当前美股数据源信息"""
        if self.us_data_source_preference:
            data_source = self.data_sources.get(self.us_data_source_preference)
            if data_source:
                return f"当前美股数据源: {data_source.get_name()}"
        return "当前未设置美股数据源"


# 全局数据源管理器实例
_data_source_manager = None

def get_data_source_manager() -> DataSourceManager:
    """获取数据源管理器实例（单例模式）"""
    global _data_source_manager
    if _data_source_manager is None:
        _data_source_manager = DataSourceManager()
    return _data_source_manager