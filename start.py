# start.py - 更简单的启动脚本
#!/usr/bin/env python3
"""
个人资产数据管理系统 - 简单启动脚本
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def check_requirements():
    """检查必要的库"""
    required_libs = ['akshare', 'pandas', 'sqlite3']
    missing_libs = []
    
    for lib in required_libs:
        try:
            if lib == 'sqlite3':
                # sqlite3 是Python内置的
                import sqlite3
            else:
                __import__(lib)
            print(f"✓ {lib} 可用")
        except ImportError:
            if lib != 'sqlite3':  # sqlite3应该总是可用的
                missing_libs.append(lib)
                print(f"✗ {lib} 未安装")
    
    return missing_libs

def check_database():
    """检查数据库文件"""
    from config import DB_FILE
    
    if not DB_FILE.exists():
        print(f"✗ 数据库文件不存在: {DB_FILE}")
        print("请先使用 propertyTables.sql 创建数据库:")
        print(f"  sqlite3 {DB_FILE} < propertyTables.sql")
        return False
    
    print(f"✓ 数据库文件存在: {DB_FILE}")
    return True

def main():
    """主函数"""
    print("=" * 70)
    print("个人资产数据管理系统")
    print("=" * 70)
    
    # 检查依赖
    print("\n检查依赖库...")
    missing = check_requirements()
    
    if missing:
        print(f"\n缺少以下依赖库: {', '.join(missing)}")
        print("请运行: pip install " + " ".join(missing))
        input("\n按回车键退出...")
        sys.exit(1)
    
    # 检查数据库
    print("\n检查数据库...")
    if not check_database():
        input("\n按回车键退出...")
        sys.exit(1)
    
    # 导入主程序
    try:
        print("\n导入模块...")
        from utils import setup_logging
        from menu import MenuSystem
        
        # 设置日志
        print("初始化日志系统...")
        setup_logging("INFO")
        
        # 运行程序
        print("\n" + "=" * 70)
        print("启动主程序...")
        print("=" * 70)
        
        menu_system = MenuSystem()
        menu_system.run()
        
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n感谢使用个人资产数据管理系统！")

if __name__ == "__main__":
    main()