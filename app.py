from flask import Flask, render_template, request, redirect, url_for
from model import get_analysis

app = Flask(__name__)

# --- ROUTES ---

@app.route('/')
def home():
    """Home page displaying categorized top 5 assets."""
    market_data = {
        "STOCKS": [
            {"name": "Reliance", "symbol": "RELIANCE.NS"},
            {"name": "TCS", "symbol": "TCS.NS"},
            {"name": "Apple", "symbol": "AAPL"},
            {"name": "Nvidia", "symbol": "NVDA"},
            {"name": "Tesla", "symbol": "TSLA"}
        ],
        "CRYPTO": [
            {"name": "Bitcoin", "symbol": "BTC"},
            {"name": "Ethereum", "symbol": "ETH"},
            {"name": "Solana", "symbol": "SOL"},
            {"name": "Binance Coin", "symbol": "BNB"},
            {"name": "Cardano", "symbol": "ADA"}
        ],
        "FOREX": [
            {"name": "USD/INR", "symbol": "USDINR"},
            {"name": "EUR/USD", "symbol": "EURUSD"},
            {"name": "GBP/USD", "symbol": "GBPUSD"},
            {"name": "USD/JPY", "symbol": "USDJPY"},
            {"name": "AUD/USD", "symbol": "AUDUSD"}
        ],
        "COMMODITY": [
            {"name": "Gold", "symbol": "GOLD"},
            {"name": "Silver", "symbol": "SILVER"},
            {"name": "Crude Oil", "symbol": "CRUDEOIL"},
            {"name": "Natural Gas", "symbol": "NATURALGAS"},
            {"name": "Copper", "symbol": "COPPER"}
        ]
    }
    return render_template('index.html', market_data=market_data)

@app.route('/predict/<symbol>')
def predict(symbol):
    """Trading Terminal route with full UI."""
    market_type = request.args.get('market', 'STOCKS')
    data = get_analysis(symbol.upper(), market_type)
    if data:
        return render_template('result.html', data=data)
    return redirect(url_for('home'))

@app.route('/risk-lab')
def risk_lab():
    """
    Standalone Neural Risk Lab route. 
    Crucial: Must return 'risk_lab.html'
    """
    symbol = request.args.get('symbol')
    market = request.args.get('market', 'STOCKS')
    
    if symbol:
        data = get_analysis(symbol.strip().upper(), market)
        # Verify this file exists in your /templates folder
        return render_template('risk_lab.html', data=data)
    
    return render_template('risk_lab.html', data=None)

@app.route('/search', methods=['POST'])
def search():
    """Handles main search bar input."""
    symbol = request.form.get('symbol')
    market = request.form.get('market_type', 'STOCKS') 
    if symbol:
        return redirect(url_for('predict', symbol=symbol.strip().upper(), market=market))
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
