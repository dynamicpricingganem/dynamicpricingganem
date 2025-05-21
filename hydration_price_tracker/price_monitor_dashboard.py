import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="Hydration Price Tracker", layout="wide")
st.title("Hydration Drink Price Tracker - GANEM")

DATA_FILE = "hydration_price_tracker/price_history.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df.dropna(inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Extract brand and retailer more robustly
    df['Brand'] = df['Product'].str.extract(r'^(FlashLyte|GatorLyte|Electrolit|Suerox|Hydrolit)', expand=False)
    df['Retailer'] = df['Product'].str.extract(r'- ([\w\s\(\)]+)$', expand=False)
    df['Brand'] = df['Brand'].fillna("Unknown")
    df['Retailer'] = df['Retailer'].fillna("Unknown")

    # Sidebar filters
    st.sidebar.header("🔍 Filter")
    selected_brand = st.sidebar.multiselect("Brand:", sorted(df['Brand'].unique()), default=sorted(df['Brand'].unique()))
    selected_retailer = st.sidebar.multiselect("Retailer:", sorted(df['Retailer'].unique()), default=sorted(df['Retailer'].unique()))

    filtered_df = df[
        df['Brand'].isin(selected_brand) &
        df['Retailer'].isin(selected_retailer)
    ]

    # Current prices
    st.subheader("📌 Latest Price Per Product")
    latest = filtered_df.sort_values('Timestamp').groupby('Product').last().reset_index()
    latest[['Brand', 'Retailer']] = latest['Product'].str.extract(r'^(.*) - (.*)$')
    st.dataframe(latest[['Product', 'Brand', 'Retailer', 'Price', 'Timestamp']])

    # Retailer comparison
    st.subheader("🏪 Cross-Retailer Price Matrix")
    pivot = latest.pivot_table(index='Brand', columns='Retailer', values='Price')
    st.dataframe(pivot.style.format("${:.2f}"))

    # Price trends
    st.subheader("📈 Price Trends Over Time")
    fig = px.line(filtered_df, x='Timestamp', y='Price', color='Product', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Promo detection
    st.subheader("🎯 Promo Highlights")
    promo_msgs = []
    for _, row in latest.iterrows():
        product = row['Product']
        price = row['Price']
        if "Electrolit" in product and price <= 21.00:
            promo_msgs.append(f"🔥 2x$42 promo likely active for **{product}**")
        elif "Suerox" in product and price <= 15.25:
            promo_msgs.append(f"⭐ 2x$30.50 promo detected for **{product}**")
        elif "FlashLyte" in product and price <= 18:
            promo_msgs.append(f"⚡ Flash deal under $18 for **{product}**")

    if promo_msgs:
        for msg in promo_msgs:
            st.success(msg)
    else:
        st.info("No active promos detected.")
else:
    st.warning("No data yet. Please upload or generate 'price_history.csv'.")
