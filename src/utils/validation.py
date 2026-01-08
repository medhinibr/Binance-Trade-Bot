def validate_symbol(symbol: str) -> bool:
    """Validates if the symbol is in the correct format (e.g., BTCUSDT)."""
    return isinstance(symbol, str) and len(symbol) > 4 and symbol.isupper()

def validate_quantity(quantity: float) -> bool:
    """Validates if the quantity is a positive number."""
    return isinstance(quantity, (int, float)) and quantity > 0

def validate_price(price: float) -> bool:
    """Validates if the price is a positive number."""
    return isinstance(price, (int, float)) and price > 0

def validate_side(side: str) -> bool:
    """Validates if the order side is either 'BUY' or 'SELL'."""
    return isinstance(side, str) and side.upper() in ["BUY", "SELL"]