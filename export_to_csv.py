import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///weather.db')

df_locations = pd.read_sql("SELECT * FROM locations", engine)
df_locations.to_csv("exports/locations.csv", index=False)

df_forecasts = pd.read_sql("SELECT * FROM forecasts", engine)
df_forecasts.to_csv("exports/forecasts.csv", index=False)

print(" CSV files saved to 'exports/' folder.")
