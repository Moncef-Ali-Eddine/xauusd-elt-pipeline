# dashboard/app.py — Dashboard XAU/USD

import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import os

# ─────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────
def load_data():
    df = pd.read_csv("data/processed/xauusd_processed.csv", parse_dates=["date"])
    return df

def get_forecast(df, days=30):
    df_prophet = df[["date", "close"]].copy()
    df_prophet.columns = ["ds", "y"]
    df_prophet = df_prophet.dropna()
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05
    )
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    return forecast

# ─────────────────────────────────────────
# INITIALISATION
# ─────────────────────────────────────────
print("📊 Chargement des données...")
df = load_data()

print("🤖 Entraînement Prophet (30 secondes)...")
forecast = get_forecast(df, days=30)
print("✅ Prêt !")

last_price   = df["close"].iloc[-1]
prev_price   = df["close"].iloc[-2]
change_pct   = ((last_price - prev_price) / prev_price) * 100
price_min    = df["close"].min()
price_max    = df["close"].max()
next_30_pred = forecast[forecast["ds"] > df["date"].max()]["yhat"].iloc[-1]

# ─────────────────────────────────────────
# APPLICATION DASH
# ─────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container([

    # ── HEADER ──────────────────────────
    dbc.Row([
        dbc.Col([
            html.H1("🥇 XAU/USD Dashboard", 
                    className="text-warning fw-bold mt-3"),
            html.P("Pipeline ELT + Machine Learning — Gold Price Analysis | Created by ALI EDDINE MONCEF",
                   className="text-muted")
        ])
    ]),

    html.Hr(style={"borderColor": "#FFD700"}),

    # ── KPI CARDS ───────────────────────
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Prix Actuel", className="text-muted"),
                html.H3(f"${last_price:,.2f}", className="text-warning fw-bold"),
                html.P(f"{'▲' if change_pct > 0 else '▼'} {change_pct:+.2f}% vs hier",
                       className="text-success" if change_pct > 0 else "text-danger")
            ])
        ], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Prix Min (historique)", className="text-muted"),
                html.H3(f"${price_min:,.2f}", className="text-info fw-bold"),
                html.P("Depuis Janvier 2022", className="text-muted")
            ])
        ], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Prix Max (historique)", className="text-muted"),
                html.H3(f"${price_max:,.2f}", className="text-danger fw-bold"),
                html.P("Depuis Janvier 2022", className="text-muted")
            ])
        ], color="dark", outline=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H6("Prédiction dans 30j", className="text-muted"),
                html.H3(f"${next_30_pred:,.2f}", className="text-success fw-bold"),
                html.P(f"{'▲' if next_30_pred > last_price else '▼'} Prophet ML Model",
                       className="text-success" if next_30_pred > last_price else "text-danger")
            ])
        ], color="dark", outline=True), width=3),
    ], className="mb-4"),

    # ── SÉLECTEUR DE PÉRIODE ────────────
    dbc.Row([
        dbc.Col([
            html.Label("📅 Sélectionner la période :", className="text-dark"),
            dcc.Dropdown(
                id="period-selector",
                options=[
                    {"label": "3 derniers mois",  "value": 90},
                    {"label": "6 derniers mois",  "value": 180},
                    {"label": "1 an",             "value": 365},
                    {"label": "Tout",             "value": 9999},
                ],
                value=365,
                clearable=False,
                style={"backgroundColor": "#222", "color": "white"}
            )
        ], width=4)
    ], className="mb-3"),

    # ── GRAPHIQUE PRINCIPAL ──────────────
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📈 Prix & Moyennes Mobiles",
                               className="text-warning"),
                dbc.CardBody([
                    dcc.Graph(id="price-chart")
                ])
            ], color="dark", outline=True)
        ])
    ], className="mb-4"),

    # ── CHANDELIER + PRÉDICTION ──────────
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🕯️ Graphique Chandelier",
                               className="text-warning"),
                dbc.CardBody([dcc.Graph(id="candle-chart")])
            ], color="dark", outline=True)
        ], width=6),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("🔮 Prédiction Prophet (30 jours)",
                               className="text-warning"),
                dbc.CardBody([dcc.Graph(id="forecast-chart")])
            ], color="dark", outline=True)
        ], width=6),
    ], className="mb-4"),

    # ── DISTRIBUTION ────────────────────
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("📊 Distribution des variations journalières",
                               className="text-warning"),
                dbc.CardBody([dcc.Graph(id="returns-chart")])
            ], color="dark", outline=True)
        ])
    ], className="mb-4"),

    # ── FOOTER ──────────────────────────
    html.Hr(style={"borderColor": "#FFD700"}),
    html.P("🛠️ Stack : Python • yfinance • Snowflake • Prophet • Plotly Dash - Created by ALI EDDINE MONCEF",
           className="text-muted text-center mb-3")

], fluid=True, style={"backgroundColor": "#111", "minHeight": "100vh"})


# ─────────────────────────────────────────
# CALLBACKS — Interactivité
# ─────────────────────────────────────────

@app.callback(
    Output("price-chart", "figure"),
    Input("period-selector", "value")
)
def update_price_chart(days):
    df_filtered = df.tail(days) if days < 9999 else df

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["close"],
        name="Prix Close", line=dict(color="#FFD700", width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["ma_7"],
        name="MA 7j", line=dict(color="#00BFFF", width=1.5, dash="dot")
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["ma_30"],
        name="MA 30j", line=dict(color="#FF6347", width=1.5, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["ma_90"],
        name="MA 90j", line=dict(color="#90EE90", width=2)
    ))
    fig.update_layout(
        template="plotly_dark", height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=1.1)
    )
    return fig


@app.callback(
    Output("candle-chart", "figure"),
    Input("period-selector", "value")
)
def update_candle_chart(days):
    days_candle = min(days, 180)
    df_filtered = df.tail(days_candle)

    fig = go.Figure(data=[go.Candlestick(
        x=df_filtered["date"],
        open=df_filtered["open"],
        high=df_filtered["high"],
        low=df_filtered["low"],
        close=df_filtered["close"],
        name="XAU/USD"
    )])
    fig.update_layout(
        template="plotly_dark", height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_rangeslider_visible=False
    )
    return fig


@app.callback(
    Output("forecast-chart", "figure"),
    Input("period-selector", "value")
)
def update_forecast_chart(days):
    df_filtered   = df.tail(min(days, 365))
    last_real_date = df["date"].max()
    future_fc     = forecast[forecast["ds"] > last_real_date]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_filtered["date"], y=df_filtered["close"],
        name="Prix Réel", line=dict(color="#FFD700", width=1.5)
    ))
    fig.add_trace(go.Scatter(
        x=future_fc["ds"], y=future_fc["yhat"],
        name="Prédiction", line=dict(color="#00BFFF", width=2, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=pd.concat([future_fc["ds"], future_fc["ds"][::-1]]),
        y=pd.concat([future_fc["yhat_upper"], future_fc["yhat_lower"][::-1]]),
        fill="toself",
        fillcolor="rgba(0,191,255,0.15)",
        line=dict(color="rgba(0,0,0,0)"),
        name="Intervalle"
    ))
    fig.update_layout(
        template="plotly_dark", height=350,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    return fig


@app.callback(
    Output("returns-chart", "figure"),
    Input("period-selector", "value")
)
def update_returns_chart(days):
    df_filtered = df.tail(days) if days < 9999 else df

    fig = px.histogram(
        df_filtered.dropna(subset=["daily_return"]),
        x="daily_return", nbins=60,
        color_discrete_sequence=["#FFD700"],
        template="plotly_dark"
    )
    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Variation (%)",
        yaxis_title="Nombre de jours"
    )
    return fig


# ─────────────────────────────────────────
# LANCEMENT
# ─────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)