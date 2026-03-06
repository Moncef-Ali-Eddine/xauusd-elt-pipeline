# ml/train_prophet.py — Prédiction XAU/USD avec Prophet

import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px
import os
import webbrowser

# ─────────────────────────────────────────
# 1. CHARGER LES DONNÉES
# ─────────────────────────────────────────
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/processed/xauusd_processed.csv", parse_dates=["date"])
    print(f"✅ {len(df)} lignes chargées")
    return df

# ─────────────────────────────────────────
# 2. PRÉPARER LES DONNÉES POUR PROPHET
# ─────────────────────────────────────────
def prepare_for_prophet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prophet exige exactement 2 colonnes :
    - ds : la date
    - y  : la valeur à prédire
    """
    df_prophet = df[["date", "close"]].copy()
    df_prophet.columns = ["ds", "y"]
    df_prophet = df_prophet.dropna()
    print(f"✅ Données préparées pour Prophet : {len(df_prophet)} lignes")
    return df_prophet

# ─────────────────────────────────────────
# 3. ENTRAÎNER LE MODÈLE
# ─────────────────────────────────────────
def train_model(df_prophet: pd.DataFrame) -> Prophet:
    print("\n🤖 Entraînement du modèle Prophet...")
    
    model = Prophet(
        daily_seasonality=False,   # Pas de saisonnalité journalière
        weekly_seasonality=True,   # Oui pour hebdomadaire
        yearly_seasonality=True,   # Oui pour annuelle
        changepoint_prior_scale=0.05  # Sensibilité aux changements de tendance
    )
    
    model.fit(df_prophet)
    print("✅ Modèle entraîné !")
    return model

# ─────────────────────────────────────────
# 4. FAIRE LES PRÉDICTIONS
# ─────────────────────────────────────────
def make_predictions(model: Prophet, days: int = 30) -> pd.DataFrame:
    print(f"\n🔮 Prédiction sur {days} jours...")
    
    # Créer les dates futures
    future = model.make_future_dataframe(periods=days)
    
    # Prédire
    forecast = model.predict(future)
    
    print(f"✅ Prédictions générées jusqu'au {forecast['ds'].max().date()}")
    return forecast

# ─────────────────────────────────────────
# 5. VISUALISER LES RÉSULTATS
# ─────────────────────────────────────────
def plot_forecast(df_prophet: pd.DataFrame, forecast: pd.DataFrame):
    """Graphique prix réel + prédiction"""
    
    fig = go.Figure()
    
    # Prix réels
    fig.add_trace(go.Scatter(
        x=df_prophet["ds"],
        y=df_prophet["y"],
        name="Prix Réel",
        line=dict(color="#FFD700", width=1.5)
    ))
    
    # Prédiction
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["yhat"],
        name="Prédiction",
        line=dict(color="#00BFFF", width=2, dash="dash")
    ))
    
    # Intervalle de confiance (zone d'incertitude)
    fig.add_trace(go.Scatter(
        x=pd.concat([forecast["ds"], forecast["ds"][::-1]]),
        y=pd.concat([forecast["yhat_upper"], forecast["yhat_lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(0, 191, 255, 0.1)",
        line=dict(color="rgba(255,255,255,0)"),
        name="Intervalle de confiance"
    ))
    
    fig.update_layout(
        title="XAU/USD — Prix Réel vs Prédiction (30 jours)",
        xaxis_title="Date",
        yaxis_title="Prix (USD)",
        template="plotly_dark",
        height=500
    )
    
    fig.write_html("data/processed/chart4_prediction.html")
    print("✅ Graphique prédiction créé !")

def plot_components(model: Prophet, forecast: pd.DataFrame):
    """Graphique des composantes du modèle"""
    
    # Tendance
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=forecast["ds"],
        y=forecast["trend"],
        name="Tendance",
        line=dict(color="#FF6347", width=2)
    ))
    
    fig.update_layout(
        title="XAU/USD — Tendance détectée par Prophet",
        xaxis_title="Date",
        yaxis_title="Prix (USD)",
        template="plotly_dark",
        height=400
    )
    
    fig.write_html("data/processed/chart5_trend.html")
    print("✅ Graphique tendance créé !")

# ─────────────────────────────────────────
# 6. AFFICHER LES PRÉDICTIONS EN CHIFFRES
# ─────────────────────────────────────────
def print_predictions(df_prophet: pd.DataFrame, forecast: pd.DataFrame):
    # Garder uniquement les 30 dernières lignes (futures)
    last_real_date = df_prophet["ds"].max()
    future_forecast = forecast[forecast["ds"] > last_real_date]
    
    print("\n🔮 PRÉDICTIONS XAU/USD — 30 prochains jours")
    print("=" * 55)
    print(f"{'Date':<15} {'Prédiction':>12} {'Min':>10} {'Max':>10}")
    print("-" * 55)
    
    for _, row in future_forecast.iterrows():
        print(f"{str(row['ds'].date()):<15} "
              f"${row['yhat']:>10.2f} "
              f"${row['yhat_lower']:>8.2f} "
              f"${row['yhat_upper']:>8.2f}")

# ─────────────────────────────────────────
# PIPELINE COMPLET
# ─────────────────────────────────────────
def run_ml():
    print("=" * 50)
    print("🚀 DÉMARRAGE ML — Prophet XAU/USD")
    print("=" * 50)
    
    df = load_data()
    df_prophet = prepare_for_prophet(df)
    model = train_model(df_prophet)
    forecast = make_predictions(model, days=30)
    
    print_predictions(df_prophet, forecast)
    plot_forecast(df_prophet, forecast)
    plot_components(model, forecast)
    
    # Ouvrir les graphiques
    webbrowser.open(os.path.abspath("data/processed/chart4_prediction.html"))
    webbrowser.open(os.path.abspath("data/processed/chart5_trend.html"))
    
    print("\n✅ ML TERMINÉ !")

if __name__ == "__main__":
    run_ml()