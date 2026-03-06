# Base Testnet RPC & wallet
RPC_URL = "https://goerli.base.org"
PRIVATE_KEY = "YOUR_PRIVATE_KEY_HERE"
ACCOUNT_ADDRESS = ""  # optional, derived from PRIVATE_KEY

# Tokens
TOKEN_IN = "0xYourTokenInAddress"
TOKEN_OUT = "0xYourTokenOutAddress"
TOKEN_DECIMALS_IN = 6
TOKEN_DECIMALS_OUT = 18

# Uniswap v3 Router
DEX_ROUTER_ADDRESS = "0xE592427A0AEce92De3Edee1F18E0157C05861564"

# Chainlink price feed for TOKEN_OUT/USD
CHAINLINK_FEED = "0xYourChainlinkPriceFeedAddress"

# Trading settings
TRADE_AMOUNT_IN = 10
SLIPPAGE_TOLERANCE = 0.01
SLEEP_INTERVAL = 60
SMA_WINDOW = 5
