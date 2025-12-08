import pandas as pd
import os
import glob
import psycopg2
from sqlalchemy import create_engine
import io
import csv


joined_files = os.path.join("C:\RenewableEnergyAI\RenewableEnergyRevolution\data\countrywise", "*.csv")
joined_list = glob.glob(joined_files)

    # Using a list comprehension
list_of_dfs = [pd.read_csv(filename) for filename in joined_list]
combined_df = pd.concat(list_of_dfs, ignore_index=True)

# data = pd.DataFrame(combined_df)

# print(combined_df.head())
# print(combined_df.info())
# print(combined_df.describe())
# print(data.shape)
# print(len(data))

# --- Database Connection Details ---
DB_NAME = "energy"
DB_USER = "postgres"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_PORT = "5432"

# --- Data Transformation / ETL ---
col_interested = ['country','iso_code','year', \
                  'biofuel_consumption',\
                  'coal_consumption',\
                  'coal_production',\
                  'electricity_demand',\
                  'biofuel_electricity',\
                  'coal_electricity',\
                  'fossil_electricity',\
                  'gas_electricity',\
                  'hydro_electricity',\
                  'nuclear_electricity',\
                  'oil_electricity',\
                  'other_renewable_exc_biofuel_electricity',\
                  'other_renewable_electricity',\
                  'renewables_electricity',\
                  'solar_electricity',\
                  'wind_electricity',\
                  'electricity_generation',\
                  'fossil_fuel_consumption',\
                  'gas_consumption',\
                  'gas_production',\
                  'hydro_consumption',\
                  'low_carbon_consumption',\
                  'nuclear_consumption',\
                  'oil_consumption',\
                  'oil_production',\
                  'other_renewables_cons_change_pct',\
                  'other_renewables_share_energy',\
                  'other_renewables_cons_change_twh',\
                  'other_renewable_consumption',\
                  'other_renewables_share_elec',\
                  'primary_energy_consumption',\
                  'renewables_share_elec',\
                  'renewables_share_energy',\
                  'renewables_consumption',\
                  'solar_share_elec',\
                  'solar_share_energy',\
                  'solar_consumption',\
                  'wind_share_elec',\
                  'wind_share_energy',\
                  'wind_consumption',]

renew_data = combined_df[col_interested]

# print(renew_data.head())
# print(renew_data.shape)


# --- Connect to PostgreSQL and Read Sample Data ---
conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
conn_string = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
db_engine = create_engine(conn_string)

# --- Import DataFrame into PostgreSQL ---
try:    
    print(f"Please Truncate table before running twice.")
    renew_data.to_sql('allcountryenergy', db_engine, if_exists='append', index=False)
    print(f"Successfully imported data from CSVs into '{'allcountryenergy'}' table.")
    select_query = f"SELECT * from allcountryenergy WHERE country = 'India' LIMIT 5;"
    df= pd.read_sql(select_query, db_engine)
    print(df.head())
except Exception as e:
    print(f"Error importing data: {e}")

# Optional: Close the connection
db_engine.dispose()
conn.close()