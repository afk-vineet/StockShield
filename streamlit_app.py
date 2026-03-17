import streamlit as st
import plotly.graph_objects as go
from model import get_analysis

# 1. Professional Dashboard Config
st.set_page_config(page_title="Stock Shield | AI Security", layout="wide", initial_sidebar_state="collapsed")

# 2. Enhanced CSS for Sleek UI
st.markdown("""
    <style>
        .stApp {
            background: #05070a;
            background-image: radial-gradient(at 0% 0%, rgba(29, 78, 216, 0.12) 0, transparent 50%), 
                              radial-gradient(at 100% 100%, rgba(16, 185, 129, 0.08) 0, transparent 50%);
            color: #f8fafc;
        }
        
        .glass-card {
            background: rgba(15, 23, 42, 0.6);
            backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 24px;
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            border-color: rgba(59, 130, 246, 0.4);
            background: rgba(15, 23, 42, 0.8);
            transform: translateY(-2px);
        }

        .glow-text { text-shadow: 0 0 30px rgba(59, 130, 246, 0.4); font-weight: 800; }

        @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
        .blink-dot {
            width: 8px; height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            display: inline-block;
            animation: blink 1.5s infinite;
            box-shadow: 0 0 10px #10b981;
            margin-right: 8px;
        }

        /* Clean Streamlit Interface */
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stButton>button {
            background: linear-gradient(90deg, #2563eb, #0891b2);
            border: none; color: white; border-radius: 12px; font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Handle Navigation Logic (Clickable Cards)
query_params = st.query_params
initial_symbol = query_params.get("search", "AAPL")

# 4. Hero Section
st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <span style="padding: 6px 14px; background: rgba(59, 130, 246, 0.1); color: #60a5fa; font-size: 11px; font-weight: 800; border-radius: 20px; letter-spacing: 1px; border: 1px solid rgba(59, 130, 246, 0.2);">
            AI-POWERED FINANCIAL SECURITY
        </span>
        <h1 style="font-size: 50px; margin-top: 15px; font-weight: 800;">
            Predict the Market. <span class="glow-text" style="color: #60a5fa;">Manage Risk.</span>
        </h1>
    </div>
""", unsafe_allow_html=True)

# 5. Search Section
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    symbol = st.text_input("", value=initial_symbol, placeholder="Search Stock Symbol...", label_visibility="collapsed").upper()
    analyze = st.button("RUN SHIELD ANALYSIS", use_container_width=True)

# 6. Result Logic
if analyze or "search" in query_params:
    with st.spinner('Analyzing market data...'):
        data = get_analysis(symbol)
        if data:
            st.markdown(f"### <span style='color:#64748b;'>Analysis for</span> {symbol}", unsafe_allow_html=True)
            
            # --- ROW 1: METRICS ---
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="glass-card"><p style="color:#94a3b8;font-size:11px;font-weight:bold;">LIVE PRICE</p><h2 style="font-size:36px;font-weight:800;">${data["price"]}</h2></div>', unsafe_allow_html=True)
            with m2:
                t_color = "#10b981" if data['trend'] == "UP" else "#ef4444"
                st.markdown(f'<div class="glass-card" style="border-bottom:3px solid {t_color};"><p style="color:#94a3b8;font-size:11px;font-weight:bold;">ML TREND</p><h2 style="font-size:36px;font-weight:800;color:{t_color};">{data["trend"]}</h2></div>', unsafe_allow_html=True)
            with m3:
                r_color = "#ef4444" if data['risk'] == "HIGH" else "#10b981"
                st.markdown(f'<div class="glass-card" style="border-bottom:3px solid {r_color};"><p style="color:#94a3b8;font-size:11px;font-weight:bold;">RISK SCORE</p><h2 style="font-size:36px;font-weight:800;color:{r_color};">{data["risk"]}</h2></div>', unsafe_allow_html=True)

            # --- ROW 2: ADVANCED CHART ---
            st.markdown("<br>", unsafe_allow_html=True)
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data['dates'], y=data['history'], 
                fill='tozeroy', 
                mode='lines',
                line=dict(width=4, color='#3b82f6'),
                fillcolor='rgba(59, 130, 246, 0.1)'
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#64748b'), margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.03)', side="right")
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- ROW 3: INTELLIGENCE CARDS ---
            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f'<div class="glass-card" style="border-left: 4px solid #3b82f6;"><p style="color:#3b82f6;font-size:11px;font-weight:bold;">MOMENTUM ANALYSIS (15D)</p><h3 style="margin:0;">{data["analysis"]["fifteen_day"]["trend"]} ({data["analysis"]["fifteen_day"]["change"]}%)</h3></div>', unsafe_allow_html=True)
            with d2:
                st.markdown(f'<div class="glass-card" style="background:rgba(59, 130, 246, 0.05); border-left: 4px solid #60a5fa;"><p style="color:#60a5fa;font-size:11px;font-weight:bold;">AI FORECAST (3-DAY)</p><h3 style="margin:0;color:#f8fafc;">{data["analysis"]["next_three"]["trend"]}</h3></div>', unsafe_allow_html=True)
            
            # Reset Button
            if st.button("CLEAR ANALYSIS"):
                st.query_params.clear()
                st.rerun()

        else:
            st.error("Invalid Stock Symbol or API Limit reached. Wait 60 seconds.")

# 7. CLICKABLE MARKET INTELLIGENCE
st.markdown("<br><br><h5 style='color:#475569; letter-spacing:1px; font-weight:800; font-size:12px;'>MARKET LEADERS</h5>", unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
stocks = ["RELIANCE.NS", "NVDA", "AAPL", "TSLA", "GOOGL"]
cols = [m1, m2, m3, m4, m5]

for i, s in enumerate(stocks):
    with cols[i]:
        # Using <a> tag to create a clickable card that updates the URL
        st.markdown(f"""
            <a href="?search={s}" target="_self" style="text-decoration: none;">
                <div class="glass-card" style="padding: 15px; text-align: center; cursor: pointer;">
                    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 5px;">
                        <span class="blink-dot"></span><span style="font-size: 10px; color: #10b981; font-weight: bold;">LIVE</span>
                    </div>
                    <h4 style="margin: 0; color: white;">{s}</h4>
                </div>
            </a>
        """, unsafe_allow_html=True)
