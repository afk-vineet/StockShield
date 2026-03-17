# StockShield
Stock Shield is an advanced Decision Support System (DSS) designed to protect retail investors from extreme market volatility. By combining Machine Learning (Random Forest) with Temporal Intelligence, it bridges the gap between raw market data and safe investment strategies.

🚀 Key Features
ML Trend Forecast: Uses an Ensemble Random Forest Classifier (100 estimators) to predict the next 3-day trend.

Temporal Intelligence Dashboard: Comparative analysis of 7-day and 15-day price momentum.

Risk Intelligence: Real-time volatility tracking using Standard Deviation to categorize stocks as High or Low risk.

Stress Test Simulator: A "What-If" engine that simulates a 10% market crash to visualize potential capital loss.

Hackathon-Level UI: A modern, dark-themed dashboard built with Tailwind CSS and Glassmorphism aesthetics.

🛠️ Tech Stack
Backend: Python (Flask)

Machine Learning: Scikit-Learn (Random Forest), Pandas, NumPy

Frontend: HTML5, Tailwind CSS, JavaScript

Data Visualization: Plotly.js

API: Alpha Vantage (Real-time Market Data)

📊 How It Works
Data Acquisition: The system fetches real-time OHLC (Open, High, Low, Close) data via REST API.

Feature Engineering: It calculates price deltas and daily returns to prepare the dataset for the ML model.

Training: The Random Forest model runs in the background, analyzing patterns across 100+ decision trees to reach a probabilistic conclusion.

Risk Shield: The system measures "Market Noise" (volatility); if the risk exceeds a 2% threshold, a safety warning is triggered.

⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/YOUR_USERNAME/Stock-Shield.git
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
python app.py
Open http://127.0.0.1:5000 in your browser.
https://stockshield.streamlit.app/

📈 Future Roadmap
[ ] Sentiment Analysis: Integrating Twitter/X and News API to gauge market mood.

[ ] Portfolio Stress Test: Multi-stock risk assessment.

[ ] Email Alerts: Automated notifications when a stock hits a "High Risk" threshold.
