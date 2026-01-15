# 个人资产数据管理系统

一个用于管理个人资产数据的Python应用程序，支持股票、基金、汇率数据的自动获取和存储。

## 功能特点

1. **多数据源支持**
   - A股数据：使用 akshare 获取
   - 美股数据：使用 yfinance 获取
   - 基金数据：使用 akshare 获取
   - 汇率数据：使用 akshare 获取

2. **模块化设计**
   - 数据源抽象层，便于更换数据源
   - 数据库操作封装
   - 功能模块分离

3. **美股数据处理**
   - 专门的美股数据源类
   - 获取美股详细信息（行业、市值、PE等）
   - 自动更新美股备注信息

4. **用户友好界面**
   - 清晰的菜单导航
   - 进度显示
   - 错误处理

## 安装说明

### 1. 安装依赖
```bash
python -m pip install -r requirements.txt


### 2. 创建数据库
# 使用提供的SQL文件创建数据库
sqlite3 propertyTables.sqlite < propertyTables.sql

### 3. 运行
python main.py

项目目录
personal_assets/
├── main.py              # 主程序入口
├── config.py           # 配置参数
├── data_source.py      # 数据源抽象和实现
├── database.py         # 数据库操作
├── fetcher.py          # 数据获取功能
├── utils.py           # 工具函数
├── menu.py            # 菜单界面
├── requirements.txt   # 依赖列表
└── README.md         # 说明文档