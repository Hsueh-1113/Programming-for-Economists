import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from question1_3 import House_Price
HP_long = House_Price.copy()

HP_long = HP_long.melt(
    id_vars="municipality",
    var_name="quarter",
    value_name="price"
)

HP_long = HP_long.sort_values(
    ["municipality", "quarter"]
).reset_index(drop=True)

HP_long["price_roll4"] = (
    HP_long
        .groupby("municipality")["price"]
        .transform(lambda x: x.rolling(4).mean())
)
HP_long["year"] = HP_long["quarter"].str.extract(r"(\d{4})").astype(int)
# Identify pre-crisis peak
pre_crisis = HP_long[HP_long["year"] < 2008]

pre_crisis_peak = (
    pre_crisis
        .groupby("municipality")["price_roll4"]
        .max()
)
# Latest value
latest_value = (
    HP_long
        .groupby("municipality")["price_roll4"]
        .last()
)
# Calculate change from peak

change_from_peak = latest_value - pre_crisis_peak
results = pd.DataFrame({
    "pre_2008_peak": pre_crisis_peak,
    "latest_value": latest_value,
    "change_from_peak": change_from_peak
})
# Drop NaN values
below_peak = results[results["change_from_peak"] < 0]
below_peak
# Plot change from peak
plt.figure(figsize=(6,25))
results["change_from_peak"].sort_values().plot(
    kind="barh",
    color="green"
)
# Plot the bar chart
plt.axvline(0, color="black", linewidth=1)
plt.xlabel("Change in 4-quarter rolling average house price (DKK per m²)")
plt.title("Change from Pre-2008 Peak to Latest Observation")
plt.tight_layout()
plt.show()