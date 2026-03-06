from utils import get_balance, get_chainlink_price
from config import TRADE_AMOUNT_IN, SLIPPAGE_TOLERANCE, SMA_WINDOW
from collections import deque

price_history = deque(maxlen=SMA_WINDOW)

def decide_action():
    price = get_chainlink_price()
    price_history.append(price)
    if len(price_history) < SMA_WINDOW:
        return "hold", 0, 0
    sma = sum(price_history)/SMA_WINDOW
    balance = get_balance(token_in)

    if balance >= TRADE_AMOUNT_IN * 10**6 and price < sma:
        min_out = int((TRADE_AMOUNT_IN * (1 - SLIPPAGE_TOLERANCE)) * 10**18)
        return "swap", TRADE_AMOUNT_IN * 10**6, min_out
    return "hold", 0, 0
