from .fetch_stock_prices import main as fetch_stock_prices_main
from .fetch_fund_navs import main as fetch_fund_navs_main
from .fetch_exchange_rates import main as fetch_exchange_rates_main
from .fetch_us_stocks import main as fetch_us_stocks_main
from .fetch_all_data import main as fetch_all_data_main
from .view_stock_info import main as view_stock_info_main
from .view_fund_info import main as view_fund_info_main
from .view_exchange_info import main as view_exchange_info_main
from .database_management import main as database_management_main

# 提供别名以便向后兼容
fetch_stock_prices = fetch_stock_prices_main
fetch_fund_navs = fetch_fund_navs_main
fetch_exchange_rates = fetch_exchange_rates_main
fetch_us_stocks = fetch_us_stocks_main
fetch_all_data = fetch_all_data_main
view_stock_info = view_stock_info_main
view_fund_info = view_fund_info_main
view_exchange_info = view_exchange_info_main
database_management = database_management_main

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