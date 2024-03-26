import os
from dotenv import load_dotenv
import pyupbit
import time

load_dotenv()
UPBIT_ACCESS = os.getenv('r9TcZo1xRoGzeQqI2mAw9LOhhmyKdVaVUB5o1jfb')
UPBIT_SECRET = os.getenv('G7z8zJkxsbCCT8PuTmxdUFYI7pybNnG3POc747Nq')

upbit = pyupbit.Upbit(UPBIT_ACCESS, UPBIT_SECRET)

def get_price(ticker="KRW-BTC"):
    return pyupbit.get_current_price(ticker)

def check_volatility_breakout(k=0.5):
    """Decide to buy based on the volatility breakout strategy."""
    df = pyupbit.get_ohlcv("KRW-BTC", interval="minute1", count=2)  # Fetching last 2 minutes data
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    current_price = get_price()
    return current_price > target_price, target_price

def execute_buy():
    """Buy as much BTC as possible with the current KRW balance."""
    krw_balance = upbit.get_balance("KRW")
    if krw_balance > 5000:  # Minimum requirement for transaction
        result = upbit.buy_market_order("KRW-BTC", krw_balance*0.9995)  # 0.9995 to account for transaction fees
        print("Buy order successful:", result)
        return True
    return False

def monitor_and_sell(buy_price, target_profit=0.02, stop_loss=-0.015):
    """Monitor the BTC price and sell based on target profit or stop loss."""
    while True:
        current_price = get_price()
        profit_ratio = (current_price - buy_price) / buy_price

        if profit_ratio >= target_profit or profit_ratio <= stop_loss:
            btc_balance = upbit.get_balance("BTC")
            if btc_balance * current_price > 5000:  # Check if sell order meets minimum requirement
                result = upbit.sell_market_order("KRW-BTC", btc_balance)
                print("Sell order successful:", result)
                break
        time.sleep(1)  # Check price every second

def trade():
    while True:
        buy_decision, target_price = check_volatility_breakout()
        if buy_decision:
            if execute_buy():
                print(f"Bought at target price {target_price}. Monitoring for sell conditions...")
                monitor_and_sell(target_price)
        time.sleep(60)  # Check for buying opportunity every minute

if __name__ == "__main__":
    trade()
