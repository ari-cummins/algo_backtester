import yfinance as yf
import pandas as pd

def load_stock_data(ticker, start_date, end_date):
    """
    Download historical stock data from Yahoo Finance.
    
    Args:
        ticker: Stock symbol (e.g., 'SPY')
        start_date: Start date as string 'YYYY-MM-DD'
        end_date: End date as string 'YYYY-MM-DD'
    
    Returns:
        DataFrame with OHLCV data
    """
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    # Flatten multi-index columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    return data