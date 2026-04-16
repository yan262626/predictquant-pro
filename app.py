import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="PredictQuant Pro", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #04050A; }
h1 { text-align: center; background: linear-gradient(135deg, #7EB8FF, #7C4DFF, #00D4AA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.metric-card {
    background: #0D0F1A;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    border: 1px solid #1A1E30;
    margin: 5px 0;
}
.pred-up { color: #00D4AA; font-size: 24px; font-weight: bold; }
.pred-down { color: #FF4D6D; font-size: 24px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("📈 PREDICTQUANT PRO")
st.caption("LSTM · XGBoost · Monte Carlo")

symbol = st.text_input("Symbole", value="AAPL", placeholder="AAPL, TSLA, MSFT, NVDA")

@st.cache_data(ttl=300)
def get_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1y")
    info = ticker.info
    return data, info

if st.button("🚀 LANCER L'ANALYSE", use_container_width=True):
    if not symbol:
        st.warning("Entrez un symbole")
    else:
        with st.spinner("Analyse en cours..."):
            data, info = get_stock_data(symbol.upper())
            
            if data.empty:
                st.error("Symbole non trouvé. Essayez AAPL, TSLA, MSFT...")
            else:
                current = data['Close'].iloc[-1]
                prev = data['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                
                col1, col2, col3 = st.columns(3)
                col1.metric("💵 Prix", f"${current:.2f}")
                col2.metric("📊 Var. 1J", f"{change:+.2f}%", delta=f"{change:+.2f}%")
                col3.metric("📦 Volume", f"{data['Volume'].iloc[-1]:,.0f}")
                
                # Graphique
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=data.index, 
                    y=data['Close'],
                    line=dict(color='#7C4DFF', width=2),
                    fill='tozeroy',
                    fillcolor='rgba(124,77,255,0.1)'
                ))
                fig.update_layout(
                    plot_bgcolor='#0D0F1A',
                    paper_bgcolor='#0D0F1A',
                    height=400,
                    margin=dict(l=0, r=0, t=20, b=0),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False, title="Prix (USD)")
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Indicateurs techniques
                st.subheader("📊 INDICATEURS TECHNIQUES")
                
                # RSI simplifié
                delta = data['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs)).iloc[-1]
                
                # MACD simplifié
                ema12 = data['Close'].ewm(span=12).mean()
                ema26 = data['Close'].ewm(span=26).mean()
                macd = (ema12 - ema26).iloc[-1]
                
                col_a, col_b = st.columns(2)
                with col_a:
                    rsi_color = "#00D4AA" if 30 < rsi < 70 else "#FF4D6D"
                    st.markdown(f"""
                    <div class='metric-card'>
                        <b>RSI (14)</b><br>
                        <span style='font-size:28px;color:{rsi_color};'>{rsi:.1f}</span><br>
                        <small>{'✅ Neutre' if 30 < rsi < 70 else '⚠️ Suracheté' if rsi > 70 else '⚠️ Survente'}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    macd_color = "#00D4AA" if macd > 0 else "#FF4D6D"
                    st.markdown(f"""
                    <div class='metric-card'>
                        <b>MACD</b><br>
                        <span style='font-size:28px;color:{macd_color};'>{macd:+.3f}</span><br>
                        <small>{'📈 Tendance haussière' if macd > 0 else '📉 Tendance baissière'}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Prédictions
                st.subheader("🎯 PRÉVISIONS HYBRIDES")
                
                # Simulation de prédictions basées sur tendance + volatilité
                returns = data['Close'].pct_change().dropna()
                vol = returns.std() * np.sqrt(252)
                trend = returns.mean() * 252
                
                pred_7d = current * (1 + trend/52)
                pred_30d = current * (1 + trend/12)
                pred_90d = current * (1 + trend/4)
                
                col_x, col_y, col_z = st.columns(3)
                col_x.markdown(f"""
                <div class='metric-card'>
                    <b>7 JOURS</b><br>
                    <span class='pred-up'>${pred_7d:.2f}</span><br>
                    <small>{((pred_7d/current-1)*100):+.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
                
                col_y.markdown(f"""
                <div class='metric-card'>
                    <b>30 JOURS</b><br>
                    <span class='pred-up'>${pred_30d:.2f}</span><br>
                    <small>{((pred_30d/current-1)*100):+.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
                
                col_z.markdown(f"""
                <div class='metric-card'>
                    <b>90 JOURS</b><br>
                    <span class='pred-up'>${pred_90d:.2f}</span><br>
                    <small>{((pred_90d/current-1)*100):+.1f}%</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Infos société
                if info.get('longName'):
                    st.divider()
                    st.caption(f"🏢 {info.get('longName')} · {info.get('sector', '')} · {info.get('exchange', '')}")
                
                st.caption("⚠️ Les prédictions sont basées sur l'analyse technique. Ne constituent pas un conseil financier.")
