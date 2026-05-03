import argparse
from data.loader import load_stock_data
from strategies import ma_crossover, mean_reversion
from engine.backtest import run_backtest
from utils.visualize import plot_equity_curves, plot_signals, plot_performance_comparison

def main():
    # Command-line argument parsing
    parser = argparse.ArgumentParser(description='Algorithmic Trading Backtester')
    parser.add_argument('--ticker', type=str, default='SPY', help='Stock ticker symbol')
    parser.add_argument('--start', type=str, default='2024-01-01', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', type=str, default='2025-01-01', help='End date (YYYY-MM-DD)')
    parser.add_argument('--capital', type=float, default=10000, help='Initial capital')
    parser.add_argument('--strategy', type=str, choices=['ma', 'mr', 'both'], default='both',
                       help='Strategy: ma (MA Crossover), mr (Mean Reversion), both (compare)')
    args = parser.parse_args()
    
    # Load data
    print(f"\nLoading {args.ticker} data from {args.start} to {args.end}...")
    data = load_stock_data(args.ticker, args.start, args.end)
    
    if data.empty:
        print(f"Error: No data found for {args.ticker}")
        return
    
    # Calculate buy-and-hold return
    buy_hold_return = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / 
                       data['Close'].iloc[0] * 100)
    
    results = {}
    
    # Run MA Crossover
    if args.strategy in ['ma', 'both']:
        print("\n=== MOVING AVERAGE CROSSOVER ===")
        data_ma = ma_crossover.generate_signals(data, short_window=20, long_window=50)
        trades_ma, portfolio_ma, metrics_ma = run_backtest(data_ma, args.capital)
        
        print(f"Final Value: ${metrics_ma['final_value']:,.2f}")
        print(f"Total Return: {metrics_ma['total_return']:.2f}%")
        print(f"Max Drawdown: {metrics_ma['max_drawdown']:.2f}%")
        print(f"Number of Trades: {metrics_ma['num_trades']}")
        
        results['ma'] = (data_ma, trades_ma, portfolio_ma, metrics_ma)
    
    # Run Mean Reversion
    if args.strategy in ['mr', 'both']:
        print("\n=== MEAN REVERSION ===")
        data_mr = mean_reversion.generate_signals(data, window=20, threshold=0.02)
        trades_mr, portfolio_mr, metrics_mr = run_backtest(data_mr, args.capital)
        
        print(f"Final Value: ${metrics_mr['final_value']:,.2f}")
        print(f"Total Return: {metrics_mr['total_return']:.2f}%")
        print(f"Max Drawdown: {metrics_mr['max_drawdown']:.2f}%")
        print(f"Number of Trades: {metrics_mr['num_trades']}")
        
        results['mr'] = (data_mr, trades_mr, portfolio_mr, metrics_mr)
    
    # Print comparison
    print(f"\n=== COMPARISON ===")
    if 'ma' in results:
        print(f"MA Crossover: {results['ma'][3]['total_return']:.2f}%")
    if 'mr' in results:
        print(f"Mean Reversion: {results['mr'][3]['total_return']:.2f}%")
    print(f"Buy & Hold: {buy_hold_return:.2f}%")
    
    # Generate visualizations if comparing both
    if args.strategy == 'both' and 'ma' in results and 'mr' in results:
        print("\nGenerating visualizations...")
        plot_equity_curves(results['ma'][2], results['mr'][2], data, args.capital)
        plot_signals(results['ma'][0], results['ma'][1], "MA Crossover")
        plot_signals(results['mr'][0], results['mr'][1], "Mean Reversion")
        plot_performance_comparison(results['ma'][3], results['mr'][3], buy_hold_return)
        print("\n✓ Charts saved")
    
    # Save trade logs
    if 'ma' in results:
        results['ma'][1].to_csv(f'trades_ma_{args.ticker}.csv', index=False)
    if 'mr' in results:
        results['mr'][1].to_csv(f'trades_mr_{args.ticker}.csv', index=False)
    
    print(f"\n✓ Backtest complete for {args.ticker}")

if __name__ == "__main__":
    main()