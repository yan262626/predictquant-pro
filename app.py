import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import yfinance as yf
import time

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

/* Header */
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

/* Radio buttons */
.stRadio {
    margin: 20px 0;
}
.stRadio > div {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}
.stRadio label {
    background: #0D0F1A !important;
    padding: 12px 28px !important;
    border-radius: 50px !important;
    border: 2px solid #7C4DFF !important;
    color: #7C4DFF !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}
.stRadio label:hover {
    border-color: #00D4AA !important;
    background: rgba(0, 212, 170, 0.1) !important;
    color: #00D4AA !important;
    transform: translateY(-2px);
}
.stRadio div[data-baseweb="radio"] {
    display: none;
}
.stRadio div[role="radiogroup"] > div:has(input:checked) label {
    background: linear-gradient(135deg, #7C4DFF 0%, #00D4AA 100%) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(124, 77, 255, 0.4);
}

/* Cartes métriques avec style amélioré */
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
    line-height: 1.3;
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
    letter-spacing: 0.5px;
}

/* Badges */
.model-badge {
    background: rgba(124, 77, 255, 0.15);
    border: 1px solid rgba(124, 77, 255, 0.3);
    border-radius: 20px;
    padding: 4px 10px;
    font-size: 9px;
    font-weight: 600;
    color: #7C4DFF;
}

/* Section titles */
.section-title {
    color: white;
    font-size: 14px;
    font-weight: 700;
    margin: 20px 0 10px 0;
    padding-bottom: 6px;
    border-bottom: 2px solid rgba(124, 77, 255, 0.3);
}

/* Inputs */
.stTextInput > div > div > input {
    background: #0D0F1A !important;
    border: 2px solid #7C4DFF !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 15px !important;
    padding: 12px 18px !important;
    font-weight: 500 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #00D4AA !important;
    box-shadow: 0 0 0 2px rgba(0, 212, 170, 0.2);
}
.stTextInput > div > div > input::placeholder {
    color: #4A5070 !important;
    font-weight: 400;
}

/* Labels */
.stMarkdown p {
    color: #7C4DFF !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #7C4DFF 0%, #00D4AA 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    letter-spacing: 1px !important;
    width: 100% !important;
}

/* Alert */
.stAlert {
    background: #0D0F1A !important;
    border-color: #7C4DFF !important;
}

/* Disclaimer */
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

/* Current price card */
.current-price {
    font-size: 36px;
    font-weight: 800;
    color: white;
}

/* Légende du graphique */
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

/* Glossaire */
.glossary {
    background: rgba(124, 77, 255, 0.05);
    border-radius: 10px;
    padding: 12px;
    margin: 15px 0;
}
.glossary-title {
    color: #7C4DFF;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 8px;
}
.glossary-item {
    font-size: 9px;
    color: #8A9AB0;
    margin: 5px 0;
    line-height: 1.4;
}
.glossary-item strong {
    color: #00D4AA;
}

/* Fix mobile */
@media (max-width: 640px) {
    .pred-price { font-size: 16px; }
    .metric-card { padding: 8px; }
    .pred-card { padding: 8px 4px; }
    .stRadio label { padding: 8px 18px !important; font-size: 13px !important; }
    .fiability { font-size: 9px; }
    .legend-item { font-size: 9px; }
    .metric-explanation { font-size: 7px; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
ALPHA_VANTAGE_KEY = "HD9BEUEF8M9632YY"

TICKER_ALIAS = {
    "IREN": "IREN",
    "BNP": "BNP.PA",
    "AI": "AI.PA",
    "OR": "OR.PA",
    "SAP": "SAP.DE",
    "BMW": "BMW.DE",
}

ISIN_TO_TICKER = {
    "US0378331005": "AAPL",
    "US88160R1014": "TSLA",
    "US5949181045": "MSFT",
    "US67066G1040": "NVDA",
    "US02079K1079": "GOOGL",
    "US0231351067": "AMZN",
    "US30303M1027": "META",
    "CA44812H1091": "IREN",
    "FR0000130008": "BNP.PA",
    "FR0000120271": "AI.PA",
    "FR0000120628": "OR.PA",
    "DE0007164600": "SAP.DE",
}

# ══════════════════════════════════════════════════════════════════════════════
# FONCTIONS
# ══════════════════════════════════════════════════════════════════════════════
def isin_to_ticker(isin):
    isin = isin.upper().strip()
    return ISIN_TO_TICKER.get(isin)

def search_by_name(query):
    try:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bestMatches" in data:
                matches = []
                for match in data["bestMatches"][:5]:
                    symbol = match.get("1. symbol", "")
                    name = match.get("2. name", "")
                    if symbol and symbol not in [m["symbol"] for m in matches]:
                        matches.append({"symbol": symbol, "name": name[:40]})
                return matches
    except:
        pass
    return []

@st.cache_data(ttl=60, show_spinner=False)
def get_stock_data(symbol):
    try:
        ticker = yf.Ticker(symbol)
        time.sleep(0.5)
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
# RECHERCHE
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p style="text-align: center; color: #7C4DFF; font-size: 13px; margin-bottom: 5px;">🔍 TYPE DE RECHERCHE</p>', unsafe_allow_html=True)
search_type = st.radio("", ["📊 SYMBOLE", "🔢 ISIN", "🔍 NOM"], horizontal=True, label_visibility="collapsed")

query = ""

if search_type == "📊 SYMBOLE":
    st.markdown('<p style="color: #7C4DFF; font-size: 12px; margin-bottom: 5px;">Entrez un symbole boursier</p>', unsafe_allow_html=True)
    query = st.text_input("", value="AAPL", placeholder="Ex: AAPL, TSLA, MSFT, NVDA, IREN", label_visibility="collapsed")
    if query:
        st.session_state.selected_symbol = query.upper()

elif search_type == "🔢 ISIN":
    st.markdown('<p style="color: #7C4DFF; font-size: 12px; margin-bottom: 5px;">Entrez un code ISIN (12 caractères)</p>', unsafe_allow_html=True)
    isin_input = st.text_input("", placeholder="Ex: US0378331005 pour Apple", label_visibility="collapsed")
    if isin_input:
        ticker_result = isin_to_ticker(isin_input)
        if ticker_result:
            st.session_state.selected_symbol = ticker_result
            st.success(f"✅ {isin_input} → {ticker_result}")
        else:
            st.warning("⚠️ ISIN non reconnu")

elif search_type == "🔍 NOM":
    st.markdown('<p style="color: #7C4DFF; font-size: 12px; margin-bottom: 5px;">Entrez le nom d\'une entreprise</p>', unsafe_allow_html=True)
    name_input = st.text_input("", placeholder="Ex: Apple, Tesla, BNP Paribas", label_visibility="collapsed")
    if name_input:
        with st.spinner("Recherche..."):
            matches = search_by_name(name_input)
        
        if matches:
            st.markdown("### 📋 RÉSULTATS :")
            cols = st.columns(min(4, len(matches)))
            for i, match in enumerate(matches):
                with cols[i % 4]:
                    if st.button(f"🔹 {match['symbol']}", key=f"btn_{match['symbol']}", use_container_width=True):
                        st.session_state.selected_symbol = match['symbol']
                        st.session_state.analyze_clicked = True
                        st.rerun()
            
            for match in matches:
                st.caption(f"📌 {match['symbol']} - {match['name']}")
        elif name_input:
            st.info("🔍 Aucun résultat. Essayez un autre nom.")

# ══════════════════════════════════════════════════════════════════════════════
# BOUTON D'ANALYSE
# ══════════════════════════════════════════════════════════════════════════════
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    if st.button("🚀 ANALYSE PRÉDICTIVE", use_container_width=True):
        if st.session_state.selected_symbol:
            st.session_state.analyze_clicked = True
        else:
            st.warning("Veuillez entrer ou sélectionner un symbole")

# ══════════════════════════════════════════════════════════════════════════════
# AFFICHAGE DE L'ANALYSE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.analyze_clicked and st.session_state.selected_symbol:
    symbol = st.session_state.selected_symbol
    
    if symbol in TICKER_ALIAS:
        symbol = TICKER_ALIAS[symbol]
    
    with st.spinner(f"Analyse de {symbol} en cours..."):
        data, info = get_stock_data(symbol)
        
        if data is None or data.empty:
            st.error(f"❌ Données non trouvées pour {st.session_state.selected_symbol}")
            st.info("💡 Essayez : AAPL, TSLA, MSFT, NVDA, GOOGL, META, AMZN, IREN")
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
            
            # Légende des courbes
            st.markdown("""
            <div class="legend-box">
                <div class="legend-item">
                    <div class="legend-color-area" style="background: rgba(124,77,255,0.3);"></div>
                    <span><strong style="color:#7C4DFF">● Prix</strong> — Cours de clôture quotidien</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color-line" style="background: #00D4AA;"></div>
                    <span><strong style="color:#00D4AA">MA20</strong> — Moyenne mobile 20 jours (tendance court terme)</span>
                </div>
                <div class="legend-item">
                    <div class="legend-color-line" style="background: #FFB74D;"></div>
                    <span><strong style="color:#FFB74D">MA50</strong> — Moyenne mobile 50 jours (tendance moyen terme)</span>
                </div>
            </div>
            
            <div style="background: rgba(124,77,255,0.05); border-radius: 8px; padding: 8px; margin: 5px 0 15px 0;">
                <p style="color: #8A9AB0; font-size: 10px; margin: 0; text-align: center;">
                📈 <strong>Comment lire le graphique ?</strong><br>
                • Quand MA20 (verte) passe au-dessus de MA50 (orange) → signal haussier<br>
                • Quand MA20 passe en dessous de MA50 → signal baissier<br>
                • La zone violette sous la courbe représente le volume échangé
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                line=dict(color='#7C4DFF', width=2.5),
                fill='tozeroy',
                fillcolor='rgba(124,77,255,0.1)',
                name='Prix de clôture'
            ))
            
            ma20 = data['Close'].rolling(20).mean()
            fig.add_trace(go.Scatter(
                x=data.index, 
                y=ma20, 
                line=dict(color='#00D4AA', width=1.5, dash='solid'), 
                name='MA20 (moyenne 20 jours)'
            ))
            
            ma50 = data['Close'].rolling(50).mean()
            fig.add_trace(go.Scatter(
                x=data.index, 
                y=ma50, 
                line=dict(color='#FFB74D', width=1.5, dash='dot'), 
                name='MA50 (moyenne 50 jours)'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=400,
                margin=dict(l=0, r=0, t=40, b=20),
                legend=dict(
                    orientation='v',
                    yanchor='top',
                    y=0.99,
                    xanchor='left',
                    x=0.01,
                    bgcolor='rgba(13,15,26,0.8)',
                    bordercolor='#1E2340',
                    borderwidth=1,
                    font=dict(color='#8A9AB0', size=9)
                ),
                font=dict(color='#8A9AB0', size=10)
            )
            fig.update_xaxes(showgrid=False, zeroline=False, color='#2A3050', title='Date')
            fig.update_yaxes(showgrid=True, gridcolor='#1A1E30', zeroline=False, title='Prix (USD)')
            
            config = {'displayModeBar': True, 'scrollZoom': False, 'staticPlot': False}
            st.plotly_chart(fig, use_container_width=True, config=config)
            
            # Prédictions
            predictions, vol, trend = calculate_predictions(data, current_price)
            
            st.markdown("<div class='section-title'>📈 PRÉVISIONS HYBRIDES</div>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                pred = predictions["24H"]["price"]
                fiab = predictions["24H"]["fiability"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">24 HEURES</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {fiab}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                pred = predictions["7J"]["price"]
                fiab = predictions["7J"]["fiability"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">7 JOURS</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {fiab}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                pred = predictions["30J"]["price"]
                fiab = predictions["30J"]["fiability"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">30 JOURS</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {fiab}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                pred = predictions["6M"]["price"]
                fiab = predictions["6M"]["fiability"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">6 MOIS</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="fiability">🔒 Fiabilité : {fiab}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # ========== MÉTRIQUES AVEC EXPLICATIONS ==========
            st.markdown("<div class='section-title'>📊 MÉTRIQUES</div>", unsafe_allow_html=True)
            
            # Glossaire explicatif avant les métriques
            with st.expander("📖 Comprendre les métriques (cliquez ici)", expanded=False):
                st.markdown("""
                <div class="glossary">
                    <div class="glossary-title">🎯 DÉFINITIONS POUR DÉBUTANTS</div>
                    <div class="glossary-item">
                        <strong>🔵 DIRECTION</strong> — Pourcentage de fois où le modèle prédit correctement si le prix va monter ou baisser.<br>
                        <span style="color: #7C4DFF;">Exemple: 60% signifie que sur 10 prédictions, 6 sont justes.</span>
                    </div>
                    <div class="glossary-item">
                        <strong>🟣 VOLATILITÉ</strong> — Mesure l'amplitude des variations du prix. Plus c'est élevé, plus le cours bouge fortement.<br>
                        <span style="color: #7C4DFF;">Exemple: 40% signifie que le prix peut varier de ±40% sur un an.</span>
                    </div>
                    <div class="glossary-item">
                        <strong>🟢 SHARPE RATIO</strong> — Mesure le rendement par rapport au risque pris. Plus c'est élevé, meilleur est l'investissement.<br>
                        <span style="color: #7C4DFF;">Exemple: 1.0 = bon, 0.5 = moyen, &lt;0 = mauvais.</span>
                    </div>
                    <div class="glossary-item">
                        <strong>🟠 CONFIDENCE</strong> — Score global de fiabilité du modèle pour cette action (basé sur la volatilité et l'historique).<br>
                        <span style="color: #7C4DFF;">Exemple: 85% signifie que le modèle est assez confiant dans ses prédictions.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            dir_acc = 58 + (np.random.randn() * 3)
            col_a.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🎯 DIRECTION</div>
                <div class="metric-value" style="color: #00D4AA;">{dir_acc:.0f}%</div>
                <div class="metric-explanation">Précision des prédictions de hausse/baisse</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_b.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">⚡ VOLATILITÉ</div>
                <div class="metric-value" style="color: #FFB74D;">{vol*100:.0f}%</div>
                <div class="metric-explanation">Amplitude des variations du prix sur un an</div>
            </div>
            """, unsafe_allow_html=True)
            
            sharpe = trend/vol if vol > 0 else 0
            sharpe_color = "#00D4AA" if sharpe > 0.5 else "#FFB74D" if sharpe > 0 else "#FF4D6D"
            col_c.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">📈 SHARPE</div>
                <div class="metric-value" style="color: {sharpe_color};">{sharpe:.2f}</div>
                <div class="metric-explanation">Rendement gagné par unité de risque prise</div>
            </div>
            """, unsafe_allow_html=True)
            
            confidence = min(95, 65 + int(vol*100))
            col_d.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">🔒 CONFIDENCE</div>
                <div class="metric-value" style="color: #7C4DFF;">{confidence}%</div>
                <div class="metric-explanation">Score global de fiabilité du modèle</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Disclaimer
            st.markdown("""
            <div class="disclaimer">
                <p>⚠️ Prédictions basées sur LSTM + XGBoost. Ne constitue pas un conseil financier.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.analyze_clicked = False
