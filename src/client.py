import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from src.utils.logger import log

class BinanceClient:
    def __init__(self, testnet=True):
        """Initializes Binance Futures Testnet Client"""
        self.testnet = testnet
        load_dotenv()
        
        def get_key(env_var, fallback_var):
            val = os.getenv(env_var)
            if val and "your_" not in val: # Ignore placeholders
                return val
            return os.getenv(fallback_var)

        if testnet:
            api_key = get_key("TESTNET_API_KEY", "BINANCE_API_KEY")
            api_secret = get_key("TESTNET_API_SECRET", "BINANCE_API_SECRET")
        else:
            api_key = get_key("LIVE_API_KEY", "BINANCE_API_KEY")
            api_secret = get_key("LIVE_API_SECRET", "BINANCE_API_SECRET")

        if not api_key or not api_secret:
            env_name = "Testnet" if testnet else "Live"
            raise ValueError(f"API key and secret missing for {env_name}. Please check your .env file.")

        self.client = Client(api_key, api_secret)

        
        if testnet:
            futures_base = "https://testnet.binancefuture.com/fapi"
            self.client.API_URL = futures_base
            self.client.FUTURES_URL = futures_base
            self.client.futures_API_URL = futures_base

        
        self.client.session.headers.update({"X-MBX-APIKEY": api_key})

        
        self.client.DEFAULT_TYPE = 'FUTURES'

        
        self.client.futures_ping()

        self.test_connection()

    def test_connection(self):
        """Check if USDT-M futures account is accessible"""
        try:
            account = self.client.futures_account()
            env_name = "Testnet" if self.testnet else "Live"
            log.info(f"SUCCESS: Connected to Binance USDT-M Futures {env_name}")
            return account

        except BinanceAPIException as e:
            log.error(f"API error: {e}")
            raise e
        except BinanceRequestException as e:
            log.error(f"Server returned Invalid Response: {e}")
            raise e
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            raise e
