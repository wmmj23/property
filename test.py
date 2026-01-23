import akshare as ak
from datetime import datetime, timedelta

# stock_us_spot_em_df = ak.stock_us_spot_em()
# print(stock_us_spot_em_df)

# stock_us_hist_df = ak.stock_us_hist(symbol='MTP', start_date="22220101", end_date="22220102", adjust="qfq")


# print(stock_us_hist_df)

# df = ak.stock_us_daily(symbol='AAPL')

# latest = df.iloc[-1]
# price = round(float(latest['close']), 4)
# date = latest['date'].strftime('%Y-%m-%d')

# print(df)
# print(date)

# df = ak.fund_open_fund_daily_em()
# print(df)

# fund_open_fund_info_em_df = ak.fund_open_fund_info_em(symbol="563900", indicator="单位净值走势", period="1月")
# print(fund_open_fund_info_em_df)

# currency = "HKD"
# df = ak.currency_boc_safe()

# if df is not None and not df.empty:
#     latest = df.iloc[-1]
#     if currency == "USD":
#         rate = round(float(latest['美元']/100), 4)
#         date = latest['日期'].strftime('%Y-%m-%d')
#     if currency == "HKD":
#         rate = round(float(latest['港元']/100), 4)
#         date = latest['日期'].strftime('%Y-%m-%d')
# print(rate)
# print(date)

yesterday = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
today = datetime.now().strftime('%Y%m%d')
df = ak.stock_zh_a_hist(
    symbol='002407', 
    period="daily", 
    start_date=yesterday,
    end_date=today,
    adjust="qfq"
)
print(df)



# df = ak.stock_zh_a_daily(symbol="sh601398", adjust="qfq")
# print(df)
