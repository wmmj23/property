# utils.py
import os
import sys
import logging
from datetime import datetime
from typing import Any, Optional
import json

logger = logging.getLogger(__name__)


def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title: str, width: int = 60):
    """打印标题"""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def print_success(message: str):
    """打印成功信息"""
    print(f"✓ {message}")


def print_error(message: str):
    """打印错误信息"""
    print(f"✗ {message}")


def print_warning(message: str):
    """打印警告信息"""
    print(f"⚠ {message}")


def print_info(message: str):
    """打印信息"""
    print(f"ℹ {message}")


def format_number(number: float, decimal_places: int = 4) -> str:
    """格式化数字，保留指定小数位"""
    if number is None:
        return "N/A"
    
    try:
        return f"{number:.{decimal_places}f}"
    except (ValueError, TypeError):
        return str(number)


def format_currency(amount: float, currency: str = "CNY") -> str:
    """格式化货币金额"""
    if amount is None:
        return "N/A"
    
    symbols = {
        "CNY": "¥",
        "USD": "$",
        "HKD": "HK$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥"
    }
    
    symbol = symbols.get(currency, currency)
    return f"{symbol}{format_number(amount)}"


def format_percentage(value: float, decimal_places: int = 2) -> str:
    """格式化百分比"""
    if value is None:
        return "N/A"
    
    try:
        return f"{value:.{decimal_places}%}"
    except (ValueError, TypeError):
        return str(value)


def get_user_choice(prompt: str, valid_choices: list) -> str:
    """获取用户选择"""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        else:
            print_error(f"无效选择，请从 {valid_choices} 中选择")


def confirm_action(prompt: str = "确定要执行此操作吗？") -> bool:
    """确认操作"""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes', '是']:
            return True
        elif response in ['n', 'no', '否']:
            return False
        else:
            print_error("请输入 y/n 或 是/否")


def save_to_json(data: Any, filename: str):
    """保存数据到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"数据已保存到 {filename}")
    except Exception as e:
        logger.error(f"保存数据到 {filename} 失败: {e}")


def load_from_json(filename: str) -> Optional[Any]:
    """从JSON文件加载数据"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"从 {filename} 加载数据失败: {e}")
    return None


def get_timestamp() -> str:
    """获取时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def calculate_percentage_change(old_value: float, new_value: float) -> Optional[float]:
    """计算百分比变化"""
    if old_value is None or new_value is None or old_value == 0:
        return None
    
    try:
        return (new_value - old_value) / old_value
    except (ValueError, TypeError, ZeroDivisionError):
        return None


def validate_stock_code(code: str, market: str) -> bool:
    """验证股票代码格式"""
    if not code or not isinstance(code, str):
        return False
    
    code = code.strip()
    
    if market == "SH":
        return code.isdigit() and len(code) == 6 and code.startswith(('6', '9', '5'))
    elif market == "SZ":
        return code.isdigit() and len(code) == 6 and code.startswith(('0', '2', '3'))
    elif market == "BJ":
        return code.isdigit() and len(code) == 6 and code.startswith('4')
    elif market == "US":
        # 美股代码通常是1-5个字母
        return 1 <= len(code) <= 5 and code.isalpha()
    elif market == "HK":
        # 港股代码通常是5位数字
        return code.isdigit() and len(code) == 5
    
    return True  # 其他市场不验证


def setup_logging(log_level: str = "INFO"):
    """设置日志"""
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }
    
    level = log_levels.get(log_level.upper(), logging.INFO)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/app_{get_timestamp()}.log"),
            logging.StreamHandler()
        ]
    )

def safe_format(value: Any, format_str: str = "{}", default: str = "N/A") -> str:
    """安全地格式化值，避免 None 导致的错误"""
    if value is None:
        return default
    try:
        return format_str.format(value)
    except (ValueError, TypeError, AttributeError):
        try:
            return str(value)
        except:
            return default


def print_table(headers: list, rows: list, column_widths: Optional[list] = None):
    """打印表格"""
    if not rows:
        print("暂无数据")
        return
    
    # 如果未指定列宽，自动计算
    if column_widths is None:
        column_widths = []
        for i, header in enumerate(headers):
            # 获取该列所有数据中最大的长度
            max_len = len(str(header))
            for row in rows:
                if i < len(row):
                    cell_len = len(safe_format(row[i]))
                    max_len = max(max_len, cell_len)
            column_widths.append(max_len + 2)  # 加2个空格作为边距
    
    # 打印表头
    header_line = ""
    for i, header in enumerate(headers):
        width = column_widths[i] if i < len(column_widths) else 15
        header_line += f"{safe_format(header):<{width}}"
    print(header_line)
    print("-" * len(header_line))
    
    # 打印数据行
    for row in rows:
        row_line = ""
        for i, cell in enumerate(row):
            width = column_widths[i] if i < len(column_widths) else 15
            row_line += f"{safe_format(cell):<{width}}"
        print(row_line)


def setup_logging(log_level: str = "INFO"):
    """设置日志"""
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR
    }
    
    level = log_levels.get(log_level.upper(), logging.INFO)
    
    # 确保日志目录存在
    from config import LOG_DIR
    LOG_DIR.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_DIR / f"app_{get_timestamp()}.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )