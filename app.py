from flask import Flask, render_template, request, redirect, url_for
from model import get_analysis

app = Flask(__name__)

# --- ROUTES ---

@app.route('/')
def home():
    """
    Home page displaying categorized top 5 assets for Global Market Pulse.
    """
    # Organized market data for the frontend grid
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
    """
    Direct link route. Captures 'market' from URL params to route API correctly.
    """
    market_type = request.args.get('market', 'STOCKS')
    
    # Run the Random Forest Analysis from model.py
    data = get_analysis(symbol.upper(), market_type)
    
    if data:
        # Pass the processed AI data to the results page
        return render_template('result.html', data=data)
    
    # If API fails or symbol is invalid, redirect back home
    return redirect(url_for('home'))

@app.route('/search', methods=['POST'])
def search():
    """
    Handles search bar input. Captures the symbol and the hidden market_type input.
    """
    symbol = request.form.get('symbol')
    market = request.form.get('market_type', 'STOCKS') 
    
    if symbol:
        # Redirect to predict route with market as a query parameter
        return redirect(url_for('predict', symbol=symbol.strip().upper(), market=market))
    
    return redirect(url_for('home'))

# --- ERROR HANDLING ---

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('home'))

if __name__ == '__main__':
    # threaded=True allows handling multiple simulation requests at once
    app.run(debug=True, threaded=True)
