"""
主数据源模块 - 统一入口
提供向后兼容的接口
"""
import logging
from typing import Optional

# 使用相对导入
from .base_data_source import DataSource, DataSourceType, DataSourceFactory
from .data_source_manager import DataSourceManager, get_data_source_manager

logger = logging.getLogger(__name__)

# 全局数据源管理器实例（单例）
_data_source_manager: Optional[DataSourceManager] = None


def get_data_source() -> DataSourceManager:
    """
    获取数据源管理器（兼容原有代码）
    使用方式：
    - 原有方式: data_source = get_data_source()
    - 新方式: data_source_manager = get_data_source_manager()
    """
    return get_data_source_manager()


def init_data_sources() -> DataSourceManager:
    """
    初始化所有数据源
    """
    global _data_source_manager
    if _data_source_manager is None:
        _data_source_manager = DataSourceManager()
        logger.info("数据源系统初始化完成")
    return _data_source_manager


def get_available_data_sources_info() -> dict:
    """
    获取可用数据源信息
    """
    manager = get_data_source_manager()
    return manager.get_data_source_info()


# 兼容性别名
DataSource = DataSource  # 保持导出
HybridDataSource = DataSourceManager  # 兼容旧名称


if __name__ == "__main__":
    # 测试代码
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("数据源模块测试")
    print("=" * 50)
    
    # 初始化
    manager = init_data_sources()
    
    # 获取信息
    info = get_available_data_sources_info()
    print("可用数据源:")
    for name, details in info.items():
        print(f"  {name}: {details['type']}")
        print(f"    支持市场: {', '.join(details['supported_markets'])}")
    
    print("\n测试完成")