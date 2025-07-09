# python script to  fetch_data_from_ azure sql

import os
import pandas as pd
import pyodbc
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

def get_connection():
    conn_str = f"""
        DRIVER={os.getenv('AZURE_SQL_DRIVER')};
        SERVER={os.getenv('AZURE_SQL_SERVER')};
        DATABASE={os.getenv('AZURE_SQL_DATABASE')};
        UID={os.getenv('AZURE_SQL_USERNAME')};
        PWD={os.getenv('AZURE_SQL_PASSWORD')};
        Encrypt=yes;
        TrustServerCertificate=no;
        Connection Timeout=30;
    """
    return pyodbc.connect(conn_str)

def fetch_table_as_df(table_name):
    try:
        conn = get_connection()
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error fetching {table_name}:", e)
        return pd.DataFrame()

# --- FETCH TRAIN AND TEST ---
train_df = fetch_table_as_df("cleaned_train")
test_df = fetch_table_as_df("cleaned_test")

# --- TEMP CHECK ---
print("Train Data:")
print(train_df.head())
print("\nTest Data:")
print(test_df.head())
