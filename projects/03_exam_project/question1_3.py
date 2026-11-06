import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the Excel file
BM010_houses = pd.read_excel("BM010_houses.xlsx")
BM010_houses.head()
pd.read_excel("BM010_houses.xlsx").iloc[:5,:137] # 5 rows, 137 columns
# Clean the data
Houses = pd.read_excel("BM010_houses.xlsx",skiprows=2) 
Houses.iloc[:5,:137]
drop_cols = [f'Unnamed: {num}' for num in range(2)] # use list comprehension to create list of columns
print(f'{drop_cols = }')
House_Price = Houses.drop(columns=drop_cols)
House_Price.iloc[:3,:135]
House_Price = House_Price.rename(columns={'Unnamed: 2':'municipality'})
House_Price.iloc[:5,:5]
col_dict = {str(i): f'Price_per_meter_square{i}' for i in House_Price.columns[1:]}
House_Price = House_Price.rename(columns=col_dict)
House_Price.head(5).iloc[:,0:5]
# Sort by municipality name
House_Price = House_Price.sort_values('municipality').reset_index(drop=True) # drop=True to avoid adding old index as a column
House_Price.iloc[:5,:5]
#drop municipalities with missing observations
House_Price = House_Price.dropna()
# Convert price columns to numeric
price_cols = House_Price.columns[1:]  # exclude municipality
House_Price[price_cols] = House_Price[price_cols].apply(pd.to_numeric, errors="coerce")
# Calculate initial price and total growth
initial_price = House_Price[price_cols[0]]
final_price = House_Price[price_cols[-1]]

total_growth = final_price - initial_price
# Create summary DataFrame
summary = pd.DataFrame({
    "municipality": House_Price["municipality"],
    "initial_price": initial_price,
    "total_growth": total_growth
})
# Calculate correlation
correlation = summary["initial_price"].corr(summary["total_growth"])
print("Correlation:", correlation)
# Scatter plot
top_growth = summary.nlargest(5, "total_growth")
top_initial = summary.nlargest(5, "initial_price")

label_municipalities = pd.concat(
    [top_growth, top_initial]
)["municipality"].unique()

plt.scatter(
    summary["initial_price"],
    summary["total_growth"],
    alpha=0.7
)

for muni in label_municipalities:
    row = summary[summary["municipality"] == muni].iloc[0]
    plt.text(
        row["initial_price"],
        row["total_growth"],
        muni,
        fontsize=9,
        ha="right",
        va="bottom"
    )

plt.xlabel("Initial house price per m²")
plt.ylabel("Total house price growth")
plt.title("House Price Growth vs Initial Price")
plt.grid(True)
plt.tight_layout()
plt.show()
