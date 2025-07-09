# main.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from simulator import LPSimulator

# --- Configuration ---
COIN_ID = 'ethereum'
DATA_FILE = f"{COIN_ID}_data.csv"
INITIAL_INVESTMENT = 10000  # in USD
FEE_TIER = 0.003  # 0.3% fee, common for volatile pairs
DAILY_VOLUME_PERCENTAGE = 0.10 # Assume daily volume is 10% of liquidity

def analyze_and_plot(results):
    """
    Analyzes the simulation results and generates plots.
    """
    print("\n--- Simulation Results ---")
    
    # Final values
    final_hodl_value = results['hodl_value'].iloc[-1]
    final_lp_value = results['total_lp_value'].iloc[-1]
    
    # P&L
    hodl_pnl = (final_hodl_value - INITIAL_INVESTMENT) / INITIAL_INVESTMENT * 100
    lp_pnl = (final_lp_value - INITIAL_INVESTMENT) / INITIAL_INVESTMENT * 100
    
    print(f"Initial Investment: ${INITIAL_INVESTMENT:,.2f}")
    print(f"Final HODL Value:   ${final_hodl_value:,.2f} (P&L: {hodl_pnl:.2f}%)")
    print(f"Final LP Value:     ${final_lp_value:,.2f} (P&L: {lp_pnl:.2f}%)")
    
    final_il = results['impermanent_loss'].iloc[-1]
    final_fees = results['fees_earned'].iloc[-1]
    print(f"Total Impermanent Loss: ${final_il:,.2f}")
    print(f"Total Fees Earned:      ${final_fees:,.2f}")
    print(f"LP performance vs HODL: {final_lp_value - final_hodl_value:,.2f}")
    
    # --- Plotting ---
    sns.set_style("whitegrid")
    plt.figure(figsize=(14, 7))
    
    # Plot 1: Portfolio Value Comparison
    plt.subplot(2, 1, 1)
    plt.plot(results.index, results['hodl_value'], label='HODL Strategy Value')
    plt.plot(results.index, results['total_lp_value'], label='LP Strategy Value (incl. Fees)')
    plt.title('HODL vs. Liquidity Provision Strategy Performance')
    plt.ylabel('Portfolio Value (USD)')
    plt.legend()
    
    # Plot 2: Impermanent Loss vs. Fees Earned
    plt.subplot(2, 1, 2)
    plt.plot(results.index, results['fees_earned'], label='Cumulative Fees Earned', color='green')
    plt.plot(results.index, -results['impermanent_loss'], label='Impermanent Loss (as a positive value)', color='red', linestyle='--')
    plt.title('Impermanent Loss vs. Cumulative Fees Earned')
    plt.ylabel('Value (USD)')
    plt.xlabel('Date')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('simulation_results.png')
    print("\nPlots saved to simulation_results.png")
    plt.show()

if __name__ == '__main__':
    # Load data
    try:
        data = pd.read_csv(DATA_FILE, index_col='date', parse_dates=True)
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE}")
        print("Please run data_fetcher.py first.")
        exit()
        
    # Initialize and run the simulator
    simulator = LPSimulator(data, INITIAL_INVESTMENT, FEE_TIER, DAILY_VOLUME_PERCENTAGE)
    results_df = simulator.run_simulation()
    
    # Analyze and plot
    analyze_and_plot(results_df)