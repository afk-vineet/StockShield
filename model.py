import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Replace with your actual Alpha Vantage API Key
API_KEY = '3ULF1RNLHE2VHNWK' 

def get_analysis(symbol):
    # 1. Fetch Real-time Data from Alpha Vantage
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    
    try:
        r = requests.get(url)
        data = r.json()
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

    if "Time Series (Daily)" not in data:
        print("API Limit reached or Invalid Symbol.")
        return None

    # 2. Data Engineering with Pandas
    # Convert JSON to a DataFrame and clean it
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
    df = df.rename(columns={"4. close": "Close"}).astype(float)
    df = df.sort_index()

    # 3. Temporal Trend Analysis (Past Windows)
    # 7-Day Analysis
    last_7 = df['Close'].tail(7)
    trend_7 = "UP" if last_7.iloc[-1] > last_7.iloc[0] else "DOWN"
    change_7 = round(((last_7.iloc[-1] - last_7.iloc[0]) / last_7.iloc[0]) * 100, 2)

    # 15-Day Analysis
    last_15 = df['Close'].tail(15)
    trend_15 = "UP" if last_15.iloc[-1] > last_15.iloc[0] else "DOWN"
    change_15 = round(((last_15.iloc[-1] - last_15.iloc[0]) / last_15.iloc[0]) * 100, 2)

    # 4. Machine Learning Logic (Random Forest)
    # We create a 'Target' column: 1 if price went up the next day, 0 if down
    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    
    # Feature Selection (X) and Label (y)
    X = df[['Close']].iloc[:-1] 
    y = df['Target'].iloc[:-1]

    # Training the "Forest"
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # 5. Risk & Prediction Calculations
    current_price = df['Close'].iloc[-1]
    prediction = model.predict([[current_price]])[0]
    
    # Volatility = Standard Deviation of daily percentage changes
    # High volatility (> 2%) means High Risk
    volatility = df['Close'].pct_change().std()
    
    # AI Next 3-Day Forecast Logic
    next_3_trend = "BULLISH (UP)" if prediction == 1 else "BEARISH (DOWN)"

    # 6. Final Data Package for Frontend
    return {
        "symbol": symbol,
        "price": round(current_price, 2),
        "trend": "UP" if prediction == 1 else "DOWN",
        "risk": "HIGH" if volatility > 0.02 else "LOW",
        "history": df['Close'].tail(30).tolist(),
        "dates": [d for d in df.index[-30:]],
        "analysis": {
            "seven_day": {"trend": trend_7, "change": change_7},
            "fifteen_day": {"trend": trend_15, "change": change_15},
            "next_three": {"trend": next_3_trend}
        }
    }