import time
import pyupbit
import datetime
import bestk  # bestk 모듈을 import합니다.

access = "r9TcZo1xRoGzeQqI2mAw9LOhhmyKdVaVUB5o1jfb"
secret = "G7z8zJkxsbCCT8PuTmxdUFYI7pybNnG3POc747Nq"

ticket = "KRW-CVC"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=2)  # 2분간의 데이터를 사용
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
# k_value를 처음에 한 번 확인하고, 이후 매분마다 업데이트합니다.

k_value = bestk.find_best_k()
last_k_update = datetime.datetime.now()
buy_price = 0  # 매수 가격을 저장할 변수

# 자동매매 시작
# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(ticket)
        end_time = start_time + datetime.timedelta(days=1)
        
        if now - last_k_update > datetime.timedelta(minutes=1):
            k_value = bestk.find_best_k()
            last_k_update = now  # k_value 업데이트 시간을 현재 시간으로 설정합니다.
                        
        current_price = get_current_price(ticket)  # 현재 가격을 매초마다 업데이트

        # 주문 가능 시간인지 확인
        if start_time < now < end_time - datetime.timedelta(seconds=1):
            target_price = get_target_price(ticket, k_value)  # 최적의 k 값을 사용
            currency = ticket.split("-")[1]
            btc = get_balance(currency)
            
            # 매수 조건 확인
            if target_price < current_price and buy_price == 0:  # 아직 매수하지 않았을 경우
                krw = get_balance("KRW")
                if krw > 5000:
                    # 매수 주문
                    upbit.buy_market_order(ticket, krw*0.9995)
                    buy_price = current_price  # 매수 가격 업데이트
            elif btc > 0.00008 and buy_price != 0:
                profit_ratio = (current_price - buy_price) / buy_price
                if profit_ratio >= 0.02 or profit_ratio <= -0.015:
                    result = upbit.sell_market_order(ticket, btc*0.9995)  # 매도 주문 실행
                    print(result)  # API 호출 결과 확인
                    buy_price = 0  # 매수 가격 초기화
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

