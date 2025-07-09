# simulator.py
import pandas as pd
import numpy as np

class LPSimulator:
    def __init__(self, data, initial_investment, fee_tier, daily_volume_percentage):
        """
        Initializes the simulator.

        Args:
            data (pd.DataFrame): DataFrame with a 'price' column.
            initial_investment (float): Total initial investment in USD.
            fee_tier (float): The trading fee percentage (e.g., 0.003 for 0.3%).
            daily_volume_percentage (float): Estimated daily trading volume as a percentage of pool liquidity.
        """
        self.data = data
        self.initial_investment = initial_investment
        self.fee_tier = fee_tier
        self.daily_volume_percentage = daily_volume_percentage
        self.results = None

    def _calculate_hodl_value(self):
        """Calculates the value of the portfolio if we just held the initial assets."""
        initial_price = self.data['price'].iloc[0]
        # 50/50 split at the start
        asset_a_amount = (self.initial_investment / 2) / initial_price # e.g., amount of ETH
        asset_b_amount = self.initial_investment / 2 # e.g., amount of USDC
        
        self.results['hodl_value'] = (asset_a_amount * self.results['price']) + asset_b_amount

    def _calculate_lp_performance(self):
        """Calculates the value of the LP position, including IL and fees."""
        initial_price = self.data['price'].iloc[0]
        
        # Initial deposit
        x0 = (self.initial_investment / 2) / initial_price # Initial amount of asset A (ETH)
        y0 = self.initial_investment / 2                 # Initial amount of asset B (USDC)
        k = x0 * y0                                      # The constant product

        # Calculate asset amounts and values at each price point
        self.results['lp_asset_a_amount'] = np.sqrt(k / self.results['price'])
        self.results['lp_asset_b_amount'] = np.sqrt(k * self.results['price'])
        
        # Value of LP position (without fees)
        self.results['lp_value_no_fees'] = (self.results['lp_asset_a_amount'] * self.results['price']) + self.results['lp_asset_b_amount']
        
        # Impermanent Loss
        self.results['impermanent_loss'] = self.results['lp_value_no_fees'] - self.results['hodl_value']
        
        # Simulate Fees
        # Assumption: Our share of the pool remains constant, which is a simplification.
        # Daily volume is a % of the total value in the pool at that time.
        daily_fees = self.results['lp_value_no_fees'] * self.daily_volume_percentage * self.fee_tier
        self.results['fees_earned'] = daily_fees.cumsum()
        
        # Total LP Value
        self.results['total_lp_value'] = self.results['lp_value_no_fees'] + self.results['fees_earned']

    def run_simulation(self):
        """Runs the full simulation."""
        self.results = self.data.copy()
        
        print("Running HODL strategy calculation...")
        self._calculate_hodl_value()
        
        print("Running LP strategy calculation...")
        self._calculate_lp_performance()
        
        print("Simulation complete.")
        return self.results