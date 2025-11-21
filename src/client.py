import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from src.utils.logger import log

class BinanceClient:
    def __init__(self, testnet=True):
        """Initializes Binance Futures Testnet Client"""
        load_dotenv()
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        if not api_key or not api_secret:
            raise ValueError("API key and secret missing in .env file")

        self.client = Client(api_key, api_secret)

        
        if testnet:
            futures_base = "https://testnet.binancefuture.com"
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
            log.info("SUCCESS: Connected to Binance USDT-M Futures Testnet")
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
