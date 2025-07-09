# 💸 DeFi Liquidity Pool (LP) Strategy Simulator

### 🚀 [VIEW THE LIVE DEMO HERE](https://defi-lp-simulator-bwipc8kux6smhj4ata645c.streamlit.app/) 🚀


  <img width="1421" height="784" alt="Image" src="https://github.com/user-attachments/assets/299fa0ea-7131-4f92-b850-5ab9ddaf8baa" />

  <img width="1428" height="816" alt="Image" src="https://github.com/user-attachments/assets/45cb693d-964d-4de4-a9f4-2379b6da8591" />

An interactive web application built with Python and Streamlit to backtest and analyze the profitability of providing liquidity to Decentralized Exchanges (DEXs) compared to a simple "HODL" strategy.

---

## 🚀 Overview

This tool simulates the financial performance of a Liquidity Provider in an Automated Market Maker (AMM) pool, such as those found on Uniswap. It answers the fundamental question for any potential LP:

**"Do the fees I earn from providing liquidity outweigh the risk of Impermanent Loss?"**

The dashboard allows users to dynamically adjust parameters like the crypto-asset pair, initial investment, and fee assumptions to see how these factors impact profitability over a historical one-year period.

## ✨ Key Features

- **Interactive Dashboard:** Built with Streamlit for a user-friendly experience.
- **Dynamic Parameters:** Select different cryptocurrencies (ETH, BTC, SOL) and adjust investment size, fee tiers, and volume assumptions.
- **Strategy Comparison:** Directly compares the value of the LP position against a baseline HODL strategy.
- **Impermanent Loss Quantification:** Explicitly calculates and visualizes the impact of Impermanent Loss.
- **Volatility Analysis:** Calculates and displays the annualized volatility of the selected asset, a key driver of both risk and reward.
- **Live Data:** Fetches up-to-date historical price data from the CoinGecko API.

## 📊 Core Concepts Explained

- **Liquidity Providing (LP):** Depositing a pair of assets (e.g., ETH and USD) into a shared pool to facilitate trading on a DEX. In return, you earn a percentage of the trading fees.
- **Impermanent Loss (IL):** A unique risk for LPs. It's the potential loss in value you experience when the price of the deposited assets changes, compared to simply holding them in your wallet. The "loss" is "impermanent" because it only becomes a real loss if you withdraw your funds at that moment.

## 🛠️ Tech Stack

- **Language:** Python
- **Libraries:**
  - **Web Framework:** Streamlit
  - **Data Analysis:** Pandas, NumPy
  - **API Interaction:** PyCoinGecko
  - **Visualization:** Matplotlib, Seaborn

## ⚙️ Setup and Usage

To run this application on your local machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vkk28/defi-lp-simulator.git
    cd defi-lp-simulator
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    The application will open in your web browser.

---