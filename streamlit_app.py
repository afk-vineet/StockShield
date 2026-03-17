import streamlit as st
import plotly.graph_objects as go
from model import get_analysis

# 1. Professional Dashboard Config
st.set_page_config(page_title="Stock Shield | AI Security", layout="wide", initial_sidebar_state="collapsed")

# 2. Inject Glassmorphism CSS & Blinking Animations
st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background: #05070a;
            background-image: radial-gradient(at 0% 0%, rgba(29, 78, 216, 0.15) 0, transparent 50%), 
                              radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.1) 0, transparent 50%);
            color: #f8fafc;
        }
        
        /* Glassmorphism Card Style */
        .glass-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 25px;
            transition: 0.4s;
            margin-bottom: 20px;
        }
        
        .glow-text { 
            text-shadow: 0 0 20px rgba(59, 130, 246, 0.5); 
            font-weight: 800; 
        }
        
        /* Blinking Active Dot */
        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        .blink-dot {
            width: 8px; height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            animation: blink 1.5s infinite;
            box-shadow: 0 0 8px #10b981;
            margin-right: 8px;
        }

        /* Hide Default Streamlit Header/Footer */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Hero Section
st.markdown("""
    <div style="text-align: center; padding: 40px 0;">
        <span style="padding: 6px 14px; background: rgba(59, 130, 246, 0.1); color: #60a5fa; font-size: 11px; font-weight: bold; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 20px; letter-spacing: 1px;">
            AI-POWERED FINANCIAL SECURITY
        </span>
        <h1 style="font-size: 55px; margin-top: 15px; line-height: 1.1; font-weight: 800;">
            Predict the Market.<br>
            <span class="glow-text" style="color: transparent; background: linear-gradient(to right, #60a5fa, #34d399); -webkit-background-clip: text;">Manage the Risk.</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# 4. Search Section (Centered)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    symbol = st.text_input("", placeholder="Enter Symbol (e.g., AAPL, RELIANCE.NS, NVDA)", label_visibility="collapsed").upper()
    search_btn = st.button("Analyze Now", use_container_width=True)

# 5. Analysis Logic
if search_btn or symbol:
    with st.spinner('Shielding capital...'):
        data = get_analysis(symbol)
        
        if data:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Metrics Row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="glass-card"><p style="color:#64748b;font-size:12px;font-weight:bold;">PRICE</p><h2 style="font-size:30px;font-weight:800;">${data["price"]}</h2></div>', unsafe_allow_html=True)
            with m2:
                t_color = "#10b981" if data['trend'] == "UP" else "#ef4444"
                st.markdown(f'<div class="glass-card" style="border-left:4px solid {t_color};"><p style="color:#64748b;font-size:12px;font-weight:bold;">ML PREDICTION</p><h2 style="font-size:30px;font-weight:800;color:{t_color};">{data["trend"]}</h2></div>', unsafe_allow_html=True)
            with m3:
                r_color = "#ef4444" if data['risk'] == "HIGH" else "#10b981"
                st.markdown(f'<div class="glass-card" style="border-left:4px solid {r_color};"><p style="color:#64748b;font-size:12px;font-weight:bold;">RISK LEVEL</p><h2 style="font-size:30px;font-weight:800;color:{r_color};">{data["risk"]}</h2></div>', unsafe_allow_html=True)

            # Chart Section
            fig = go.Figure(data=[go.Scatter(x=data['dates'], y=data['history'], fill='tozeroy', line=dict(color='#3b82f6', width=3))])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#64748b'),
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
            )
            st.plotly_chart(fig, use_container_width=True)

            # Detail Cards
            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f'<div class="glass-card"><p style="color:#3b82f6;font-size:11px;font-weight:bold;">7-DAY TREND</p><p style="font-size:18px;font-weight:700;">{data["analysis"]["seven_day"]["trend"]} ({data["analysis"]["seven_day"]["change"]}%)</p></div>', unsafe_allow_html=True)
            with d2:
                st.markdown(f'<div class="glass-card" style="background:rgba(59,130,246,0.05); border-top:2px solid #3b82f6;"><p style="color:#3b82f6;font-size:11px;font-weight:bold;">AI FORECAST (NEXT 3D)</p><p style="font-size:18px;font-weight:700;">{data["analysis"]["next_three"]["trend"]}</p></div>', unsafe_allow_html=True)
        else:
            st.error("API Limit reached or Invalid Symbol.")

# Default "Market Intelligence" view (when no search)
else:
    st.markdown("<br><br><h4 style='color:#64748b; letter-spacing:2px; font-size:14px; font-weight:bold;'>MARKET INTELLIGENCE</h4>", unsafe_allow_html=True)
    m1, m2, m3, m4, m5 = st.columns(5)
    stocks = ["AAPL", "NVDA", "TSLA", "RELIANCE.NS", "GOOGL"]
    cols = [m1, m2, m3, m4, m5]
    for i, s in enumerate(stocks):
        with cols[i]:
            st.markdown(f"""
                <div class="glass-card">
                    <div style="display:flex; align-items:center; margin-bottom:8px;">
                        <span class="blink-dot"></span><span style="font-size:10px; color:#10b981; font-weight:bold;">ACTIVE</span>
                    </div>
                    <h4 style="font-weight:800; margin:0;">{s}</h4>
                </div>
            """, unsafe_allow_html=True)
