import streamlit as st
from model import get_analysis
import plotly.graph_objects as go

# Professional Dashboard Config
st.set_page_config(page_title="Stock Shield AI", layout="wide")

st.title("🛡️ Stock Shield: AI Financial Security")
st.markdown("### Predict the Market. Manage the Risk.")

# Sidebar Search
st.sidebar.header("Search Intelligence")
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, RELIANCE.NS)", "AAPL").upper()

if st.sidebar.button("Analyze Now"):
    data = get_analysis(symbol)
    
    if data:
        # Top Row Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${data['price']}")
        col2.metric("ML Prediction", data['trend'], delta_color="normal")
        col3.metric("Risk Level", data['risk'])

        # Chart Section
        fig = go.Figure(data=[go.Scatter(x=data['dates'], y=data['history'], fill='tozeroy')])
        fig.update_layout(title=f"{symbol} Performance History", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # Analysis Cards
        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**7-Day Trend:** {data['analysis']['seven_day']['trend']} ({data['analysis']['seven_day']['change']}%)")
        with c2:
            st.success(f"**AI Forecast:** {data['analysis']['next_three']['trend']}")
    else:
        st.error("API Limit reached or Invalid Symbol. Please wait 1 minute.")
