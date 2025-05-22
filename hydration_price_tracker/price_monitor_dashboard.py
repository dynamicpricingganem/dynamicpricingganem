
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

st.set_page_config(layout="wide")
st.image("hydration_price_tracker/ganem_logo.png", width=180)
st.title(" Hydration Drink Price Tracker")

try:
    df = pd.read_csv("hydration_price_tracker/price_history.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])

    df['Retailer'] = df['Product'].str.split(" - ").str[-1]
    df['Brand'] = df['Product'].str.split(" - ").str[0]

    #  Show full price table immediately after header
    st.subheader(" All Brands & Retailers  Latest Prices")
    latest = df.sort_values("Timestamp").drop_duplicates(subset=["Product"], keep="last")
    table = latest[["Brand", "Retailer", "Price", "Timestamp"]].sort_values(["Brand", "Retailer"])
    st.dataframe(table, use_container_width=True)

    # Sidebar filters
    st.sidebar.header("Filter")
    selected_brand = st.sidebar.multiselect("Brand:", sorted(df['Brand'].unique()), default=sorted(df['Brand'].unique()))
    selected_retailer = st.sidebar.multiselect("Retailer:", sorted(df['Retailer'].unique()), default=sorted(df['Retailer'].unique()))

    filtered_df = df[
        df['Brand'].isin(selected_brand) &
        df['Retailer'].isin(selected_retailer)
    ]

    st.subheader(" Price Trends Over Time")
    fig = px.line(filtered_df, x="Timestamp", y="Price", color="Product", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(" Retailer Price Comparison")
    latest_filtered = filtered_df.sort_values("Timestamp").drop_duplicates(subset=["Product"], keep="last")
    bar_fig = px.bar(
        latest_filtered,
        x="Retailer",
        y="Price",
        color="Brand",
        barmode="group",
        text="Price",
        hover_data=["Product"]
    )
    st.plotly_chart(bar_fig, use_container_width=True)

    st.subheader(" Latest Price Table (Filtered)")
    st.dataframe(latest_filtered.sort_values(by="Product")[["Timestamp", "Product", "Price"]])

    st.subheader(" Confirmed Hydration Promos")
    promo_file = "hydration_price_tracker/all_confirmed_promos.csv"
    if os.path.exists(promo_file):
        promo_df = pd.read_csv(promo_file)
        for idx, row in promo_df.iterrows():
            st.markdown(f"**{row['product']}**  {row['retailer']} | **{row['promo']}**")
    else:
        st.info("No confirmed promos found.")

except Exception as e:
    st.error(" Error loading or displaying data. Please check the CSV files.")
