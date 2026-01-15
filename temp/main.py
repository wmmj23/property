# main.py
#!/usr/bin/env python3
"""
个人资产数据管理系统 - 主程序入口
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from utils import setup_logging, print_header, print_error
from config import LOG_LEVEL
from menu import MenuSystem


def check_dependencies():
    """检查依赖"""
    try:
        import akshare
        print_success("✓ akshare 已安装")
    except ImportError:
        print_error("✗ akshare 未安装，请运行: pip install akshare")
        return False
    
    try:
        import yfinance
        print_success("✓ yfinance 已安装")
    except ImportError:
        print_warning("⚠ yfinance 未安装，美股功能可能受限")
        print_info("  如需完整功能，请运行: pip install yfinance")
    
    try:
        import pandas
        print_success("✓ pandas 已安装")
    except ImportError:
        print_error("✗ pandas 未安装，请运行: pip install pandas")
        return False
    
    return True


def check_database():
    """检查数据库"""
    from config import DB_FILE
    
    if not os.path.exists(DB_FILE):
        print_error(f"✗ 数据库文件 {DB_FILE} 不存在")
        print_info("  请先使用 propertyTables.sql 创建数据库")
        print_info("  命令: sqlite3 propertyTables.sqlite < propertyTables.sql")
        return False
    
    print_success(f"✓ 数据库文件 {DB_FILE} 存在")
    return True


def print_success(message: str):
    """打印成功信息"""
    print(f"\033[92m{message}\033[0m")


def print_error(message: str):
    """打印错误信息"""
    print(f"\033[91m{message}\033[0m")


def print_warning(message: str):
    """打印警告信息"""
    print(f"\033[93m{message}\033[0m")


def print_info(message: str):
    """打印信息"""
    print(f"\033[94m{message}\033[0m")


def main():
    """主函数"""
    # 设置日志
    setup_logging(LOG_LEVEL)
    
    print_header("个人资产数据管理系统 - 启动检查", 70)
    
    # 检查依赖
    print("\n检查依赖库...")
    if not check_dependencies():
        print_error("依赖检查失败，程序退出")
        sys.exit(1)
    
    # 检查数据库
    print("\n检查数据库...")
    if not check_database():
        print_error("数据库检查失败，程序退出")
        sys.exit(1)
    
    print("\n" + "="*70)
    print_success("所有检查通过，正在启动程序...")
    print("="*70)
    
    # 运行菜单系统
    try:
        menu_system = MenuSystem()
        menu_system.run()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print_error(f"程序运行出错: {e}")
        logging.exception("程序运行异常")
    finally:
        print("\n感谢使用个人资产数据管理系统！")


if __name__ == "__main__":
    main()