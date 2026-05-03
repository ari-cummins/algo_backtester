import matplotlib.pyplot as plt
import pandas as pd

def plot_equity_curves(portfolio_ma, portfolio_mr, data, initial_capital):
    """
    Plot portfolio value over time for both strategies vs buy-and-hold.
    
    Args:
        portfolio_ma: DataFrame from MA crossover backtest
        portfolio_mr: DataFrame from mean reversion backtest
        data: Original price data
        initial_capital: Starting capital amount
    """
    # Calculate buy-and-hold portfolio value
    buy_hold = pd.DataFrame({
        'Date': data.index[1:],
        'Total': initial_capital * (data['Close'][1:] / data['Close'].iloc[1])
    })
    
    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_ma['Date'], portfolio_ma['Total'], label='MA Crossover', linewidth=2)
    plt.plot(portfolio_mr['Date'], portfolio_mr['Total'], label='Mean Reversion', linewidth=2)
    plt.plot(buy_hold['Date'], buy_hold['Total'], label='Buy & Hold', linewidth=2, linestyle='--')
    
    plt.axhline(y=initial_capital, color='gray', linestyle=':', alpha=0.5)
    plt.title('Strategy Performance Comparison', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('equity_curves.png', dpi=300)
    print("✓ Saved equity_curves.png")
    plt.close()


def plot_signals(data, trades, strategy_name):
    """
    Plot price chart with buy/sell signals marked.
    
    Args:
        data: DataFrame with price and signal data
        trades: DataFrame with trade log
        strategy_name: Name of strategy for title
    """
    plt.figure(figsize=(14, 7))
    
    # Plot price
    plt.plot(data.index, data['Close'], label='SPY Price', color='black', linewidth=1.5)
    
    # Plot moving averages if they exist
    if 'MA_Short' in data.columns:
        plt.plot(data.index, data['MA_Short'], label='MA 20', alpha=0.7, linewidth=1)
        plt.plot(data.index, data['MA_Long'], label='MA 50', alpha=0.7, linewidth=1)
    elif 'MA' in data.columns:
        plt.plot(data.index, data['MA'], label='MA 20', alpha=0.7, linewidth=1)
    
    # Mark buy signals
    buys = trades[trades['Action'] == 'BUY']
    if not buys.empty:
        plt.scatter(buys['Date'], buys['Price'], color='green', marker='^', 
                   s=100, label='Buy Signal', zorder=5)
    
    # Mark sell signals
    sells = trades[trades['Action'] == 'SELL']
    if not sells.empty:
        plt.scatter(sells['Date'], sells['Price'], color='red', marker='v', 
                   s=100, label='Sell Signal', zorder=5)
    
    plt.title(f'{strategy_name} - Trading Signals on SPY', fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    filename = f"signals_{strategy_name.lower().replace(' ', '_')}.png"
    plt.savefig(filename, dpi=300)
    print(f"✓ Saved {filename}")
    plt.close()


def plot_performance_comparison(metrics_ma, metrics_mr, buy_hold_return):
    """
    Bar chart comparing returns of all strategies.
    
    Args:
        metrics_ma: Metrics dict from MA crossover
        metrics_mr: Metrics dict from mean reversion
        buy_hold_return: Buy-and-hold return %
    """
    strategies = ['MA Crossover', 'Mean Reversion', 'Buy & Hold']
    returns = [metrics_ma['total_return'], metrics_mr['total_return'], buy_hold_return]
    colors = ['#2ecc71' if r > 0 else '#e74c3c' for r in returns]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(strategies, returns, color=colors, alpha=0.7, edgecolor='black')
    
    # Add value labels on bars
    for bar, ret in zip(bars, returns):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{ret:.2f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.axhline(y=0, color='black', linewidth=0.8)
    plt.title('Total Return Comparison - SPY (2024)', fontsize=14, fontweight='bold')
    plt.ylabel('Return (%)')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300)
    print("✓ Saved performance_comparison.png")
    plt.close()