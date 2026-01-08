import ccxt
import os
from dotenv import load_dotenv

load_dotenv()

def get_exchange():
    try:
        api_key = os.getenv('BINANCE_API_KEY')
        secret_key = os.getenv('BINANCE_SECRET_KEY')
        use_testnet = os.getenv('USE_TESTNET') == 'True'

        if not api_key or not secret_key:
            raise ValueError("API keys not found in .env file")

        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'options': {
                'defaultType': 'future', 
            },
            'enableRateLimit': True
        })

        if use_testnet:
            exchange.set_sandbox_mode(True)

        return exchange

    except Exception as e:
        print(f"Error initializing exchange: {e}")
        return None