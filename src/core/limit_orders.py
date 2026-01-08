from binance.exceptions import BinanceAPIException
from src.utils.logger import log
from src.utils.validation import (
    validate_symbol,
    validate_side,
    validate_quantity,
    validate_price,
)

def place_limit_order(client, symbol, side, quantity, price):
    """Places a limit order."""
    if not (
        validate_symbol(symbol)
        and validate_side(side)
        and validate_quantity(quantity)
        and validate_price(price)
    ):
        log.error("Limit order validation failed.")
        return None

    try:
        log.info(f"Placing limit {side} order for {quantity} {symbol} at price {price}...")
        order = client.futures_create_order(
            symbol=symbol,
            side=side.upper(),
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=price
        )
        log.info(f"SUCCESS: Limit order placed: {order}")
        return order
    except BinanceAPIException as e:
        log.error(f"ERROR placing limit order: {e}")
        return None