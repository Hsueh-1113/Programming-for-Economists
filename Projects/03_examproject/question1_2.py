import pandas as pd
import numpy as np
import requests
from io import StringIO
from dstapi import DstApi
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# connect to Statistics Denmark API
api = DstApi("PRIS113")

# inspect table structure 
api.tablesummary(language='en')

# 2. Download CPI (PRIS113)

cpi_vars = {
    'table': 'PRIS113',
    'format': 'BULK', 
    'lang': 'en',
    'variables': [
        {'code': 'TYPE', 'values': ["INDEKS"]}, # all Denmark
        {'code': 'Tid', 'values': ['*']}, # '*' is everything
        ]
    }
# API request
url = "https://api.statbank.dk/v1/data"
response = requests.post(url, json=cpi_vars)
response.raise_for_status()

# load data into DataFrame
df = pd.read_csv(StringIO(response.text), sep=";")
df.columns = ["type", "time", "cpi"]

df["cpi"] = pd.to_numeric(df["cpi"], errors="coerce")
cpi = df[["time", "cpi"]].copy()
# Convert monthly string to timestamp
cpi["month"] = pd.to_datetime(cpi["time"], format="%YM%m")

# Convert to quarter
cpi["quarter"] = cpi["month"].dt.to_period("Q")

# Quarterly CPI = mean of months
cpi_q = (
    cpi.groupby("quarter")["cpi"]
       .mean()
       .to_frame()
)

from question1_1 import prices
# Merge CPI into house price panel
real_prices = prices.merge(
    cpi_q,
    left_index=True,
    right_index=True,
    how="inner"
)

# real index = nominal index / CPI × 100
for province in prices.columns:
    real_prices[province] = (
        real_prices[province] / real_prices["cpi"] * 100
    )
from question1_1 import base_period
real_prices = real_prices[prices.columns]
real_indexed = real_prices / real_prices.loc[base_period] * 100
real_indexed = real_indexed.loc[base_period:]

real_indexed.index = real_indexed.index.to_timestamp()

# Plot
plt.figure(figsize=(12,6))

for p in real_indexed.columns:
    plt.plot(real_indexed.index, real_indexed[p], label=p)

plt.title("Real House Prices Across Danish Provinces from 1992 Q1 to 2025 Q3")
plt.xlabel("Year")
plt.ylabel("Real house price index")
plt.legend(fontsize=8)
plt.tight_layout()
plt.show()
