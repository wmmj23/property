# base_data_source.py
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple, Dict, Any, List
import logging
import sys
import os

logger = logging.getLogger(__name__)


class DataSourceType(Enum):
    """数据源类型枚举"""
    AKSHARE = "akshare"
    YFINANCE = "yfinance"
    ALPHA_VANTAGE = "alpha_vantage"


class DataSource(ABC):
    """数据源抽象基类"""
    
    @abstractmethod
    def get_stock_price(self, code: str, market_code: str) -> Tuple[Optional[float], Optional[str]]:
        """获取股票最新收盘价和日期"""
        pass
    
    @abstractmethod
    def get_fund_nav(self, code: str, market_code: str = None) -> Tuple[Optional[float], Optional[str]]:
        """获取基金最新净值和日期"""
        pass
    
    @abstractmethod
    def get_exchange_rate(self, currency: str) -> Tuple[Optional[float], Optional[str]]:
        """获取货币兑换人民币的汇率和日期"""
        pass
    
    @abstractmethod
    def get_data_source_type(self) -> DataSourceType:
        """获取数据源类型"""
        pass
    
    @abstractmethod
    def get_supported_markets(self) -> List[str]:
        """获取支持的市场列表"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """获取数据源名称"""
        pass


class DataSourceFactory:
    """数据源工厂类"""
    
    @staticmethod
    def create_data_source(source_type: DataSourceType, **kwargs) -> DataSource:
        """创建数据源实例"""
        if source_type == DataSourceType.AKSHARE:
            # 动态导入以避免循环导入
            module_name = "data_sources.akshare_data_source"
            if module_name in sys.modules:
                # 如果模块已经导入，直接从sys.modules获取
                module = sys.modules[module_name]
            else:
                # 否则导入模块
                from . import akshare_data_source as module
            
            return module.AkshareDataSource(**kwargs)
        elif source_type == DataSourceType.YFINANCE:
            module_name = "data_sources.yfinance_data_source"
            if module_name in sys.modules:
                module = sys.modules[module_name]
            else:
                from . import yfinance_data_source as module
            
            return module.YFinanceDataSource(**kwargs)
        elif source_type == DataSourceType.ALPHA_VANTAGE:
            module_name = "data_sources.alpha_vantage_data_source"
            if module_name in sys.modules:
                module = sys.modules[module_name]
            else:
                from . import alpha_vantage_data_source as module
            
            return module.AlphaVantageDataSource(**kwargs)
        else:
            raise ValueError(f"不支持的数据源类型: {source_type}")