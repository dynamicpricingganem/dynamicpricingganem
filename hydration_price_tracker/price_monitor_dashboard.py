import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="Hydration Price Tracker", layout="wide")
st.title("💧 Hydration Drink Price Tracker")

DATA_FILE = "price_history.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df.dropna(inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # Sidebar filters
    st.sidebar.header("🔍 Filter")
    all_products = sorted(df['Product'].unique())
    selected_products = st.sidebar.multiselect("Select Product(s):", options=all_products, default=all_products)

    filtered_df = df[df['Product'].isin(selected_products)]

    # Current price snapshot
    st.subheader("📌 Current Prices")
    latest = filtered_df.sort_values('Timestamp').groupby('Product').last().reset_index()
    st.dataframe(latest[['Product', 'Price', 'Timestamp']])

    # Price trends chart
    st.subheader("📈 Price Trends Over Time")
    fig = px.line(filtered_df, x='Timestamp', y='Price', color='Product', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Promotion highlights
    st.subheader("🎯 Promotions & Highlights")
    promo_msgs = []

    for _, row in latest.iterrows():
        product = row['Product']
        price = row['Price']

        if "Electrolit" in product and price <= 21:
            promo_msgs.append(f"🔥 Promo: 2x$42 likely active for **{product}**")
        elif "Suerox" in product and price <= 19:
            promo_msgs.append(f"⭐ Deal: 2x$30.50 likely active for **{product}**")
        elif "Hydrolit" in product and price <= 18:
            promo_msgs.append(f"⚡ Flash Deal: Hydrolit under $18 at **{product}**")

    if promo_msgs:
        for msg in promo_msgs:
            st.success(msg)
    else:
        st.info("No active promotions detected.")

    # Optional export for backup
    df.to_html("dashboard_snapshot.html")
else:
    st.warning("No data yet. Please upload a 'price_history.csv' file to begin.")
