from web3 import Web3
from config import *
import json

w3 = Web3(Web3.HTTPProvider(RPC_URL))
if not ACCOUNT_ADDRESS:
    account = w3.eth.account.from_key(PRIVATE_KEY)
else:
    account = w3.eth.account.address(ACCOUNT_ADDRESS)

# ERC20 ABI
ERC20_ABI = json.loads("""
[
  {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},
  {"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"type":"function"}
]
""")
token_in = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_IN), abi=ERC20_ABI)
token_out = w3.eth.contract(address=Web3.to_checksum_address(TOKEN_OUT), abi=ERC20_ABI)

# Uniswap v3 Router ABI
DEX_ABI = json.loads("""
[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},
{"internalType":"address","name":"tokenOut","type":"address"},
{"internalType":"uint256","name":"amountIn","type":"uint256"},
{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"}],
"name":"swapExactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],
"stateMutability":"payable","type":"function"}]
""")
dex_router = w3.eth.contract(address=Web3.to_checksum_address(DEX_ROUTER_ADDRESS), abi=DEX_ABI)

# Chainlink ABI
CHAINLINK_ABI = json.loads("""
[
    {"inputs":[],"name":"latestRoundData","outputs":[
        {"internalType":"uint80","name":"roundId","type":"uint80"},
        {"internalType":"int256","name":"answer","type":"int256"},
        {"internalType":"uint256","name":"startedAt","type":"uint256"},
        {"internalType":"uint256","name":"updatedAt","type":"uint256"},
        {"internalType":"uint80","name":"answeredInRound","type":"uint80"}
    ],"stateMutability":"view","type":"function"}
]
""")
price_feed = w3.eth.contract(address=Web3.to_checksum_address(CHAINLINK_FEED), abi=CHAINLINK_ABI)

# Functions
def get_balance(token_contract):
    return token_contract.functions.balanceOf(account.address).call()

def approve(token_contract, spender, amount):
    nonce = w3.eth.get_transaction_count(account.address)
    tx = token_contract.functions.approve(spender, amount).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.to_wei('10', 'gwei')
    })
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def swap_tokens(amount_in, min_amount_out):
    approve(token_in, DEX_ROUTER_ADDRESS, amount_in)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = dex_router.functions.swapExactInputSingle(
        Web3.to_checksum_address(TOKEN_IN),
        Web3.to_checksum_address(TOKEN_OUT),
        amount_in,
        min_amount_out
    ).build_transaction({
        'from': account.address,
        'nonce': nonce,
        'gas': 350000,
        'gasPrice': w3.to_wei('10', 'gwei'),
        'value': 0
    })
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return w3.to_hex(tx_hash)

def get_chainlink_price():
    round_data = price_feed.functions.latestRoundData().call()
    answer = round_data[1]
    return answer / 1e8
