from flask import Flask, render_template, request
from model import get_analysis

app = Flask(__name__)

@app.route('/')
def home():
    # Showing top 5 trending symbols
    stocks = ["AAPL", "TSLA", "NVDA", "MSFT", "GOOGL"]
    return render_template('index.html', stocks=stocks)

@app.route('/predict/<symbol>')
def predict(symbol):
    data = get_analysis(symbol)
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)