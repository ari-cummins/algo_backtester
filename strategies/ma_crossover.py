import pandas as pd

def generate_signals(data, short_window=20, long_window=50):
    """
    Generate trading signals based on moving average crossover.
    
    Args:
        data: DataFrame with 'Close' column
        short_window: Short-term MA period (default 20)
        long_window: Long-term MA period (default 50)
    
    Returns:
        DataFrame with added MA columns and Signal column
    """
    df = data.copy()
    
    # Calculate moving averages
    df['MA_Short'] = df['Close'].rolling(window=short_window).mean()
    df['MA_Long'] = df['Close'].rolling(window=long_window).mean()
    
    # Generate signals: 1 = buy, 0 = sell/hold cash
    df['Signal'] = 0
    df.loc[df['MA_Short'] > df['MA_Long'], 'Signal'] = 1
    
    return df