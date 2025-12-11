import pandas as pd
import os
import glob
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables (e.g., GOOGLE_API_KEY)
load_dotenv()


joined_files = os.path.join("C:\RenewableEnergyAI\RenewableEnergyRevolution\data\World_Production", "*.csv")
joined_list_worldprod = glob.glob(joined_files)

    # Using a list comprehension
list_of_dfs = [pd.read_csv(filename) for filename in joined_list_worldprod]
combined_df = pd.concat(list_of_dfs, ignore_index=True)

# data = pd.DataFrame(combined_df)

# print(combined_df.head())
# print(combined_df.info())
# print(combined_df.describe())
# print(data.shape)
# print(len(data))

# --- Database Connection Details ---
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"


# --- Connect to PostgreSQL and Read Sample Data ---
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
conn_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db_engine = create_engine(conn_string)

# --- Import DataFrame into PostgreSQL ---
try:    
    print(f"Please Truncate table before running twice.")
    combined_df.to_sql('worldproduction', db_engine, if_exists='append', index=False)
    print(f"Successfully imported data from CSVs into '{'worldproduction'}' table.")
    select_query = f"SELECT * from worldproduction WHERE Country = 'India' LIMIT 5;"
    df= pd.read_sql(select_query, db_engine)
    print(df.head())
except Exception as e:
    print(f"Error importing Energy Production data: {e}")

# Optional: Close the connection
db_engine.dispose()
conn.close()