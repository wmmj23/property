"""
数据源模块包
提供多种金融数据源的统一接口
"""

# 在包级别，我们需要使用相对导入
from .base_data_source import DataSource, DataSourceType, DataSourceFactory
from .data_source_manager import DataSourceManager, get_data_source_manager
from .main_data_source import get_data_source

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    'DataSource',
    'DataSourceType', 
    'DataSourceFactory',
    'DataSourceManager',
    'get_data_source_manager',
    'get_data_source'
]