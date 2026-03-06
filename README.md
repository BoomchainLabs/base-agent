# Ultimate Base AI Trading Bot

## Features
- Live ERC-20 swaps on Base
- Chainlink price feeds for accurate token pricing
- SMA-based AI trend detection
- Slippage protection
- Full logging of trades
- Modular for strategy upgrades

## Setup

1. Clone repo
```bash
git clone https://github.com/BoomchainLabs/base-agent.git
cd base-agent

	2.	Install dependencies
pip install -r requirements.txt


	3.	Configure config.py with your RPC, tokens, router, Chainlink feed, and private key.


	4.	Run bot
python agent.py

Strategy
	•	Uses SMA (Simple Moving Average) over SMA_WINDOW of Chainlink prices
	•	Buys TOKEN_OUT when price < SMA

Next Steps
	•	Multi-token strategies
	•	Stop-loss / take-profit
	•	Deploy on secure cloud with auto-restart

---

## **8️⃣ GitHub Actions workflow (.github/workflows/deploy.yml)**

```yaml
name: Deploy Base AI Bot

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install python-dotenv

      - name: Setup environment variables
        run: echo "PRIVATE_KEY=${{ secrets.PRIVATE_KEY }}" >> $GITHUB_ENV

      - name: Deploy to Server
        uses: appleboy/ssh-action@v0.1.7
        with:
          host: ${{ secrets.SERVER_HOST }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          port: 22
          script: |
            cd ~/base-agent
            git pull
            pip install -r requirements.txt
            pkill -f agent.py || true
            nohup python agent.py > bot.log 2>&1 &
