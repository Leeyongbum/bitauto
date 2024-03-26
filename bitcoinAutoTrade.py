import time
import pyupbit
import datetime
import bestk  # bestk 모듈을 import합니다.

access = "your-access"
secret = "your-secret"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute2", count=2)  # 2분간의 데이터를 사용
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

buy_price = 0  # 매수 가격을 저장할 변수
k_value = bestk.find_best_k()  # 최적의 k 값을 찾습니다.

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        # 주문 가능 시간인지 확인
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", k_value)  # 최적의 k 값을 사용
            current_price = get_current_price("KRW-BTC")
            
            # 매수 조건 확인
            if target_price < current_price and buy_price == 0:  # 아직 매수하지 않았을 경우
                krw = get_balance("KRW")
                if krw > 5000:
                    # 매수 주문
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    buy_price = current_price  # 매수 가격 업데이트
        else:
            btc = get_balance("BTC")
            if btc > 0.00008 and buy_price != 0:
                profit_ratio = (current_price - buy_price) / buy_price
                # 2% 이상 상승하거나 1.5% 이상 하락 시 매도
                if profit_ratio >= 0.02 or profit_ratio <= -0.015:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)
                    buy_price = 0  # 매수 가격 초기화
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
