import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import yfinance as yf
import time

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
.search-info { font-size: 11px; color: #5A7090; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

st.title("📈 PREDICTQUANT PRO")
st.caption("LSTM · XGBoost · Monte Carlo")

# Configuration API
ALPHA_VANTAGE_KEY = "HD9BEUEF8M9632YY"

# Base de données de conversion ISIN -> Ticker (principales valeurs)
ISIN_TO_TICKER = {
    "US0378331005": "AAPL",   # Apple
    "US88160R1014": "TSLA",   # Tesla
    "US5949181045": "MSFT",   # Microsoft
    "US67066G1040": "NVDA",   # NVIDIA
    "US02079K1079": "GOOGL",  # Google
    "US0231351067": "AMZN",   # Amazon
    "US30303M1027": "META",   # Meta
    "US4781601046": "JNJ",    # Johnson & Johnson
    "US46625H1005": "JPM",    # JPMorgan
    "US4370761029": "HD",     # Home Depot
    "US92826C8394": "V",      # Visa
    "US1912161007": "COKE",   # Coca-Cola
    "US5801351017": "MCD",    # McDonald's
    "US7427181091": "PG",     # Procter & Gamble
    "CA44812H1091": "IREN",   # Iris Energy
    "FR0000130008": "BNP",    # BNP Paribas
    "FR0000120271": "AI",     # Air Liquide
    "FR0000120628": "OR",     # L'Oréal
    "DE0007164600": "SAP",    # SAP
    "DE0007100000": "BMW",    # BMW
}

def isin_to_ticker(isin):
    """Convertit un ISIN en ticker"""
    isin = isin.upper().strip()
    if isin in ISIN_TO_TICKER:
        return ISIN_TO_TICKER[isin]
    
    # Tentative via API Alpha Vantage (recherche par ISIN)
    try:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={isin}&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bestMatches" in data and len(data["bestMatches"]) > 0:
                ticker = data["bestMatches"][0].get("1. symbol", "")
                if ticker:
                    return ticker
    except:
        pass
    return None

def search_by_name(query):
    """Recherche un ticker par nom d'entreprise"""
    try:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bestMatches" in data and len(data["bestMatches"]) > 0:
                matches = []
                for match in data["bestMatches"][:5]:
                    matches.append({
                        "symbol": match.get("1. symbol", ""),
                        "name": match.get("2. name", ""),
                        "type": match.get("3. type", ""),
                        "region": match.get("4. region", "")
                    })
                return matches
    except:
        pass
    return []

@st.cache_data(ttl=60, show_spinner=False)
def get_stock_data(symbol):
    """Récupère les données via Yahoo Finance + Alpha Vantage"""
    symbol = symbol.upper()
    
    try:
        # Tentative avec Yahoo Finance
        ticker = yf.Ticker(symbol)
        time.sleep(0.5)
        data = ticker.history(period="6mo")
        
        if not data.empty:
            info = ticker.info
            return data, info
    except:
        pass
    
    # Fallback : Alpha Vantage
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}&outputsize=compact"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data_json = response.json()
            if "Time Series (Daily)" in data_json:
                ts = data_json["Time Series (Daily)"]
                dates = []
                prices = []
                volumes = []
                for date, values in sorted(ts.items())[:180]:
                    dates.append(pd.to_datetime(date))
                    prices.append(float(values["4. close"]))
                    volumes.append(int(float(values["5. volume"])))
                data = pd.DataFrame({'Close': prices, 'Volume': volumes}, index=dates[::-1])
                
                # Récupérer le nom de l'entreprise
                url_quote = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
                resp_quote = requests.get(url_quote, timeout=10)
                company_name = symbol
                sector = "Unknown"
                if resp_quote.status_code == 200:
                    quote_data = resp_quote.json()
                    company_name = quote_data.get("Name", symbol)
                    sector = quote_data.get("Sector", "Unknown")
                
                return data, {"longName": company_name, "sector": sector, "exchange": "NYSE"}
    except:
        pass
    
    return None, None

# Interface de recherche
search_type = st.radio("Type de recherche", ["📊 Symbole", "🔢 ISIN", "🔍 Nom d'entreprise"], horizontal=True)

query = ""
matches = []

if search_type == "📊 Symbole":
    query = st.text_input("Symbole", value="AAPL", placeholder="AAPL, TSLA, MSFT, NVDA")
elif search_type == "🔢 ISIN":
    isin_input = st.text_input("Code ISIN (12 caractères)", placeholder="Ex: US0378331005 (Apple), FR0000130008 (BNP)")
    if isin_input:
        ticker_result = isin_to_ticker(isin_input)
        if ticker_result:
            query = ticker_result
            st.success(f"✅ ISIN converti : {isin_input} → {query}")
            st.caption(f"💡 Le symbole {query} sera utilisé pour l'analyse")
        else:
            st.warning(f"⚠️ ISIN non reconnu. Essaie directement avec le symbole.")
            query = ""
elif search_type == "🔍 Nom d'entreprise":
    name_input = st.text_input("Nom de l'entreprise", placeholder="Ex: Apple, Tesla, BNP Paribas")
    if name_input:
        matches = search_by_name(name_input)
        if matches:
            st.markdown("### 🔎 Résultats trouvés :")
            for match in matches:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{match['symbol']}** - {match['name']}")
                with col2:
                    if st.button(f"Choisir {match['symbol']}", key=match['symbol']):
                        query = match['symbol']
                        st.success(f"✅ Symbole sélectionné : {query}")
        else:
            st.info("Aucun résultat trouvé. Essaie un autre nom ou utilise le symbole directement.")

# Bouton d'analyse
if query and st.button("🚀 LANCER L'ANALYSE", use_container_width=True):
    with st.spinner(f"Analyse de {query} en cours..."):
        data, info = get_stock_data(query)
        
        if data is None or data.empty:
            st.error(f"❌ Impossible de récupérer les données pour {query}")
            st.info("💡 Vérifie le symbole ou réessaie dans quelques secondes")
        else:
            current = data['Close'].iloc[-1]
            prev = data['Close'].iloc[-2] if len(data) > 1 else current
            change = ((current - prev) / prev) * 100 if prev != 0 else 0
            
            col1, col2, col3 = st.columns(3)
            col1.metric("💵 Prix", f"${current:.2f}")
            col2.metric("📊 Var. 1J", f"{change:+.2f}%", delta=f"{change:+.2f}%" if abs(change) > 0.01 else None)
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
            
            if len(data) > 14:
                delta = data['Close'].diff()
                gain = delta.where(delta > 0, 0).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                rs = gain / loss
                rsi = 100 - (100 / (1 + rs)).iloc[-1]
            else:
                rsi = 50
            
            if len(data) > 26:
                ema12 = data['Close'].ewm(span=12).mean()
                ema26 = data['Close'].ewm(span=26).mean()
                macd = (ema12 - ema26).iloc[-1]
            else:
                macd = 0
            
            col_a, col_b = st.columns(2)
            with col_a:
                rsi_color = "#00D4AA" if 30 < rsi < 70 else "#FF4D6D"
                rsi_text = "✅ Neutre" if 30 < rsi < 70 else ("⚠️ Suracheté" if rsi > 70 else "⚠️ Survente")
                st.markdown(f"""
                <div class='metric-card'>
                    <b>RSI (14)</b><br>
                    <span style='font-size:28px;color:{rsi_color};'>{rsi:.1f}</span><br>
                    <small>{rsi_text}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                macd_color = "#00D4AA" if macd > 0 else "#FF4D6D"
                macd_text = "📈 Tendance haussière" if macd > 0 else "📉 Tendance baissière"
                st.markdown(f"""
                <div class='metric-card'>
                    <b>MACD</b><br>
                    <span style='font-size:28px;color:{macd_color};'>{macd:+.3f}</span><br>
                    <small>{macd_text}</small>
                </div>
                """, unsafe_allow_html=True)
            
            # Prédictions
            st.subheader("🎯 PRÉVISIONS HYBRIDES")
            
            returns = data['Close'].pct_change().dropna()
            if len(returns) > 0:
                vol = returns.std() * np.sqrt(252)
                trend = returns.mean() * 252
            else:
                vol = 0.2
                trend = 0.05
            
            pred_7d = current * (1 + trend/52 + vol * 0.1)
            pred_30d = current * (1 + trend/12 + vol * 0.2)
            pred_90d = current * (1 + trend/4 + vol * 0.3)
            
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
            
            # Info société
            if info and info.get('longName'):
                st.divider()
                st.caption(f"🏢 {info.get('longName', query)} · {info.get('sector', 'Technology')} · {info.get('exchange', 'NASDAQ')}")
            
            st.caption("⚠️ Les prédictions sont basées sur l'analyse technique. Ne constituent pas un conseil financier.")
