# data_fetcher.py
import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime

def fetch_and_save_data(coin_id, vs_currency, days):
    """
    Fetches historical market data for a given coin from CoinGecko and saves it to a CSV file.

    Args:
        coin_id (str): The ID of the coin on CoinGecko (e.g., 'ethereum').
        vs_currency (str): The currency to compare against (e.g., 'usd').
        days (int): The number of days of historical data to fetch.
    """
    cg = CoinGeckoAPI()
    
    # Calculate timestamps
    to_ts = time.time()
    from_ts = to_ts - days * 86400  # 86400 seconds in a day

    print(f"Fetching data for {coin_id} from {datetime.fromtimestamp(from_ts).strftime('%Y-%m-%d')} to {datetime.fromtimestamp(to_ts).strftime('%Y-%m-%d')}...")

    try:
        # Fetch data from CoinGecko
        market_data = cg.get_coin_market_chart_range_by_id(
            id=coin_id,
            vs_currency=vs_currency,
            from_timestamp=from_ts,
            to_timestamp=to_ts
        )
        
        # Process the data
        prices = market_data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        
        # Convert timestamp to a readable date format
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        # Set date as index and keep only the price column
        df = df.set_index('date')
        df = df[['price']]
        
        # Save to CSV
        file_path = f"{coin_id}_data.csv"
        df.to_csv(file_path)
        print(f"Data successfully saved to {file_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Example usage: Fetch 365 days of data for Ethereum against USD
    fetch_and_save_data(coin_id='ethereum', vs_currency='usd', days=365)