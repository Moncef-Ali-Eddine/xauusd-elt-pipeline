# analysis/eda.py — Analyse Exploratoire XAU/USD

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import os

def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/processed/xauusd_processed.csv", parse_dates=["date"])
    print(f"✅ {len(df)} lignes chargées")
    return df

def print_stats(df: pd.DataFrame):
    print("\n📊 STATISTIQUES XAU/USD")
    print("=" * 40)
    print(f"📅 Période        : {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"💰 Prix min       : ${df['close'].min():.2f}")
    print(f"💰 Prix max       : ${df['close'].max():.2f}")
    print(f"💰 Prix actuel    : ${df['close'].iloc[-1]:.2f}")
    print(f"📈 Jours haussiers: {df['is_bullish'].sum()} ({df['is_bullish'].mean()*100:.1f}%)")
    print(f"📉 Jours baissiers: {(df['is_bullish']==0).sum()} ({(1-df['is_bullish'].mean())*100:.1f}%)")
    print(f"📊 Volatilité moy : {df['daily_return'].std()*100:.2f}%")

def plot_price_with_ma(df: pd.DataFrame):
    """Graphique 1 — Prix + Moyennes Mobiles"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["date"], y=df["close"],
        name="Prix Close",
        line=dict(color="#FFD700", width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["ma_7"],
        name="MA 7 jours",
        line=dict(color="#00BFFF", width=1.5, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["ma_30"],
        name="MA 30 jours",
        line=dict(color="#FF6347", width=1.5, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["ma_90"],
        name="MA 90 jours",
        line=dict(color="#90EE90", width=2)
    ))

    fig.update_layout(
        title="XAU/USD — Prix & Moyennes Mobiles",
        xaxis_title="Date",
        yaxis_title="Prix (USD)",
        template="plotly_dark",
        height=500
    )

    fig.write_html("data/processed/chart1_moving_averages.html")
    print("✅ Graphique 1 créé : chart1_moving_averages.html")

def plot_candlestick(df: pd.DataFrame):
    """Graphique 2 — Chandelier 6 derniers mois"""
    df_recent = df.tail(180)

    fig = go.Figure(data=[go.Candlestick(
        x=df_recent["date"],
        open=df_recent["open"],
        high=df_recent["high"],
        low=df_recent["low"],
        close=df_recent["close"],
        name="XAU/USD"
    )])

    fig.update_layout(
        title="XAU/USD — Chandelier (6 derniers mois)",
        xaxis_title="Date",
        yaxis_title="Prix (USD)",
        template="plotly_dark",
        height=500
    )

    fig.write_html("data/processed/chart2_candlestick.html")
    print("✅ Graphique 2 créé : chart2_candlestick.html")

def plot_daily_returns(df: pd.DataFrame):
    """Graphique 3 — Distribution des variations journalières"""
    fig = px.histogram(
        df.dropna(subset=["daily_return"]),
        x="daily_return",
        nbins=80,
        title="Distribution des variations journalières",
        color_discrete_sequence=["#FFD700"],
        template="plotly_dark"
    )

    fig.update_layout(
        xaxis_title="Variation journalière (%)",
        yaxis_title="Nombre de jours",
        height=400
    )

    fig.write_html("data/processed/chart3_daily_returns.html")
    print("✅ Graphique 3 créé : chart3_daily_returns.html")

def run_eda():
    df = load_data()
    print_stats(df)
    plot_price_with_ma(df)
    plot_candlestick(df)
    plot_daily_returns(df)
    print("\n🚀 Ouverture des graphiques dans le navigateur...")
    import webbrowser, os
    webbrowser.open(os.path.abspath("data/processed/chart1_moving_averages.html"))
    webbrowser.open(os.path.abspath("data/processed/chart2_candlestick.html"))
    webbrowser.open(os.path.abspath("data/processed/chart3_daily_returns.html"))

if __name__ == "__main__":
    run_eda()