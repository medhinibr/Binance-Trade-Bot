from flask import Flask, render_template, request, redirect, url_for
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

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Open http://127.0.0.1:5000 in your browser.")
    app.run(debug=True, port=5000)
