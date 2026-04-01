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
    return random.sample(headlines, 2)

def get_analysis(symbol, market_type="STOCKS"):
    # 1. Route to correct API Function
    if market_type == "CRYPTO":
        url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={API_KEY}'
        data_key = "Time Series (Digital Currency Daily)"
        key_map = {"1a. open (USD)": "Open", "2a. high (USD)": "High", "3a. low (USD)": "Low", "4a. close (USD)": "Close", "5. volume": "Volume"}
    elif market_type == "FOREX":
        from_sym, to_sym = symbol[:3], symbol[3:]
        url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={from_sym}&to_symbol={to_sym}&apikey={API_KEY}'
        data_key = "Time Series FX (Daily)"
        key_map = {"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close"}
    else: # Default: STOCKS
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
        data_key = "Time Series (Daily)"
        key_map = {"1. open": "Open", "2. high": "High", "3. low": "Low", "4. close": "Close", "5. volume": "Volume"}

    try:
        r = requests.get(url)
        data = r.json()
        
        if data_key not in data:
            return get_mock_data(symbol, market_type)

        # 2. Data Engineering
        df = pd.DataFrame.from_dict(data[data_key], orient='index').astype(float)
        df = df.rename(columns=key_map)
        df = df.sort_index()

        # 3. Indicators: SMA & Volatility
        df['SMA_7'] = df['Close'].rolling(window=7).mean()
        df['Returns'] = df['Close'].pct_change()
        volatility = df['Returns'].tail(15).std()

        # 4. Neural Risk Lab Calculations (NEW)
        # Factor A: 7-Day Velocity Risk (Absolute % change over 7 days)
        last_7_prices = df['Close'].tail(7)
        vel_change = abs(((last_7_prices.iloc[-1] - last_7_prices.iloc[0]) / last_7_prices.iloc[0]) * 100)
        velocity_risk = "HIGH" if vel_change > 12 else "STABLE"

        # Factor B: 15-Day Structural Stability
        stability_metric = df['Returns'].tail(15).std()
        structural_stability = "FRAGILE" if stability_metric > 0.035 else "SOLID"

        # Factor C: Neural Safety Signal
        is_unsafe = (velocity_risk == "HIGH" or structural_stability == "FRAGILE")
        safety_signal = "UNSAFE" if is_unsafe else "SAFE"

        # Prepare 30-day window
        df_display = df.tail(30).dropna()
        dates_list = [str(d) for d in df_display.index]

        # 5. ML Logic
        df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
        df_ml = df.dropna()
        X, y = df_ml[['Close', 'Returns']].iloc[:-1], df_ml['Target'].iloc[:-1]
        model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X, y)
        prediction = model.predict([[df['Close'].iloc[-1], df['Returns'].iloc[-1]]])[0]
        final_trend = "UP" if prediction == 1 else "DOWN"

        return {
            "symbol": symbol,
            "market_type": market_type,
            "price": round(df['Close'].iloc[-1], 2),
            "trend": final_trend,
            "risk": "HIGH" if volatility > (0.04 if market_type == "CRYPTO" else 0.02) else "LOW",
            "dates": dates_list,
            "ohlc": {
                "open": df_display['Open'].tolist(),
                "high": df_display['High'].tolist(),
                "low": df_display['Low'].tolist(),
                "close": df_display['Close'].tolist(),
                "volume": df_display['Volume'].tolist() if 'Volume' in df_display else []
            },
            "sma_history": df_display['SMA_7'].tolist(),
            "news": get_news(symbol, final_trend),
            # THE RISK LAB DATA
            "risk_lab": {
                "velocity_risk": velocity_risk,
                "structural_stability": structural_stability,
                "safety_signal": safety_signal,
                "stability_score": round(100 - (stability_metric * 1000), 1)
            },
            "analysis": {
                "volatility": round(volatility, 4),
                "next_three": {"trend": final_trend}
            }
        }
    except Exception as e:
        print(f"Error: {e}")
        return get_mock_data(symbol, market_type)

def get_mock_data(symbol, market_type):
    """ Fallback with full Risk Lab support """
    base = random.randint(100, 500)
    history = []
    for _ in range(40):
        close = base + random.uniform(-10, 10)
        open_p = close + random.uniform(-5, 5)
        history.append([open_p, close + 5, close - 5, close])
        base = close
        
    df = pd.DataFrame(history, columns=['Open', 'High', 'Low', 'Close'])
    df['SMA_7'] = df['Close'].rolling(7).mean()
    df['Returns'] = df['Close'].pct_change()
    df_final = df.tail(30).dropna()
    
    end_date = datetime.now()
    mock_dates = [(end_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(29, -1, -1)]
    mock_trend = random.choice(["UP", "DOWN"])

    return {
        "symbol": f"{symbol} (DEMO)",
        "market_type": market_type,
        "price": round(df_final['Close'].iloc[-1], 2),
        "trend": mock_trend,
        "risk": random.choice(["LOW", "HIGH"]),
        "dates": mock_dates,
        "ohlc": {
            "open": df_final['Open'].tolist(),
            "high": df_final['High'].tolist(),
            "low": df_final['Low'].tolist(),
            "close": df_final['Close'].tolist(),
            "volume": [random.randint(1000, 5000) for _ in range(30)]
        },
        "sma_history": df_final['SMA_7'].tolist(),
        "news": get_news(symbol, mock_trend),
        "risk_lab": {
            "velocity_risk": random.choice(["STABLE", "HIGH"]),
            "structural_stability": random.choice(["SOLID", "FRAGILE"]),
            "safety_signal": random.choice(["SAFE", "UNSAFE"]),
            "stability_score": 88.5
        },
        "analysis": { "volatility": 0.01, "next_three": {"trend": mock_trend} }
    }
