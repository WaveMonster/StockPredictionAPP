import yfinance as yf
import pandas as pd
import requests

class YahooFinanceDataFetcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_stock_history(self, ticker, period="1y", interval="1d"):
        """获取股票历史数据"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period, interval=interval)
            return hist
        except Exception as e:
            print(f"获取 {ticker} 历史数据时出错: {e}")
            return pd.DataFrame()

    def get_company_info(self, ticker):
        """获取公司基本信息"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            return info
        except Exception as e:
            print(f"获取 {ticker} 公司信息时出错: {e}")
            return {}

    def get_financials(self, ticker):
        """获取公司财务报表 (年报和季报)"""
        try:
            stock = yf.Ticker(ticker)
            financials = {
                'income_stmt': stock.financials,
                'balance_sheet': stock.balance_sheet,
                'cash_flow': stock.cashflow,
                'quarterly_income_stmt': stock.quarterly_financials,
                'quarterly_balance_sheet': stock.quarterly_balance_sheet,
                'quarterly_cash_flow': stock.quarterly_cashflow
            }
            return financials
        except Exception as e:
            print(f"获取 {ticker} 财务报表时出错: {e}")
            return {}

    def get_key_stats(self, ticker):
        """
        获取关键统计数据。
        `yfinance`的`info`对象已经包含了大部分关键统计数据。
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            # 从info字典中提取我们关心的关键统计数据
            key_stats = {
                'Market Cap': info.get('marketCap'),
                'Forward P/E': info.get('forwardPE'),
                'Trailing P/E': info.get('trailingPE'),
                'PEG Ratio': info.get('pegRatio'),
                'Price/Sales': info.get('priceToSalesTrailing12Months'),
                'Price/Book': info.get('priceToBook'),
                'EPS TTM': info.get('trailingEps'),
                'Beta': info.get('beta'),
                'Dividend Yield': info.get('dividendYield'),
                'Revenue Growth (YoY)': info.get('revenueGrowth'),
                'Profit Margins': info.get('profitMargins')
            }
            return key_stats
        except Exception as e:
            print(f"获取 {ticker} 关键统计数据时出错: {e}")
            return {}

    def search_ticker(self, company_name):
        """根据公司名称搜索股票代码"""
        search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}&quotesCount=1&newsCount=0"
        try:
            response = requests.get(search_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data and 'quotes' in data and len(data['quotes']) > 0:
                return data['quotes'][0]['symbol']
            return None
        except Exception as e:
            print(f"为 {company_name} 搜索代码时出错: {e}")
            return None

        # 在 data_fetcher.py 的 YahooFinanceDataFetcher 类中添加此方法

    def get_current_yield(self, ticker="^TNX"):
        """获取指定代码的当前收益率/价格，默认为美国10年期国债收益率"""
        try:
            # 获取最近5天的数据足以找到最新收盘价
            data = yf.Ticker(ticker).history(period="5d")
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"获取 {ticker} 的当前收益率时出错: {e}")
            return None