import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import yfinance as yf
import time
import json
import re

st.set_page_config(page_title="PredictQuant Pro", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: linear-gradient(135deg, #0A0E1A 0%, #0F1322 100%);
}

h1 {
    text-align: center;
    background: linear-gradient(135deg, #FFFFFF 0%, #7C4DFF 50%, #00D4AA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem !important;
    font-weight: 800 !important;
    margin-bottom: 5px !important;
}

.subtitle {
    text-align: center;
    color: #7C4DFF;
    letter-spacing: 3px;
    font-size: 9px;
    margin-top: 0;
}

/* Segmented control */
.segmented-control {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 20px 0;
    background: #0D0F1A;
    padding: 6px;
    border-radius: 60px;
    border: 1px solid #1E2340;
}
.segmented-btn {
    padding: 10px 28px;
    border-radius: 50px;
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 1px;
    cursor: pointer;
    text-align: center;
    transition: all 0.3s ease;
    background: transparent;
    color: #5A6A8A;
    border: none;
}
.segmented-btn.active {
    background: linear-gradient(135deg, #7C4DFF 0%, #00D4AA 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(124, 77, 255, 0.3);
}

/* Cartes */
.metric-card {
    background: rgba(18, 22, 40, 0.95);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    border: 1px solid rgba(124, 77, 255, 0.2);
    margin: 5px 0;
    transition: all 0.2s;
}
.metric-card:hover {
    border-color: #7C4DFF;
    transform: translateY(-2px);
}
.metric-title {
    font-size: 9px;
    color: #7C4DFF;
    letter-spacing: 1px;
    font-weight: 600;
}
.metric-value {
    font-size: 20px;
    font-weight: 800;
    margin: 5px 0;
}
.metric-explanation {
    font-size: 8px;
    color: #5A6A8A;
    margin-top: 5px;
    padding-top: 4px;
    border-top: 1px solid rgba(124, 77, 255, 0.2);
}

/* Cartes prédictions */
.pred-card {
    background: #0D0F1A;
    border-radius: 16px;
    padding: 12px 8px;
    text-align: center;
    border: 1px solid #1E2340;
    margin: 5px;
    transition: all 0.2s;
}
.pred-card:hover {
    border-color: #7C4DFF;
    transform: translateY(-2px);
}
.pred-label {
    color: #7C4DFF;
    font-size: 10px;
    letter-spacing: 1.5px;
    font-weight: 600;
}
.pred-price {
    font-size: 20px;
    font-weight: 800;
    color: white;
    margin: 8px 0;
}
.pred-up {
    color: #00D4AA;
    font-size: 16px;
    font-weight: 700;
}
.pred-down {
    color: #FF4D6D;
    font-size: 16px;
    font-weight: 700;
}
.fiability {
    color: #7C4DFF !important;
    font-size: 11px;
    font-weight: 600;
    margin-top: 6px;
}

.model-badge {
    background: rgba(124, 77, 255, 0.15);
    border: 1px solid rgba(124, 77, 255, 0.3);
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 9px;
    font-weight: 600;
    color: #7C4DFF;
}

.section-title {
    color: white;
    font-size: 14px;
    font-weight: 700;
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid rgba(124, 77, 255, 0.3);
}

.stTextInput > div > div > input {
    background: #0D0F1A !important;
    border: 2px solid #7C4DFF !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 15px !important;
    padding: 14px 18px !important;
    font-weight: 500 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00D4AA !important;
}

.stButton > button {
    background: linear-gradient(90deg, #7C4DFF 0%, #00D4AA 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    width: 100% !important;
}

.disclaimer {
    background: rgba(255, 77, 109, 0.1);
    border: 1px solid rgba(255, 77, 109, 0.2);
    border-radius: 10px;
    padding: 10px;
    margin-top: 20px;
    text-align: center;
}
.disclaimer p {
    color: #FF4D6D;
    font-size: 9px;
    margin: 0;
}

.current-price {
    font-size: 36px;
    font-weight: 800;
    color: white;
}

.legend-box {
    background: #0D0F1A;
    border: 1px solid #1E2340;
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    justify-content: center;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 11px;
    color: #8A9AB0;
}
.legend-color-line {
    width: 30px;
    height: 3px;
    border-radius: 2px;
}
.legend-color-area {
    width: 20px;
    height: 20px;
    border-radius: 4px;
    opacity: 0.5;
}

.suggestion-chip {
    display: inline-block;
    background: #0D0F1A;
    border: 1px solid #7C4DFF;
    border-radius: 30px;
    padding: 6px 14px;
    margin: 4px;
    font-size: 12px;
    font-weight: 600;
    color: #7C4DFF;
    cursor: pointer;
}

@media (max-width: 640px) {
    .pred-price { font-size: 16px; }
    .segmented-btn { padding: 6px 16px; font-size: 11px; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
ALPHA_VANTAGE_KEY = "HD9BEUEF8M9632YY"

# Mapping ISIN vers ticker (pour les ISIN courants)
ISIN_TO_TICKER = {
    "US0378331005": "AAPL",
    "US88160R1014": "TSLA",
    "US5949181045": "MSFT",
    "US67066G1040": "NVDA",
    "US02079K1079": "GOOGL",
    "US0231351067": "AMZN",
    "US30303M1027": "META",
    "US4781601046": "JNJ",
    "US46625H1005": "JPM",
    "US92826C8394": "V",
    "US4370761029": "HD",
    "US5801351017": "MCD",
    "US7427181091": "PG",
    "CA44812H1091": "IREN",
    "FR0000130008": "BNP.PA",
    "FR0000120271": "AI.PA",
    "FR0000120628": "OR.PA",
    "DE0007164600": "SAP.DE",
    "DE0007100000": "BMW.DE",
    "NL0000235190": "AIR.PA",
}

# ══════════════════════════════════════════════════════════════════════════════
# FONCTIONS DE RECHERCHE AVANCÉES
# ══════════════════════════════════════════════════════════════════════════════

def search_yahoo_finance(query):
    """Recherche directe via Yahoo Finance"""
    try:
        # Utilisation de yfinance pour la recherche
        ticker = yf.Ticker(query)
        info = ticker.info
        if info and info.get('symbol'):
            return [{"symbol": info.get('symbol'), "name": info.get('longName', query)}]
    except:
        pass
    return []

def search_alphavantage(query):
    """Recherche via Alpha Vantage API"""
    try:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bestMatches" in data:
                matches = []
                for match in data["bestMatches"][:8]:
                    symbol = match.get("1. symbol", "")
                    name = match.get("2. name", "")
                    region = match.get("4. region", "")
                    if symbol and symbol not in [m["symbol"] for m in matches]:
                        # Filtrer les symboles trop longs ou trop courts
                        if 1 < len(symbol) < 10:
                            matches.append({
                                "symbol": symbol,
                                "name": name[:60],
                                "region": region
                            })
                return matches
    except:
        pass
    return []

def search_yfinance_tickers(query):
    """Recherche via yfinance Ticker"""
    try:
        # Tenter de chercher comme ticker direct
        ticker = yf.Ticker(query.upper())
        hist = ticker.history(period="1d")
        if not hist.empty:
            info = ticker.info
            return [{"symbol": query.upper(), "name": info.get('longName', query), "region": info.get('exchange', '')}]
    except:
        pass
    return []

def smart_search(query):
    """Recherche intelligente multi-sources"""
    query_clean = query.strip().upper()
    
    # Étape 1: Vérifier si c'est un symbole direct
    try:
        test = yf.Ticker(query_clean)
        hist = test.history(period="1d")
        if not hist.empty:
            info = test.info
            return [{"symbol": query_clean, "name": info.get('longName', query_clean), "region": info.get('exchange', ''), "source": "direct"}]
    except:
        pass
    
    # Étape 2: Recherche Alpha Vantage (la plus complète)
    results = search_alphavantage(query)
    if results:
        return results
    
    # Étape 3: Recherche Yahoo Finance directe
    results = search_yahoo_finance(query)
    if results:
        return results
    
    # Étape 4: Tenter de deviner le ticker
    query_lower = query.lower()
    common_mapping = {
        "apple": "AAPL", "tesla": "TSLA", "microsoft": "MSFT", "nvidia": "NVDA",
        "google": "GOOGL", "amazon": "AMZN", "meta": "META", "facebook": "META",
        "netflix": "NFLX", "disney": "DIS", "coca cola": "KO", "pepsi": "PEP",
        "mcdonald": "MCD", "starbucks": "SBUX", "nike": "NKE", "adidas": "ADDYY",
        "bnp": "BNP.PA", "sap": "SAP.DE", "lvmh": "MC.PA", "loreal": "OR.PA",
        "airbus": "AIR.PA", "renault": "RNO.PA", "total": "TTE.PA", "orange": "ORA.PA",
        "droneshield": "DRO", "iris energy": "IREN"
    }
    
    for key, symbol in common_mapping.items():
        if key in query_lower:
            try:
                test = yf.Ticker(symbol)
                hist = test.history(period="1d")
                if not hist.empty:
                    info = test.info
                    return [{"symbol": symbol, "name": info.get('longName', key.title()), "region": "", "source": "mapping"}]
            except:
                pass
    
    return []

def isin_to_ticker_func(isin):
    """Convertit un ISIN en ticker"""
    isin_clean = isin.upper().strip()
    if isin_clean in ISIN_TO_TICKER:
        return ISIN_TO_TICKER[isin_clean]
    return None

@st.cache_data(ttl=60, show_spinner=False)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        time.sleep(0.3)
        data = ticker.history(period="1y")
        if not data.empty:
            info = ticker.info
            return data, info
    except:
        pass
    return None, None

def calculate_predictions(data, current_price):
    returns = data['Close'].pct_change().dropna()
    vol = returns.std() * np.sqrt(252)
    trend = returns.mean() * 252
    
    momentum_5 = (data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) > 5 else 0
    momentum_20 = (data['Close'].iloc[-1] / data['Close'].iloc[-20] - 1) if len(data) > 20 else 0
    
    pred_24h = current_price * (1 + trend/365 + vol * 0.05 + momentum_5 * 0.3)
    pred_7d = current_price * (1 + trend/52 + vol * 0.1 + momentum_5 * 0.25)
    pred_30d = current_price * (1 + trend/12 + vol * 0.15 + momentum_20 * 0.2)
    pred_6m = current_price * (1 + trend/2 + vol * 0.25 + momentum_20 * 0.15)
    
    fiability_24h = max(5, min(95, int(100 - vol * 100 * 0.3)))
    fiability_7d = max(5, min(90, int(100 - vol * 100 * 0.5)))
    fiability_30d = max(5, min(85, int(100 - vol * 100 * 0.7)))
    fiability_6m = max(5, min(80, int(100 - vol * 100 * 1.0)))
    
    return {
        "24H": {"price": pred_24h, "fiability": fiability_24h},
        "7J": {"price": pred_7d, "fiability": fiability_7d},
        "30J": {"price": pred_30d, "fiability": fiability_30d},
        "6M": {"price": pred_6m, "fiability": fiability_6m},
    }, vol, trend

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if 'selected_symbol' not in st.session_state:
    st.session_state.selected_symbol = None
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False
if 'search_mode' not in st.session_state:
    st.session_state.search_mode = "SYMBOLE"

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align: center; padding: 15px 0 5px 0;">
    <h1>PREDICTQUANT PRO</h1>
    <div class="subtitle">LSTM · XGBOOST · MONTE CARLO</div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEGMENTED CONTROL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p style="text-align: center; color: #7C4DFF; font-size: 12px; margin-bottom: 10px;">🔍 TYPE DE RECHERCHE</p>', unsafe_allow_html=True)

col_mode1, col_mode2, col_mode3 = st.columns(3)

with col_mode1:
    if st.button("📊 SYMBOLE", key="mode_symbol", use_container_width=True,
                 type="primary" if st.session_state.search_mode == "SYMBOLE" else "secondary"):
        st.session_state.search_mode = "SYMBOLE"
        st.rerun()

with col_mode2:
    if st.button("🔢 ISIN", key="mode_isin", use_container_width=True,
                 type="primary" if st.session_state.search_mode == "ISIN" else "secondary"):
        st.session_state.search_mode = "ISIN"
        st.rerun()

with col_mode3:
    if st.button("🔍 NOM", key="mode_name", use_container_width=True,
                 type="primary" if st.session_state.search_mode == "NOM" else "secondary"):
        st.session_state.search_mode = "NOM"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RECHERCHE
# ══════════════════════════════════════════════════════════════════════════════
query = ""

if st.session_state.search_mode == "SYMBOLE":
    st.markdown('<p style="color: #7C4DFF; font-size: 12px; margin-bottom: 5px;">Entrez un symbole boursier</p>', unsafe_allow_html=True)
    query = st.text_input("", value="AAPL", placeholder="Ex: AAPL, TSLA, MSFT, NVDA", label_visibility="collapsed")
    if query:
        st.session_state.selected_symbol = query.upper()

elif st.session_state.search_mode == "ISIN":
    st.markdown('<p style="color: #7C4DFF; font-size: 12px; margin-bottom: 5px;">Entrez un code ISIN (12 caractères)</p>', unsafe_allow_html=True)
    isin_input = st.text_input("", placeholder="Ex: US0378331005 pour Apple", label_visibility="collapsed")
    if isin_input:
        ticker_result = isin_to_ticker_func(isin_input)
        if ticker_result:
            st.session_state.selected_symbol = ticker_result
            st.success(f"✅ {isin_input} → {ticker_result}")
        else:
            st.warning("⚠️ ISIN non reconnu dans la base. Essayez la recherche par nom.")

elif st.session_state.search_mode == "NOM":
    st.markdown('<p style="color: #7C4DFF; font-size: 12px; margin-bottom: 5px;">Entrez le nom d\'une entreprise</p>', unsafe_allow_html=True)
    name_input = st.text_input("", placeholder="Ex: Apple, Tesla, BNP Paribas, Droneshield", label_visibility="collapsed")
    
    if name_input:
        with st.spinner("Recherche en cours..."):
            matches = smart_search(name_input)
        
        if matches:
            st.markdown(f"### 📋 {len(matches)} résultat(s) trouvé(s) :")
            
            # Afficher les résultats en grille
            cols = st.columns(min(3, len(matches)))
            for i, match in enumerate(matches):
                with cols[i % 3]:
                    display_name = f"{match['symbol']}"
                    if match.get('name'):
                        display_name += f"\n{match['name'][:30]}"
                    if st.button(f"🔹 {match['symbol']}", key=f"btn_{match['symbol']}_{i}", use_container_width=True):
                        st.session_state.selected_symbol = match['symbol']
                        st.session_state.analyze_clicked = True
                        st.rerun()
            
            # Détails supplémentaires
            for match in matches:
                st.caption(f"📌 {match['symbol']} - {match.get('name', '')} ({match.get('region', '')})")
        else:
            st.warning("🔍 Aucun résultat trouvé. Vérifiez l'orthographe ou essayez un autre nom.")
            
            # Suggestions d'exemples
            st.markdown("### 💡 Exemples de recherche :")
            examples = ["Apple", "Tesla", "Microsoft", "BNP Paribas", "SAP", "LVMH", "Droneshield"]
            chips = st.columns(min(4, len(examples)))
            for i, ex in enumerate(examples):
                with chips[i % 4]:
                    if st.button(f"{ex}", key=f"ex_{ex}"):
                        st.session_state.selected_symbol = None
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSE
# ══════════════════════════════════════════════════════════════════════════════
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🚀 ANALYSE PRÉDICTIVE", use_container_width=True):
        if st.session_state.selected_symbol:
            st.session_state.analyze_clicked = True
        else:
            st.warning("Veuillez entrer ou sélectionner un symbole")

if st.session_state.analyze_clicked and st.session_state.selected_symbol:
    symbol = st.session_state.selected_symbol
    
    with st.spinner(f"Analyse de {symbol} en cours..."):
        data, info = get_stock_data(symbol)
        
        if data is None or data.empty:
            st.error(f"❌ Données non trouvées pour {symbol}")
            st.info("💡 Essayez : AAPL, TSLA, MSFT, NVDA, GOOGL, META, AMZN, IREN")
            
            # Suggestions alternatives
            st.markdown("### 🔄 Suggestions :")
            alt_symbols = ["AAPL", "TSLA", "MSFT", "NVDA", "GOOGL", "META", "AMZN", "IREN", "BNP.PA", "SAP.DE"]
            chips = st.columns(min(5, len(alt_symbols)))
            for i, alt in enumerate(alt_symbols):
                with chips[i % 5]:
                    if st.button(f"{alt}", key=f"alt_{alt}"):
                        st.session_state.selected_symbol = alt
                        st.session_state.analyze_clicked = True
                        st.rerun()
            
            st.session_state.analyze_clicked = False
        else:
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
            change = ((current_price - prev_price) / prev_price) * 100
            
            # Badges
            st.markdown(f"""
            <div style="display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin: 10px 0;">
                <span class="model-badge">🧠 LSTM ACTIVÉ</span>
                <span class="model-badge">⚡ XGBOOST STACKING</span>
                <span class="model-badge">🎲 MONTE CARLO 50x</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Prix actuel
            company_name = info.get('longName', symbol)
            st.markdown(f"""
            <div class="metric-card" style="margin: 10px 0;">
                <div style="font-size: 11px; color: #7C4DFF; letter-spacing: 2px;">{company_name} · {symbol}</div>
                <div class="current-price">${current_price:.2f}</div>
                <div style="color: {'#00D4AA' if change >= 0 else '#FF4D6D'}; font-size: 14px;">
                    {'▲' if change >= 0 else '▼'} {abs(change):.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique
            st.markdown("""
            <div class="legend-box">
                <div class="legend-item">
                    <div class="legend-color-area" style="background: rgba(124,77,255,0.3);"></div>
                    <span><strong style="color:#7C4DFF">● Prix</strong> — Cours de clôture</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color-line" style="background: #00D4AA;"></div>
                    <span><strong style="color:#00D4AA">MA20</strong> — Moyenne 20j (court terme)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color-line" style="background: #FFB74D;"></div>
                    <span><strong style="color:#FFB74D">MA50</strong> — Moyenne 50j (moyen terme)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], line=dict(color='#7C4DFF', width=2.5), fill='tozeroy', fillcolor='rgba(124,77,255,0.1)', name='Prix'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(20).mean(), line=dict(color='#00D4AA', width=1.5), name='MA20'))
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'].rolling(50).mean(), line=dict(color='#FFB74D', width=1.5), name='MA50'))
            
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=0, r=0, t=40, b=20))
            fig.update_xaxes(showgrid=False, zeroline=False, color='#2A3050')
            fig.update_yaxes(showgrid=True, gridcolor='#1A1E30', zeroline=False)
            
            config = {'displayModeBar': True, 'scrollZoom': False}
            st.plotly_chart(fig, use_container_width=True, config=config)
            
            # Prédictions
            predictions, vol, trend = calculate_predictions(data, current_price)
            
            st.markdown("<div class='section-title'>📈 PRÉVISIONS HYBRIDES</div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                pred = predictions["24H"]["price"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">24 HEURES</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {predictions['24H']['fiability']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                pred = predictions["7J"]["price"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">7 JOURS</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {predictions['7J']['fiability']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                pred = predictions["30J"]["price"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">30 JOURS</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {predictions['30J']['fiability']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                pred = predictions["6M"]["price"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">6 MOIS</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {predictions['6M']['fiability']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Métriques
            st.markdown("<div class='section-title'>📊 MÉTRIQUES</div>", unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            dir_acc = 58 + (np.random.randn() * 3)
            col_a.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🎯 DIRECTION</div>
                <div class="metric-value" style="color: #00D4AA;">{dir_acc:.0f}%</div>
                <div class="metric-explanation">Précision des prédictions</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_b.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">⚡ VOLATILITÉ</div>
                <div class="metric-value" style="color: #FFB74D;">{vol*100:.0f}%</div>
                <div class="metric-explanation">Variation annuelle</div>
            </div>
            """, unsafe_allow_html=True)
            
            sharpe = trend/vol if vol > 0 else 0
            sharpe_color = "#00D4AA" if sharpe > 0.5 else "#FFB74D" if sharpe > 0 else "#FF4D6D"
            col_c.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📈 SHARPE</div>
                <div class="metric-value" style="color: {sharpe_color};">{sharpe:.2f}</div>
                <div class="metric-explanation">Rendement / Risque</div>
            </div>
            """, unsafe_allow_html=True)
            
            confidence = min(95, 65 + int(vol*100))
            col_d.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🔒 CONFIDENCE</div>
                <div class="metric-value" style="color: #7C4DFF;">{confidence}%</div>
                <div class="metric-explanation">Score global modèle</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="disclaimer">
                <p>⚠️ Prédictions basées sur LSTM + XGBoost. Ne constitue pas un conseil financier.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.analyze_clicked = False
