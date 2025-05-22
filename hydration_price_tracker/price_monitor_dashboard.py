
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Hydration Price Tracker", layout="wide")
st.image('hydration_price_tracker/ganem_logo.png', width=200)
st.title("💧 Hydration Drink Price Tracker")

# Dynamic file path resolution
if os.path.exists("hydration_price_tracker/price_history.csv"):
    DATA_FILE = "hydration_price_tracker/price_history.csv"
elif os.path.exists("price_history.csv"):
    DATA_FILE = "price_history.csv"
else:
    st.error("❌ price_history.csv not found in expected locations.")
    st.stop()

# Load and prepare data
df = pd.read_csv(DATA_FILE)
df.dropna(inplace=True)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Extract brand and retailer
df['Brand'] = df['Product'].str.extract(r'^(FlashLyte|GatorLyte|Electrolit|Suerox|Hydrolit)', expand=False)
df['Retailer'] = df['Product'].str.extract(r'- ([\w\s\(\)]+)$', expand=False)
df['Brand'] = df['Brand'].fillna("Unknown")
df['Retailer'] = df['Retailer'].fillna("Unknown")

# Sidebar filters
brands = sorted(df['Brand'].unique())
retailers = sorted(df['Retailer'].unique())

selected_brand = st.sidebar.selectbox("Filter by Brand", ["All"] + brands)
selected_retailer = st.sidebar.selectbox("Filter by Retailer", ["All"] + retailers)

filtered_df = df.copy()
if selected_brand != "All":
    filtered_df = filtered_df[filtered_df['Brand'] == selected_brand]
if selected_retailer != "All":
    filtered_df = filtered_df[filtered_df['Retailer'] == selected_retailer]

# Show filtered data
st.subheader("📊 Price Trends Over Time")
fig = px.line(filtered_df, x="Timestamp", y="Price", color="Product", markers=True)
st.plotly_chart(fig, use_container_width=True)

# Bar chart comparing latest prices
st.subheader("🏷️ Latest Price Comparison Across Retailers")
latest = df.sort_values("Timestamp").drop_duplicates(subset=["Product"], keep="last")
bar_fig = px.bar(latest, x="Product", y="Price", color="Retailer", barmode="group")
st.plotly_chart(bar_fig, use_container_width=True)

# Cross-tab matrix of all brands and all retailers
st.subheader("📋 Price Matrix: All Brands Across All Retailers")
pivot = latest.pivot_table(index='Brand', columns='Retailer', values='Price')
st.dataframe(pivot.style.format("${:.2f}"))

# Confirmed promos section
st.subheader("📌 Confirmed Promos via Scraping")
promo_file = "hydration_price_tracker/all_confirmed_promos.csv"
if os.path.exists(promo_file):
    promo_df = pd.read_csv(promo_file)
    for idx, row in promo_df.iterrows():
        st.markdown(f"**{row['product']}**  \nRetailer: {row['retailer']}  \nPromo: {row['promo']}")
else:
    st.info("No confirmed promo file found.")
