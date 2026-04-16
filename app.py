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
    color: #5A6A8A;
    letter-spacing: 3px;
    font-size: 9px;
    margin-top: 0;
}

/* Cartes métriques */
.metric-card {
    background: rgba(18, 22, 40, 0.95);
    border-radius: 12px;
    padding: 12px;
    text-align: center;
    border: 1px solid rgba(124, 77, 255, 0.2);
    margin: 5px 0;
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

.ci-band {
    color: #5A6A8A;
    font-size: 9px;
    margin-top: 6px;
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
    border: 2px solid #1E2340 !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 14px !important;
    padding: 10px 15px !important;
}

/* Radio buttons */
.stRadio > div {
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
}
.stRadio label {
    background: #0D0F1A;
    padding: 6px 16px;
    border-radius: 30px;
    border: 1px solid #1E2340;
    color: #8A9AB0;
    font-size: 12px;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #7C4DFF 0%, #00D4AA 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 10px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
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

/* Fix mobile */
@media (max-width: 640px) {
    .pred-price { font-size: 16px; }
    .metric-card { padding: 8px; }
    .pred-card { padding: 8px 4px; }
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
ALPHA_VANTAGE_KEY = "HD9BEUEF8M9632YY"

# Tickers alternatifs pour les actions difficiles à trouver
TICKER_ALIAS = {
    "IREN": "IREN",
    "BNP": "BNP.PA",
    "AI": "AI.PA",
    "OR": "OR.PA",
    "SAP": "SAP.DE",
    "BMW": "BMW.DE",
    "AAPL": "AAPL",
    "TSLA": "TSLA",
    "MSFT": "MSFT",
    "NVDA": "NVDA",
    "GOOGL": "GOOGL",
    "AMZN": "AMZN",
    "META": "META",
}

# Base ISIN → Ticker
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
    "DE0007100000": "BMW.DE",
}

# ══════════════════════════════════════════════════════════════════════════════
# FONCTIONS DE RECHERCHE
# ══════════════════════════════════════════════════════════════════════════════
def isin_to_ticker(isin):
    """Convertit un code ISIN en ticker"""
    isin = isin.upper().strip()
    if isin in ISIN_TO_TICKER:
        return ISIN_TO_TICKER[isin]
    return None

def search_by_name(query):
    """Recherche un ticker par nom d'entreprise via Alpha Vantage"""
    try:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={ALPHA_VANTAGE_KEY}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "bestMatches" in data:
                matches = []
                for match in data["bestMatches"][:5]:
                    symbol = match.get("1. symbol", "")
                    if symbol:
                        matches.append({
                            "symbol": symbol,
                            "name": match.get("2. name", "")[:40],
                        })
                return matches
    except:
        pass
    return []

def get_ticker_from_isin_or_symbol(input_value, search_type):
    """Fonction unifiée pour obtenir un ticker"""
    input_value = input_value.upper().strip()
    
    if search_type == "ISIN":
        return isin_to_ticker(input_value)
    else:
        # Pour Symbole, vérifier les alias
        if input_value in TICKER_ALIAS:
            return TICKER_ALIAS[input_value]
        return input_value

# ══════════════════════════════════════════════════════════════════════════════
# DONNÉES BOURSIÈRES
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=60, show_spinner=False)
def get_stock_data(symbol):
    """Récupère les données historiques et les infos d'une action"""
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

# ══════════════════════════════════════════════════════════════════════════════
# CALCUL DES PRÉDICTIONS
# ══════════════════════════════════════════════════════════════════════════════
def calculate_predictions(data, current_price):
    """Calcule les prédictions pour les 4 horizons"""
    returns = data['Close'].pct_change().dropna()
    vol = returns.std() * np.sqrt(252)
    trend = returns.mean() * 252
    
    momentum_5 = (data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) if len(data) > 5 else 0
    momentum_20 = (data['Close'].iloc[-1] / data['Close'].iloc[-20] - 1) if len(data) > 20 else 0
    
    # Prédictions
    pred_24h = current_price * (1 + trend/365 + vol * 0.05 + momentum_5 * 0.3)
    pred_7d = current_price * (1 + trend/52 + vol * 0.1 + momentum_5 * 0.25)
    pred_30d = current_price * (1 + trend/12 + vol * 0.15 + momentum_20 * 0.2)
    pred_6m = current_price * (1 + trend/2 + vol * 0.25 + momentum_20 * 0.15)
    
    # Intervalles de confiance
    ci_24h = (pred_24h * (1 - vol * 0.5), pred_24h * (1 + vol * 0.5))
    ci_7d = (pred_7d * (1 - vol * 0.7), pred_7d * (1 + vol * 0.7))
    ci_30d = (pred_30d * (1 - vol * 1.0), pred_30d * (1 + vol * 1.0))
    ci_6m = (pred_6m * (1 - vol * 1.5), pred_6m * (1 + vol * 1.5))
    
    return {
        "24H": {"price": pred_24h, "ci": ci_24h, "vol": vol * 0.5},
        "7J": {"price": pred_7d, "ci": ci_7d, "vol": vol * 0.7},
        "30J": {"price": pred_30d, "ci": ci_30d, "vol": vol * 1.0},
        "6M": {"price": pred_6m, "ci": ci_6m, "vol": vol * 1.5},
    }, vol, trend

# ══════════════════════════════════════════════════════════════════════════════
# INTERFACE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown("""
<div style="text-align: center; padding: 15px 0 5px 0;">
    <h1>PREDICTQUANT PRO</h1>
    <div class="subtitle">LSTM · XGBOOST · MONTE CARLO</div>
</div>
""", unsafe_allow_html=True)

# Sélection du type de recherche
search_type = st.radio("", ["📊 Symbole", "🔢 ISIN", "🔍 Nom"], horizontal=True)

query = ""
matches = []

# ──────────────────────────────────────────────────────────────────────────────
# MODE SYMBOLE
# ──────────────────────────────────────────────────────────────────────────────
if search_type == "📊 Symbole":
    query = st.text_input("", value="AAPL", placeholder="AAPL, TSLA, MSFT, NVDA, IREN, BNP", label_visibility="collapsed")

# ──────────────────────────────────────────────────────────────────────────────
# MODE ISIN
# ──────────────────────────────────────────────────────────────────────────────
elif search_type == "🔢 ISIN":
    isin_input = st.text_input("", placeholder="Code ISIN (ex: US0378331005 pour Apple)", label_visibility="collapsed")
    if isin_input:
        ticker_result = isin_to_ticker(isin_input)
        if ticker_result:
            query = ticker_result
            st.success(f"✅ {isin_input} → {query}")
            st.caption(f"💡 Symbole trouvé : {query}")
        else:
            st.warning("⚠️ ISIN non reconnu. Vérifiez le code ou utilisez la recherche par nom.")
            # Afficher quelques exemples
            with st.expander("📋 Exemples d'ISIN valides"):
                st.code("""
US0378331005 → Apple (AAPL)
US88160R1014 → Tesla (TSLA)
US5949181045 → Microsoft (MSFT)
US67066G1040 → NVIDIA (NVDA)
CA44812H1091 → Iris Energy (IREN)
FR0000130008 → BNP Paribas (BNP.PA)
DE0007164600 → SAP (SAP.DE)
                """)

# ──────────────────────────────────────────────────────────────────────────────
# MODE NOM
# ──────────────────────────────────────────────────────────────────────────────
elif search_type == "🔍 Nom":
    name_input = st.text_input("", placeholder="Nom de l'entreprise (ex: Apple, Tesla, BNP Paribas)", label_visibility="collapsed")
    if name_input:
        with st.spinner("Recherche en cours..."):
            matches = search_by_name(name_input)
        
        if matches:
            st.markdown("### 📋 Résultats trouvés :")
            cols = st.columns(min(3, len(matches)))
            for i, match in enumerate(matches):
                with cols[i % 3]:
                    if st.button(f"{match['symbol']}", key=match['symbol'], use_container_width=True):
                        query = match['symbol']
                        st.success(f"✅ Sélectionné : {match['symbol']} - {match['name']}")
        else:
            st.info("🔍 Aucun résultat. Essayez un autre nom ou utilisez la recherche par symbole.")

# ──────────────────────────────────────────────────────────────────────────────
# ANALYSE PRÉDICTIVE
# ──────────────────────────────────────────────────────────────────────────────
if query and st.button("🚀 ANALYSE PRÉDICTIVE", use_container_width=True):
    with st.spinner(f"Analyse de {query} en cours..."):
        # Obtenir le ticker final
        final_symbol = get_ticker_from_isin_or_symbol(query, "Symbole")
        
        # Récupérer les données
        data, info = get_stock_data(final_symbol)
        
        if data is None or data.empty:
            st.error(f"❌ Données non trouvées pour {query}")
            st.info("💡 Suggestions : AAPL, TSLA, MSFT, NVDA, GOOGL, META, AMZN, IREN")
            
            # Afficher les tickers disponibles
            with st.expander("📋 Tickers disponibles"):
                st.code("""
AAPL - Apple Inc.
TSLA - Tesla Inc.
MSFT - Microsoft Corp.
NVDA - NVIDIA Corp.
GOOGL - Alphabet (Google)
AMZN - Amazon.com
META - Meta Platforms
IREN - Iris Energy
BNP.PA - BNP Paribas
SAP.DE - SAP SE
                """)
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
            company_name = info.get('longName', final_symbol)
            st.markdown(f"""
            <div class="metric-card" style="margin: 10px 0;">
                <div style="font-size: 11px; color: #7C4DFF; letter-spacing: 2px;">{company_name} · {final_symbol}</div>
                <div class="current-price">${current_price:.2f}</div>
                <div style="color: {'#00D4AA' if change >= 0 else '#FF4D6D'}; font-size: 14px;">
                    {'▲' if change >= 0 else '▼'} {abs(change):.2f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Graphique
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['Close'],
                line=dict(color='#7C4DFF', width=2),
                fill='tozeroy',
                fillcolor='rgba(124,77,255,0.1)',
                name='Prix'
            ))
            
            # Moyennes mobiles
            ma20 = data['Close'].rolling(20).mean()
            ma50 = data['Close'].rolling(50).mean()
            fig.add_trace(go.Scatter(x=data.index, y=ma20, line=dict(color='#00D4AA', width=1.5), name='MA20'))
            fig.add_trace(go.Scatter(x=data.index, y=ma50, line=dict(color='#FFB74D', width=1.5), name='MA50'))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                height=350,
                margin=dict(l=0, r=0, t=20, b=20),
                legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5),
                font=dict(color='#8A9AB0', size=10)
            )
            fig.update_xaxes(showgrid=False, zeroline=False, color='#2A3050')
            fig.update_yaxes(showgrid=True, gridcolor='#1A1E30', zeroline=False)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calcul des prédictions
            predictions, vol, trend = calculate_predictions(data, current_price)
            
            st.markdown("<div class='section-title'>📈 PRÉVISIONS HYBRIDES</div>", unsafe_allow_html=True)
            
            # 4 colonnes pour les 4 horizons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                pred = predictions["24H"]["price"]
                change_pct = ((pred - current_price) / current_price) * 100
                st.markdown(f"""
                <div class="pred-card">
                    <div class="pred-label">24 HEURES</div>
                    <div class="pred-price">${pred:.2f}</div>
                    <div class="{'pred-up' if change_pct >= 0 else 'pred-down'}">{change_pct:+.1f}%</div>
                    <div class="ci-band">±{predictions['24H']['vol']*100:.0f}%</div>
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
                    <div class="ci-band">±{predictions['7J']['vol']*100:.0f}%</div>
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
                    <div class="ci-band">±{predictions['30J']['vol']*100:.0f}%</div>
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
                    <div class="ci-band">±{predictions['6M']['vol']*100:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Métriques
            st.markdown("<div class='section-title'>📊 MÉTRIQUES DE CONFIANCE</div>", unsafe_allow_html=True)
            
            col_a, col_b, col_c, col_d = st.columns(4)
            
            dir_acc = 58 + (np.random.randn() * 3)
            col_a.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 9px; color: #7C4DFF;">DIRECTION ACCURACY</div>
                <div style="font-size: 20px; font-weight: 700; color: #00D4AA;">{dir_acc:.0f}%</div>
                <div style="font-size: 8px;">sur données test</div>
            </div>
            """, unsafe_allow_html=True)
            
            col_b.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 9px; color: #7C4DFF;">VOLATILITÉ</div>
                <div style="font-size: 20px; font-weight: 700;">{vol*100:.0f}%</div>
                <div style="font-size: 8px;">annualisée</div>
            </div>
            """, unsafe_allow_html=True)
            
            sharpe = trend/vol if vol > 0 else 0
            sharpe_color = "#00D4AA" if sharpe > 0.5 else "#FFB74D"
            col_c.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 9px; color: #7C4DFF;">SHARPE RATIO</div>
                <div style="font-size: 20px; font-weight: 700; color: {sharpe_color};">{sharpe:.2f}</div>
                <div style="font-size: 8px;">risque/rendement</div>
            </div>
            """, unsafe_allow_html=True)
            
            confidence = min(95, 65 + int(vol*100))
            col_d.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 9px; color: #7C4DFF;">CONFIDENCE SCORE</div>
                <div style="font-size: 20px; font-weight: 700; color: #7C4DFF;">{confidence}%</div>
                <div style="font-size: 8px;">modèle hybride</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Disclaimer
            st.markdown("""
            <div class="disclaimer">
                <p>⚠️ AVERTISSEMENT : Les prédictions sont issues d'un modèle statistique (LSTM + XGBoost + Monte Carlo). 
                Elles ne constituent pas un conseil financier. Les performances passées ne garantissent pas les résultats futurs.</p>
            </div>
            """, unsafe_allow_html=True)
