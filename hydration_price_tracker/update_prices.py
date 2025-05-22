import pandas as pd
from datetime import datetime
import os

# Simulate current scraped data (in production, replace this with actual scraping)
new_data = [
    {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Product": "Electrolit - Walmart", "Price": 21.00},
    {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Product": "Suerox - Chedraui", "Price": 15.25},
    {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Product": "FlashLyte - OXXO", "Price": 17.50},
]

new_df = pd.DataFrame(new_data)

file_path = "hydration_price_tracker/price_history.csv"

# Check if file exists
if os.path.exists(file_path):
    # Append without header
    new_df.to_csv(file_path, mode="a", header=False, index=False)
else:
    # Create new file with header
    new_df.to_csv(file_path, mode="w", header=True, index=False)

print("✅ Price data updated successfully.")
