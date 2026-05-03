import pandas as pd

def run_backtest(data, initial_capital=10000):
    """
    Execute backtest based on signals in data.
    
    Args:
        data: DataFrame with 'Close' and 'Signal' columns
        initial_capital: Starting cash amount
    
    Returns:
        tuple: (trades_df, portfolio_df, metrics_dict)
    """
    cash = initial_capital
    position = 0
    portfolio_value = []
    trades = []
    
    for i in range(1, len(data)):
        date = data.index[i]
        price = float(data['Close'].iloc[i])
        signal = int(data['Signal'].iloc[i])
        prev_signal = int(data['Signal'].iloc[i-1])
        
        # BUY signal
        if signal == 1 and prev_signal == 0 and cash > 0:
            shares_to_buy = int(cash // price)
            if shares_to_buy > 0:
                position += shares_to_buy
                cash -= shares_to_buy * price
                trades.append({
                    'Date': date,
                    'Action': 'BUY',
                    'Price': price,
                    'Shares': shares_to_buy,
                    'Cash': cash,
                    'Position': position
                })
        
        # SELL signal
        elif signal == 0 and prev_signal == 1 and position > 0:
            cash += position * price
            trades.append({
                'Date': date,
                'Action': 'SELL',
                'Price': price,
                'Shares': position,
                'Cash': cash,
                'Position': 0
            })
            position = 0
        
        # Track portfolio value
        portfolio_value.append({
            'Date': date,
            'Cash': cash,
            'Position_Value': position * price,
            'Total': cash + position * price
        })
    
    trades_df = pd.DataFrame(trades)
    portfolio_df = pd.DataFrame(portfolio_value)
    
    # Calculate metrics
    final_value = portfolio_df['Total'].iloc[-1]
    total_return = (final_value - initial_capital) / initial_capital * 100
    max_drawdown = ((portfolio_df['Total'].cummax() - portfolio_df['Total']) / 
                    portfolio_df['Total'].cummax()).max() * 100
    
    metrics = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return': total_return,
        'max_drawdown': max_drawdown,
        'num_trades': len(trades_df)
    }
    
    return trades_df, portfolio_df, metrics