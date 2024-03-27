# bestk.py
import pyupbit
import numpy as np

ticket ="KRW-BTC"

def get_ror(k=0.5):
    df = pyupbit.get_ohlcv(ticket, count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'], 1)
    ror = df['ror'].cumprod()[-2]
    return ror

def find_best_k():
    best_k = 0.0
    highest_ror = 0.0
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(k)
        if ror > highest_ror:
            highest_ror = ror
            best_k = k
    return best_k

if __name__ == "__main__":
    best_k, highest_ror = find_best_k()
    print(f"Best K: {best_k:.1f} with ROR: {highest_ror}")
