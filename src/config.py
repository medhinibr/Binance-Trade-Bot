import ccxt
import os
from dotenv import load_dotenv
from binance.client import Client

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

       if testnet:/.
        log.warning("⚠️ USING BINANCE FUTURES TESTNET ⚠️")

        self.client = Client(api_key, api_secret)
        self.client.API_URL = "https://testnet.binancefuture.com/fapi"
       else:
        self.client = Client(api_key, api_secret)


    except Exception as e:
        print(f"Error initializing exchange: {e}")
        return None