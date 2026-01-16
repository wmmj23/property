# menu_functions/__init__.py
from .fetch_stock_prices import main as fetch_stock_prices
from .fetch_fund_navs import main as fetch_fund_navs
from .fetch_exchange_rates import main as fetch_exchange_rates
from .fetch_us_stocks import main as fetch_us_stocks
from .fetch_all_data import main as fetch_all_data
from .view_stock_info import main as view_stock_info
from .view_fund_info import main as view_fund_info
from .view_exchange_info import main as view_exchange_info
from .database_management import main as database_management

__all__ = [
    'fetch_stock_prices',
    'fetch_fund_navs',
    'fetch_exchange_rates',
    'fetch_us_stocks',
    'fetch_all_data',
    'view_stock_info',
    'view_fund_info',
    'view_exchange_info',
    'database_management'
]