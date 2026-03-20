import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime, timedelta
import random

# Your actual Alpha Vantage API Key
API_KEY = 'UBVKVDZJTJZV7626' 

def get_news(symbol, trend):
    """ Generates context-aware news headlines based on the current trend """
    if trend == "UP":
        headlines = [
            f"Institutional accumulation detected for {symbol}.",
            f"Bullish sentiment rising as {symbol} breaks technical resistance.",
            f"Market analysts upgrade {symbol} outlook to 'Strong Buy'.",
            f"Significant whale movement confirms structural support for {symbol}.",
            f"Neural patterns indicate sustained momentum for {symbol}."
        ]
    else:
        headlines = [
            f"Heavy profit taking observed in {symbol} following recent peak.",
            f"{symbol} faces headwinds amid global macroeconomic uncertainty.",
            f"Critical support levels tested for {symbol} as sell-side volume increases.",
            f"Short-term bearish divergence noted on {symbol} high-frequency charts.",
            f"Algorithm detects potential trend reversal for {symbol}."
        ]
    return random.sample(headlines, 2) # Returns 2 random relevant headlines

def get_analysis(symbol, market_type="STOCKS"):
    # 1. Route to correct API Function and define correct JSON keys
    if market_type == "CRYPTO":
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={API_KEY}'
        data_key = "Time Series (Digital Currency Daily)"
        price_col = "4a. close (USD)" 
    elif market_type == "FOREX":
        from_sym = symbol[:3]
        to_sym = symbol[3:]
        url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_sym}&to_symbol={to_sym}&apikey={API_KEY}'
        data_key = "Time Series FX (Daily)"
        price_col = "4. close"
    else: # Default: STOCKS
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
        data_key = "Time Series (Daily)"
        price_col = "4. close"

    try:
        r = requests.get(url)
        data = r.json()
        
        # Check for API Limit/Errors and switch to Mock Data if needed
        if data_key not in data:
            print(f"API Alert: {data.get('Note', 'Symbol Error')}. Loading Mock Data.")
            return get_mock_data(symbol, market_type)

        # 2. Data Engineering with Pandas
        df = pd.DataFrame.from_dict(data[data_key], orient='index')
        df = df.rename(columns={price_col: "Close"}).astype(float)
        df = df.sort_index()

        # Extract real dates
        dates_list = [str(d) for d in df.index[-30:]]

        # 3. Temporal Trend Analysis
        last_7 = df['Close'].tail(7)
        trend_7 = "UP" if last_7.iloc[-1] > last_7.iloc[0] else "DOWN"
        change_7 = round(((last_7.iloc[-1] - last_7.iloc[0]) / last_7.iloc[0]) * 100, 2)

        last_15 = df['Close'].tail(15)
        trend_15 = "UP" if last_15.iloc[-1] > last_15.iloc[0] else "DOWN"
        change_15 = round(((last_15.iloc[-1] - last_15.iloc[0]) / last_15.iloc[0]) * 100, 2)

        # 4. ML Logic (Random Forest)
        df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
        df['Returns'] = df['Close'].pct_change()
        df = df.dropna()

        X = df[['Close', 'Returns']].iloc[:-1] 
        y = df['Target'].iloc[:-1]

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)

        # 5. Risk & Prediction
        current_price = df['Close'].iloc[-1]
        current_return = df['Returns'].iloc[-1]
        prediction = model.predict([[current_price, current_return]])[0]
        final_trend = "UP" if prediction == 1 else "DOWN"
        volatility = df['Returns'].tail(15).std()
        
        risk_threshold = 0.04 if market_type == "CRYPTO" else 0.02

        # 6. Package Data
        return {
            "symbol": symbol,
            "market_type": market_type,
            "price": round(current_price, 2),
            "trend": final_trend,
            "risk": "HIGH" if volatility > risk_threshold else "LOW",
            "history": df['Close'].tail(30).tolist(),
            "dates": dates_list, 
            "news": get_news(symbol, final_trend), # NEWS ADDED HERE
            "analysis": {
                "seven_day": {"trend": trend_7, "change": change_7},
                "fifteen_day": {"trend": trend_15, "change": change_15},
                "next_three": {"trend": final_trend},
                "volatility": round(volatility, 4)
            }
        }
    except Exception as e:
        print(f"System Error: {e}")
        return get_mock_data(symbol, market_type)

def get_mock_data(symbol, market_type):
    """ Ensures the UI works even if API limits are hit """
    base = random.randint(100, 500)
    history = [base + random.uniform(-10, 10) for _ in range(30)]
    
    end_date = datetime.now()
    mock_dates = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
    mock_trend = random.choice(["UP", "DOWN"])

    return {
        "symbol": f"{symbol} (DEMO)",
        "market_type": market_type,
        "price": round(history[-1], 2),
        "trend": mock_trend,
        "risk": random.choice(["LOW", "HIGH"]),
        "history": history,
        "dates": mock_dates,
        "news": get_news(symbol, mock_trend), # NEWS ADDED HERE
        "analysis": {
            "seven_day": {"trend": "UP", "change": 1.5},
            "fifteen_day": {"trend": "DOWN", "change": 0.8},
            "next_three": {"trend": "UP"},
            "volatility": 0.01
        }
    }
