from binance.exceptions import BinanceAPIException
from src.utils.logger import log
from src.utils.validation import (
    validate_symbol,
    validate_side,
    validate_quantity,
)

def place_market_order(client, symbol, side, quantity):
    """Places a market order."""
    if not (validate_symbol(symbol) and validate_side(side) and validate_quantity(quantity)):
        log.error("Market order validation failed.")
        return None

    try:
        log.info(f"Placing market {side} order for {quantity} {symbol}...")
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='MARKET',
            quantity=quantity
        )
        log.info(f"SUCCESS: Market order placed: {order}")
        return order
    except BinanceAPIException as e:
        log.error(f"ERROR placing market order: {e}")
        return None