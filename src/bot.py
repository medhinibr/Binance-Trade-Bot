import argparse
from src.client import BinanceClient
from src.core.market_orders import place_market_order
from src.core.limit_orders import place_limit_order
from src.utils.logger import log

def main():
    """Main function to parse arguments and execute bot commands."""
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
    parser.add_argument("--live", action="store_true", help="Use Live Binance Futures Server (Real Money)")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)

    
    market_parser = subparsers.add_parser("market", help="Place a market order")
    market_parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    market_parser.add_argument("--side", required=True, help="Order side (BUY or SELL)")
    market_parser.add_argument("--quantity", required=True, type=float, help="Order quantity")

    
    limit_parser = subparsers.add_parser("limit", help="Place a limit order")
    limit_parser.add_argument("--symbol", required=True, help="Trading symbol")
    limit_parser.add_argument("--side", required=True, help="Order side (BUY or SELL)")
    limit_parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    limit_parser.add_argument("--price", required=True, type=float, help="Order price")

    args = parser.parse_args()

    try:
        # Default to Testnet unless --live is specified
        is_testnet = not args.live
        b_client = BinanceClient(testnet=is_testnet)
        client = b_client.client
    except Exception as e:
        log.error(f"Could not start the bot. Error: {e}")
        return

    if args.command == "market":
        place_market_order(client, args.symbol, args.side.upper(), args.quantity)
    elif args.command == "limit":
        place_limit_order(client, args.symbol, args.side.upper(), args.quantity, args.price)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()