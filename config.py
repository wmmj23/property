# config.py
import os
from pathlib import Path

# 获取当前文件所在目录
BASE_DIR = Path(__file__).parent.absolute()

# 数据库配置
DB_FILE = BASE_DIR / "property.db"
DB_BACKUP_DIR = BASE_DIR / "backups"
DECIMAL_PLACES = 4
# 数据库配置

# 数据源配置
DATA_SOURCE = "akshare"  # 可配置为 'akshare', 'yfinance', '自定义'
AKSHARE_TIMEOUT = 30  # 秒
YFINANCE_TICKER_PREFIX = {
    "US": "",
    "HK": "",
    "SH": "SS",
    "SZ": "SZ",
    "BJ": "BJ"
}

# 程序配置
ENABLE_CACHE = True
CACHE_DURATION = 3600  # 缓存时间（秒）
LOG_LEVEL = "INFO"     # DEBUG, INFO, WARNING, ERROR

# 美股配置
US_MARKET_TZ = "US/Eastern"  # 美股时区
US_DATA_PROVIDER = "yfinance"  # 美股数据提供者

# 文件路径
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

# 创建必要的目录
for directory in [DATA_DIR, LOG_DIR, Path(DB_BACKUP_DIR)]:
    directory.mkdir(exist_ok=True)

# 打印配置信息（调试用）
print(f"数据库文件路径: {DB_FILE}")
print(f"数据库文件存在: {DB_FILE.exists()}")