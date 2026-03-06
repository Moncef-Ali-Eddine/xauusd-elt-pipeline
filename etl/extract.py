# etl/extract.py — Extraction des données XAU/USD

import yfinance as yf
import pandas as pd
from datetime import datetime
import os

# ── Paramètres ──────────────────────────
SYMBOL     = "GC=F"        # Symbole Yahoo Finance pour l'or (Gold Futures)
START_DATE = "2022-01-01"
END_DATE   = datetime.today().strftime('%Y-%m-%d')

# ── Extraction ──────────────────────────
def extract():
    print(f"📥 Téléchargement XAU/USD | {START_DATE} → {END_DATE}")

    df = yf.download(SYMBOL, start=START_DATE, end=END_DATE)

    if df.empty:
        print("❌ Aucune donnée reçue !")
        return

    # Remettre 'Date' comme colonne normale
    df = df.reset_index()

    # Garder uniquement les colonnes utiles
    df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]

    # Renommer en minuscules (bonne pratique)
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    # Ajouter une colonne source
    df["symbol"] = "XAU/USD"

    # Sauvegarder en CSV
    os.makedirs("data/raw", exist_ok=True)
    filename = f"data/raw/xauusd_raw_{datetime.today().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)

    print(f"✅ {len(df)} lignes extraites")
    print(f"💾 Sauvegardé : {filename}")
    print(f"📅 Période : {df['date'].min()} → {df['date'].max()}")
    print("\n🔍 Aperçu :")
    print(df.head())

    return df

# ── Point d'entrée ───────────────────────
if __name__ == "__main__":
    extract()