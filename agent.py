from utils import swap_tokens, get_balance, token_in
from strategy import decide_action
from config import SLEEP_INTERVAL
from datetime import datetime
import time

LOG_FILE = "log.txt"

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def main():
    log("Starting AI Base trading bot with Chainlink price feeds...")
    while True:
        action, amount_in, min_out = decide_action()
        balance = get_balance(token_in)
        log(f"TOKEN_IN balance: {balance / 10**6}")

        if action == "swap":
            log(f"Swapping {amount_in / 10**6} TOKEN_IN -> TOKEN_OUT with min_out={min_out / 10**18}...")
            tx_hash = swap_tokens(amount_in, min_out)
            log(f"Swap executed, tx hash: {tx_hash}")
        else:
            log("No action this round.")

        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    main()
