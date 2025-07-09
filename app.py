# app.py

import streamlit as st
import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Import your existing simulator class
from simulator import LPSimulator

# --- Page Configuration ---
st.set_page_config(
    page_title="DeFi LP Strategy Simulator",
    page_icon="💸",
    layout="wide"
)

# --- Caching ---
# @st.cache_data is a Streamlit decorator that caches the output of a function.
# This means that when the user changes a slider, the app won't re-download
# the data from the API, making it much faster.
@st.cache_data
def fetch_data(coin_id, vs_currency, days):
    """
    Fetches historical market data for a given coin from CoinGecko.
    This function is cached to avoid repeated API calls.
    """
    cg = CoinGeckoAPI()
    to_ts = time.time()
    from_ts = to_ts - days * 86400

    try:
        market_data = cg.get_coin_market_chart_range_by_id(
            id=coin_id,
            vs_currency=vs_currency,
            from_timestamp=from_ts,
            to_timestamp=to_ts
        )
        prices = market_data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df = df.set_index('date')[['price']]
        return df
    except Exception as e:
        st.error(f"Could not fetch data for {coin_id}. Error: {e}")
        return None

def plot_results(results_df):
    """Generates and returns the matplotlib figure for plotting."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    sns.set_style("whitegrid")
    
    # Plot 1: Portfolio Value Comparison
    ax1.plot(results_df.index, results_df['hodl_value'], label='HODL Strategy Value')
    ax1.plot(results_df.index, results_df['total_lp_value'], label='LP Strategy Value (incl. Fees)')
    ax1.set_title('HODL vs. Liquidity Provision Strategy Performance', fontsize=16)
    ax1.set_ylabel('Portfolio Value (USD)')
    ax1.legend()
    ax1.grid(True)
    
    # Plot 2: Impermanent Loss vs. Fees Earned
    ax2.plot(results_df.index, results_df['fees_earned'], label='Cumulative Fees Earned', color='green')
    ax2.plot(results_df.index, -results_df['impermanent_loss'], label='Impermanent Loss (as a positive value)', color='red', linestyle='--')
    ax2.set_title('Impermanent Loss vs. Cumulative Fees Earned', fontsize=16)
    ax2.set_ylabel('Value (USD)')
    ax2.set_xlabel('Date')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

# --- Main App ---

st.title("💸 DeFi Liquidity Pool (LP) Strategy Simulator")
st.markdown("Analyze the performance of providing liquidity to a DEX compared to just holding the assets.")

# --- Sidebar for User Inputs ---
st.sidebar.header("Simulation Parameters")

# Dictionary to map user-friendly names to CoinGecko IDs
CRYPTO_OPTIONS = {
    "Ethereum (ETH)": "ethereum",
    "Bitcoin (BTC)": "bitcoin",
    "Solana (SOL)": "solana",
    "Dogecoin (DOGE)": "dogecoin"
}
selected_crypto_name = st.sidebar.selectbox("Select Cryptocurrency:", options=list(CRYPTO_OPTIONS.keys()))
coin_id = CRYPTO_OPTIONS[selected_crypto_name]

# Slider for initial investment
initial_investment = st.sidebar.slider(
    "Initial Investment (USD)",
    min_value=1000,
    max_value=100000,
    value=10000, # Default value
    step=1000,
    format="$%d"
)

# Sliders for fee and volume assumptions
fee_tier = st.sidebar.slider(
    "Trading Fee Tier (%)",
    min_value=0.01,
    max_value=1.0,
    value=0.30, # Default value for volatile pairs
    step=0.01
) / 100 # Convert percentage to decimal

daily_volume_percentage = st.sidebar.slider(
    "Estimated Daily Volume (% of Liquidity)",
    min_value=1.0,
    max_value=100.0,
    value=10.0, # Default assumption
    step=1.0
) / 100 # Convert percentage to decimal


# --- Data Loading and Simulation ---
data = fetch_data(coin_id=coin_id, vs_currency='usd', days=365)

if data is not None and not data.empty:
    # Calculate annualized volatility
    daily_returns = data['price'].pct_change()
    volatility = daily_returns.std() * (365**0.5) # Annualized volatility

    st.header(f"Results for {selected_crypto_name}")

    # Initialize and run the simulator
    simulator = LPSimulator(data, initial_investment, fee_tier, daily_volume_percentage)
    results_df = simulator.run_simulation()
    
    # --- Display Metrics ---
    final_hodl_value = results_df['hodl_value'].iloc[-1]
    final_lp_value = results_df['total_lp_value'].iloc[-1]
    total_fees = results_df['fees_earned'].iloc[-1]
    total_il = results_df['impermanent_loss'].iloc[-1]
    
    lp_vs_hodl_diff = final_lp_value - final_hodl_value

    # Find the st.columns line and replace it with this:
    col1, col2, col3, col4 = st.columns(4) # Changed from 3 to 4 columns

    col1.metric("Final HODL Value", f"${final_hodl_value:,.2f}", f"{(final_hodl_value - initial_investment):,.2f}")
    col2.metric("Final LP Value", f"${final_lp_value:,.2f}", f"{(final_lp_value - initial_investment):,.2f}")
    col3.metric("LP vs HODL", f"${lp_vs_hodl_diff:,.2f}", f"{(lp_vs_hodl_diff / final_hodl_value * 100):.2f}%")
    # Add the new volatility metric
    col4.metric("Annualized Volatility", f"{volatility:.2%}")

    # The corrected line
    st.info(f"Over the period, the LP strategy collected **${total_fees:,.2f}** in fees, while experiencing **${total_il:,.2f}** in impermanent loss.")

    # --- Display Plots ---
    st.subheader("Performance Over Time")
    fig = plot_results(results_df)
    st.pyplot(fig)

    # --- Show Raw Data (Optional) ---
    with st.expander("Show Raw Simulation Data"):
        st.dataframe(results_df)

else:
    st.warning("Please select a cryptocurrency to begin the simulation.")