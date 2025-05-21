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

    # Attempt to extract structured fields
    df[['Brand', 'Retailer']] = df['Product'].str.extract(r'^(.*) - (.*)$')
    df['Flavor'] = df['Product'].str.extract(r'(Manzana|Uva|Coco|Toronja|Limón|Mandarina)', expand=False)
    df['Size_ml'] = df['Product'].str.extract(r'(\d{3,4})\s*ml', expand=False)
    df['Size_ml'] = df['Size_ml'].fillna('625')  # default for consistency

    # Sidebar filters
    st.sidebar.header("🔍 Filter")
    selected_brand = st.sidebar.multiselect("Brand:", options=sorted(df['Brand'].dropna().unique()), default=sorted(df['Brand'].dropna().unique()))
    selected_retailer = st.sidebar.multiselect("Retailer:", options=sorted(df['Retailer'].dropna().unique()), default=sorted(df['Retailer'].dropna().unique()))
    selected_flavor = st.sidebar.multiselect("Flavor (if detected):", options=sorted(df['Flavor'].dropna().unique()), default=sorted(df['Flavor'].dropna().unique()))

    # Apply filters
    filtered_df = df[
        df['Brand'].isin(selected_brand) &
        df['Retailer'].isin(selected_retailer) &
        (df['Flavor'].isin(selected_flavor) | df['Flavor'].isna())
    ]

    # Show current prices table
    st.subheader("📌 Current Prices by Brand & Retailer")
    latest = filtered_df.sort_values('Timestamp').groupby('Product').last().reset_index()
    latest_display = latest.copy()
    latest_display[['Brand', 'Retailer']] = latest_display['Product'].str.extract(r'^(.*) - (.*)$')
    st.dataframe(latest_display[['Brand', 'Retailer', 'Price', 'Timestamp']].sort_values(by='Brand'))

    # Retailer comparison chart
    st.subheader("🏪 Retailer Comparison for Selected Brands")
    if not latest_display.empty:
        fig2 = px.bar(latest_display, x='Brand', y='Price', color='Retailer', barmode='group', text='Price')
        st.plotly_chart(fig2, use_container_width=True)

    # Price trends chart
    st.subheader("📈 Price Trends Over Time")
    fig = px.line(filtered_df, x='Timestamp', y='Price', color='Product', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Promotions section
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

else:
    st.warning("No data yet. Please upload a 'price_history.csv' file to begin.")
