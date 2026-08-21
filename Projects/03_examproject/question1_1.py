import pandas as pd
import numpy as np
import requests
from io import StringIO
from dstapi import DstApi
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# connect to Statistics Denmark API
api = DstApi("EJ56")

# inspect table structure 
api.tablesummary(language='en')
api.variable_levels('OMRÅDE',language='en')
api.variable_levels('EJENDOMSKATE',language='en')
api.variable_levels('TAL',language='en')
api.variable_levels('Tid',language='en')

# set download parameters
nominal_vars = {
    'table': 'EJ56',
    'format': 'BULK', 
    'lang': 'en',
    'variables': [
        {'code': 'OMRÅDE', 'values': ["01","02","03","04","05","06","07","08","09","10","11"]}, # all provinces
        {'code': 'EJENDOMSKATE', 'values': ['0111']},# the standard housing market measure 
        {'code': 'TAL', 'values': ['100']}, # index level
        {'code': 'Tid', 'values': ['*']}, # '*' is everything
        ]
    }
# API request
url = "https://api.statbank.dk/v1/data"
response = requests.post(url, json=nominal_vars)
response.raise_for_status()
# load data into DataFrame
df = pd.read_csv(StringIO(response.text), sep=";")
df.columns = ["province", "housing_type", "measure", "quarter", "house_price_index"]

df["house_price_index"] = pd.to_numeric(df["house_price_index"], errors="coerce")

# Quarter handling 
df["quarter"] = (
    df["quarter"]
    .astype(str)
    .str.replace("K", "Q", regex=False)
)

df["quarter"] = pd.PeriodIndex(df["quarter"], freq="Q")

# Drop provinces with missing observations
valid = (
    df.groupby("province")["house_price_index"]
      .apply(lambda x: x.notna().all())
)

df = df[df["province"].isin(valid[valid].index)]

# Pivot
prices = (
    df.pivot(index="quarter", columns="province", values="house_price_index")
      .sort_index()
)

# Index to 100 in 1992 Q1
base_period = pd.Period("1992Q1", freq="Q")

prices_indexed = prices / prices.loc[base_period] * 100
prices_indexed = prices_indexed.loc[base_period:]

# Convert to timestamps for plotting
prices_indexed.index = prices_indexed.index.to_timestamp()

# Plot
plt.figure(figsize=(12,6))

for p in prices_indexed.columns:
    plt.plot(prices_indexed.index, prices_indexed[p], label=p)

plt.title("House Prices Across Danish Provinces (from base year 1992 Q1 til 2025 Q3)")
plt.xlabel("Year")
plt.ylabel("Index")
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()

# Ranking

ranking = (prices_indexed.iloc[-1] - 100).sort_values(ascending=False)
print("Ranking of provinces by total house price growth:")
print(ranking)