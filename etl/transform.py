# etl/transform.py — Transformation des données XAU/USD

import pandas as pd
import os
from glob import glob

def load_raw_data() -> pd.DataFrame:
    """Charge le CSV brut depuis data/raw/"""
    
    # Trouver le fichier CSV le plus récent
    files = glob("data/raw/xauusd_raw_*.csv")
    
    if not files:
        raise FileNotFoundError("❌ Aucun fichier raw trouvé !")
    
    latest_file = max(files)
    print(f"📂 Chargement : {latest_file}")
    
    df = pd.read_csv(latest_file, parse_dates=["date"])
    print(f"✅ {len(df)} lignes chargées")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie les données brutes"""
    print("\n🧹 Nettoyage des données...")
    
    before = len(df)
    
    # Supprimer les doublons
    df = df.drop_duplicates(subset=["date"])
    
    # Supprimer les lignes avec valeurs manquantes
    df = df.dropna(subset=["open", "high", "low", "close"])
    
    # Trier par date
    df = df.sort_values("date").reset_index(drop=True)
    
    after = len(df)
    print(f"✅ Nettoyage terminé : {before - after} lignes supprimées")
    return df


def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les indicateurs techniques"""
    print("\n📊 Calcul des indicateurs techniques...")
    
    # ── Moyennes Mobiles ─────────────────────
    df["ma_7"]  = df["close"].rolling(window=7).mean().round(2)
    df["ma_30"] = df["close"].rolling(window=30).mean().round(2)
    df["ma_90"] = df["close"].rolling(window=90).mean().round(2)
    
    # ── Variation journalière ────────────────
    # % de changement par rapport au jour précédent
    df["daily_return"] = df["close"].pct_change().round(4)
    
    # ── Amplitude de la journée ──────────────
    df["high_low_range"] = (df["high"] - df["low"]).round(2)
    
    # ── Variation Close/Open ─────────────────
    df["close_open_diff"] = (df["close"] - df["open"]).round(2)
    
    # ── Tendance : hausse ou baisse ? ────────
    # 1 = prix en hausse, 0 = prix en baisse
    df["is_bullish"] = (df["close"] > df["open"]).astype(int)
    
    print("✅ Indicateurs ajoutés : ma_7, ma_30, ma_90, daily_return, high_low_range, is_bullish")
    return df


def save_processed_data(df: pd.DataFrame) -> str:
    """Sauvegarde les données transformées dans data/processed/"""
    
    os.makedirs("data/processed", exist_ok=True)
    filepath = "data/processed/xauusd_processed.csv"
    df.to_csv(filepath, index=False)
    
    print(f"\n💾 Sauvegardé : {filepath}")
    return filepath


def run_transform() -> pd.DataFrame:
    """Pipeline de transformation complet"""
    print("=" * 50)
    print("🚀 DÉMARRAGE TRANSFORMATION XAU/USD")
    print("=" * 50)
    
    # 1. Charger
    df = load_raw_data()
    
    # 2. Nettoyer
    df = clean_data(df)
    
    # 3. Enrichir
    df = add_technical_indicators(df)
    
    # 4. Sauvegarder
    save_processed_data(df)
    
    print("\n📋 Aperçu final :")
    print(df[["date", "close", "ma_7", "ma_30", "daily_return", "is_bullish"]].tail(10).to_string())
    
    print(f"\n✅ TRANSFORMATION TERMINÉE")
    print(f"   Lignes : {len(df)}")
    print(f"   Colonnes : {list(df.columns)}")
    
    return df


if __name__ == "__main__":
    run_transform()