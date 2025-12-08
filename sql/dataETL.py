import pandas as pd
import os
import glob
import psycopg2
import io
import csv


joined_files = os.path.join("C:\RenewableEnergyAI\RenewableEnergyRevolution\data\countrywise", "*.csv")
joined_list = glob.glob(joined_files)
raw_data = pd.concat(map(pd.read_csv, joined_list), ignore_index=True)

raw_data.info()
