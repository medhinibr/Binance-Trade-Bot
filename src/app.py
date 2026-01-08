from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.client import BinanceClient
from src.core.market_orders import place_market_order
from src.core.limit_orders import place_limit_order

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session/flash if used, but here we pass args

# Global state for environment (simple toggle)
IS_TESTNET = False

def get_client():
    try:
        b_client = BinanceClient(testnet=IS_TESTNET)
        return b_client.client, None
    except Exception as e:
        error_msg = str(e)
        if "Invalid API-key" in error_msg:
            error_msg = "Invalid API Key or Permissions. Please check your .env file and ensure you are using the correct keys for the selected environment (Testnet vs Live)."
        return None, error_msg

@app.route('/')
def index():
    message = request.args.get('message')
    status = request.args.get('status')
    return render_template('index.html', is_testnet=IS_TESTNET, message=message, status=status)

@app.route('/switch_env', methods=['POST'])
def switch_env():
    global IS_TESTNET
    IS_TESTNET = not IS_TESTNET
    return redirect(url_for('index'))

@app.route('/order', methods=['POST'])
def place_order():
    client, error = get_client()
    if error:
        return redirect(url_for('index', message=f"Connection Error: {error}", status="error"))

    order_type = request.form.get('type')
    symbol = request.form.get('symbol').upper()
    side = request.form.get('side')
    quantity = float(request.form.get('quantity'))

    try:
        if order_type == 'market':
            place_market_order(client, symbol, side, quantity)
            msg = f"Market {side} order placed for {quantity} {symbol}"
        elif order_type == 'limit':
            price = float(request.form.get('price'))
            place_limit_order(client, symbol, side, quantity, price)
            msg = f"Limit {side} order placed for {quantity} {symbol} at {price}"
        else:
            return redirect(url_for('index', message="Invalid order type", status="error"))
        
        return redirect(url_for('index', message=msg, status="success"))
    except Exception as e:
        return redirect(url_for('index', message=f"Order Failed: {e}", status="error"))

@app.route('/platform')
def platform():
    return send_from_directory('platform', 'index.html')

# --- NEW: Real Market Data API (Powered by Yahoo Finance) ---
# Requires: pip install yfinance
try:
    import yfinance as yf
except ImportError:
    print("Warning: yfinance not installed. Please run: pip install yfinance")
    yf = None

@app.route('/api/market_status')
def market_status():
    # Simple check if market is open (Mock logic usually, but we can check mostly via time)
    # For now returns true
    return {"isOpen": True, "message": "Market is Open"}

@app.route('/api/quote')
def get_quote():
    if not yf:
        return {"error": "Server missing yfinance library"}, 500
    
    symbol = request.args.get('symbol')
    if not symbol:
        return {"error": "Symbol required"}, 400
    
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.fast_info
        # fallback to regular info if fast_info missing
        price = data.last_price if hasattr(data, 'last_price') else 0
        prev_close = data.previous_close if hasattr(data, 'previous_close') else 0
        change = ((price - prev_close) / prev_close) * 100 if prev_close else 0
        
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "prev_close": round(prev_close, 2),
            "day_high": round(data.day_high, 2) if hasattr(data, 'day_high') else 0,
            "day_low": round(data.day_low, 2) if hasattr(data, 'day_low') else 0,
            "volume": data.last_volume if hasattr(data, 'last_volume') else 0
        }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
        return {"error": str(e)}, 500

@app.route('/api/batch_quotes')
def get_batch_quotes():
    if not yf: return {"error": "Server missing yfinance"}, 500
    symbols = request.args.get('symbols', '').split(',')
    
    # yfinance batch download is faster
    try:
        data = yf.download(symbols, period="1d", group_by='ticker', progress=False)
        results = []
        
        # Handle single vs multiple result structure difference
        if len(symbols) == 1:
            sym = symbols[0]
            # yfinance structure varies by version, handling broadly:
            try:
                # Accessing scalar values from the dataframe
                row = data.iloc[-1]
                price = float(row['Close'])
                if len(data) > 1:
                     prev = float(data.iloc[-2]['Close'])
                else:
                     # fallback if only 1 data point (e.g. today started), try calling ticker info
                     t = yf.Ticker(sym)
                     fi = t.fast_info
                     prev = fi.previous_close
                     
                change = ((price - prev)/prev)*100
                results.append({
                    "symbol": sym,
                    "price": round(price, 2),
                    "change": round(change, 2)
                })
            except:
                 # Fallback to single quote endpoint logic
                 t = yf.Ticker(sym)
                 fi = t.fast_info
                 results.append({
                     "symbol": sym,
                     "price": round(fi.last_price, 2),
                     "change": round(((fi.last_price - fi.previous_close)/fi.previous_close)*100, 2)
                 })
        else:
             for sym in symbols:
                 try:
                     # For multiple symbols, data is MultiIndex
                     price = float(data[sym]['Close'].iloc[-1])
                     # Approx change calculation
                     open_p = float(data[sym]['Open'].iloc[-1]) 
                     change = ((price - open_p)/open_p)*100 # Using open as proxy for prev close for speed in batch
                     results.append({
                         "symbol": sym,
                         "price": round(price, 2),
                         "change": round(change, 2)
                     })
                 except:
                     results.append({"symbol": sym, "price": 0, "change": 0})
                     
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Open http://127.0.0.1:5000/platform in your browser.")
    app.run(debug=True, port=5000)
