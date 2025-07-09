# Python Script for uploading data to the Azure SQL 

import os
from dotenv import load_dotenv
import pyodbc
import pandas as pd

server = os.getenv('AZURE_SQL_SERVER')
database = os.getenv('AZURE_SQL_DATABASE')
username = os.getenv('AZURE_SQL_USERNAME')
password = os.getenv('AZURE_SQL_PASSWORD')
driver = os.getenv('AZURE_SQL_DRIVER')
conn_str = os.getenv('CONNECTION_STRING')


conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


train_df = pd.read_csv('cleaned_train.csv')
test_df = pd.read_csv('cleaned_test.csv')


def create_table_from_df(df, table_name):
    cols = ", ".join(f"[{col}] NVARCHAR(MAX)" for col in df.columns)
    cursor.execute(f"IF OBJECT_ID('{table_name}', 'U') IS NOT NULL DROP TABLE {table_name}")
    cursor.execute(f"CREATE TABLE {table_name} ({cols})")
    conn.commit()

def insert_df_into_sql(df, table_name):
    # Replace problematic float values like NaN, inf, -inf
    df = df.replace([float('inf'), float('-inf')], None)
    df = df.where(pd.notnull(df), None)

    placeholders = ", ".join("?" for _ in df.columns)
    insert_query = f"INSERT INTO {table_name} VALUES ({placeholders})"

    for row in df.itertuples(index=False):
        try:
            cursor.execute(insert_query, *row)
        except Exception as e:
            print(f"❌ Failed to insert row {row}: {e}")
    conn.commit()


create_table_from_df(train_df, 'cleaned_train')
insert_df_into_sql(train_df, 'cleaned_train')

create_table_from_df(test_df, 'cleaned_test')
insert_df_into_sql(test_df, 'cleaned_test')

print("✅ Upload completed successfully!")

# Close connection
cursor.close()
conn.close()