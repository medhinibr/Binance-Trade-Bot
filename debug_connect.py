import os
import sys
from binance.client import Client
from dotenv import load_dotenv

# Load env
load_dotenv('src/.env')
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

print(f"API Key found: {bool(api_key)}")
print(f"API Secret found: {bool(api_secret)}")

def test_connection(testnet):
    print(f"\nTesting Connection (Testnet={testnet})...")
    try:
        # Manual override with /fapi
        client = Client(api_key, api_secret)
        if testnet:
            futures_base = "https://testnet.binancefuture.com/fapi"
            client.API_URL = futures_base
            client.FUTURES_URL = futures_base
            client.futures_API_URL = futures_base
        
        # Try to ping
        print("Pinging futures...")
        client.futures_ping()
        print("Ping successful.")

        # Try account info (Read-only)
        print("Fetching account info...")
        client.futures_account()
        print("Account info fetched successfully.")
        account = client.futures_account()
        print("Account info fetched successfully.")
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    # Test Testnet
    test_connection(testnet=True)
