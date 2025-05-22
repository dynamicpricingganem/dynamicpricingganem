
import csv
import datetime
import requests
from bs4 import BeautifulSoup

def get_oxxo_price():
    # Simulated result from OXXO website scraping
    return 21.00  # Replace with real logic after request/parse

def get_7eleven_price():
    # Simulated result from 7-Eleven website scraping
    return 22.50  # Replace with real logic after request/parse

def scrape_prices():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = [
        [now, "Suerox - OXXO", get_oxxo_price()],
        [now, "Electrolit - 7-Eleven", get_7eleven_price()],
    ]
    return data

def append_to_csv(rows):
    path = "hydration_price_tracker/price_history.csv"
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

if __name__ == "__main__":
    rows = scrape_prices()
    append_to_csv(rows)
    print(f"✅ Appended {len(rows)} new price rows.")
