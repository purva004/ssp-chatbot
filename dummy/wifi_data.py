import pandas as pd

# Step 1: Load the CSV file
df = pd.read_csv("wifi_data.csv")

# Step 2: Ensure WiFiCount is numeric
df["WiFiCount"] = pd.to_numeric(df["WiFiCount"], errors='coerce')

# Step 3: Drop missing values
df = df.dropna(subset=["WiFiCount"])

# Step 4: Apply sliding window average using .rolling()
df["SlidingAvg_WiFiCount_3"] = df["WiFiCount"].rolling(window=3).mean()

# Step 5: Save to new file
df.to_csv("wifi_data_sliding_avg.csv", index=False)

# Step 6: Show preview
print(df[["WiFiCount", "SlidingAvg_WiFiCount_3"]].head(10))
