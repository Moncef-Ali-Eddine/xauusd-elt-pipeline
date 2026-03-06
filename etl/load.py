# etl/load.py — Chargement des données vers Snowflake

import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

# Charger les variables du fichier .env
load_dotenv()

def get_connection():
    """Crée et retourne une connexion Snowflake"""
    conn = snowflake.connector.connect(
        account   = os.getenv("SNOWFLAKE_ACCOUNT"),
        user      = os.getenv("SNOWFLAKE_USER"),
        password  = os.getenv("SNOWFLAKE_PASSWORD"),
        database  = os.getenv("SNOWFLAKE_DATABASE"),
        schema    = os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    )
    return conn

def test_connection():
    """Teste simplement la connexion à Snowflake"""
    print("🔌 Connexion à Snowflake...")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT CURRENT_VERSION()")
    version = cursor.fetchone()
    
    print(f"✅ Connecté ! Snowflake version : {version[0]}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    test_connection()