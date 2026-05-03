import pandas as pd

def generate_signals(data, window=20, threshold=0.02):
    """
    Generate trading signals based on mean reversion.
    
    Buy when price drops >threshold below moving average.
    Sell when price returns to or above moving average.
    
    Args:
        data: DataFrame with 'Close' column
        window: Period for calculating moving average (default 20)
        threshold: % below MA to trigger buy (default 0.02 = 2%)
    
    Returns:
        DataFrame with added MA column and Signal column
    """
    df = data.copy()
    
    # Calculate moving average
    df['MA'] = df['Close'].rolling(window=window).mean()
    
    # Calculate % deviation from MA
    df['Deviation'] = (df['Close'] - df['MA']) / df['MA']
    
    # Generate signals
    df['Signal'] = 0
    # Buy when price is >threshold% below MA
    df.loc[df['Deviation'] < -threshold, 'Signal'] = 1
    
    return df