
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Hydration Price Tracker", layout="wide")
st.title("💧 Hydration Drink Price Tracker")

DATA_FILE = "hydration_price_tracker/price_history.csv"
PROMO_FILE = "hydration_price_tracker/all_confirmed_promos.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df.dropna(inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df['Brand'] = df['Product'].str.extract(r'^(FlashLyte|GatorLyte|Electrolit|Suerox|Hydrolit)', expand=False)
    df['Retailer'] = df['Product'].str.extract(r'- ([\w\s\(\)]+)$', expand=False)
    df['Brand'] = df['Brand'].fillna("Unknown")
    df['Retailer'] = df['Retailer'].fillna("Unknown")

    # Sidebar filters
    st.sidebar.header("Filter")
    selected_brand = st.sidebar.multiselect("Brand:", sorted(df['Brand'].unique()), default=sorted(df['Brand'].unique()))
    selected_retailer = st.sidebar.multiselect("Retailer:", sorted(df['Retailer'].unique()), default=sorted(df['Retailer'].unique()))

    filtered_df = df[
        df['Brand'].isin(selected_brand) &
        df['Retailer'].isin(selected_retailer)
    ]

    # Current prices
    st.subheader("Latest Price Per Product")
    latest = filtered_df.sort_values('Timestamp').groupby('Product').last().reset_index()
    latest[['Brand', 'Retailer']] = latest['Product'].str.extract(r'^(.*) - (.*)$')
    st.dataframe(latest[['Product', 'Brand', 'Retailer', 'Price', 'Timestamp']])

    # Retailer comparison matrix
    st.subheader("Cross-Retailer Price Matrix")
    pivot = latest.pivot_table(index='Brand', columns='Retailer', values='Price')
    st.dataframe(pivot.style.format("${:.2f}"))

    # Price trends
    st.subheader("Price Trends Over Time")
    fig = px.line(filtered_df, x='Timestamp', y='Price', color='Product', markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # 30-day historical trends
    st.subheader("30-Day Historical Trends")
    last_30_days = df[df['Timestamp'] > datetime.now() - timedelta(days=30)]
    fig30 = px.line(last_30_days, x="Timestamp", y="Price", color="Product", line_dash="Retailer")
    st.plotly_chart(fig30, use_container_width=True)

    # Retailer bar chart
    st.subheader("Retailer Price Comparison")
    bar_fig = px.bar(
        latest,
        x="Retailer",
        y="Price",
        color="Brand",
        barmode="group",
        text="Price",
        hover_data=["Product"],
        title="Prices by Retailer per Brand"
    )
    st.plotly_chart(bar_fig, use_container_width=True)

else:
    st.warning("⚠️ 'price_history.csv' not found in hydration_price_tracker/")

# Load confirmed promos
if os.path.exists(PROMO_FILE):
    st.subheader("Confirmed Hydration Promos (via scraping)")

    promos_df = pd.read_csv(PROMO_FILE)
    for _, row in promos_df.iterrows():
        st.success(f"{row['product']} – {row['promo']} at {row['retailer']}")
else:
    st.info("No confirmed promos found. Please check all_confirmed_promos.csv.")
