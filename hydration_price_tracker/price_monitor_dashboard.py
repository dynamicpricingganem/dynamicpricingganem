
import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(layout="wide")
st.image("hydration_price_tracker/ganem_logo.png", width=180)
st.title("Hydration Drink Price Tracker")

try:
    df = pd.read_csv("hydration_price_tracker/price_history.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])

    df['Retailer'] = df['Product'].str.split(" - ").str[-1]
    df['Brand'] = df['Product'].str.split(" - ").str[0]

    latest = df.sort_values("Timestamp").drop_duplicates(subset=["Product"], keep="last")

    # 1. Comparative Table
    st.subheader("Comparative Table: Latest Prices by Brand and Retailer")
    price_table = latest[["Brand", "Retailer", "Price", "Timestamp"]].sort_values(["Brand", "Retailer"])
    st.dataframe(price_table, use_container_width=True)

    # 2. Price Change Over Time
    st.subheader("Price Trends Over Time")
    fig_line = px.line(df, x="Timestamp", y="Price", color="Product", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

    # 3. Retailer Comparison Bar Chart
    st.subheader("Retailer Price Comparison by Brand")
    brand_colors = {
        brand: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
        for i, brand in enumerate(df['Brand'].unique())
    }
    bar_chart = px.bar(
        latest,
        x="Retailer",
        y="Price",
        color="Brand",
        barmode="group",
        color_discrete_map=brand_colors,
        text="Price",
        hover_data=["Product"]
    )
    st.plotly_chart(bar_chart, use_container_width=True)

    # 4. Confirmed Promotions
    st.subheader("Confirmed Hydration Promotions")
    promo_file = "hydration_price_tracker/all_confirmed_promos.csv"
    if os.path.exists(promo_file):
        promo_df = pd.read_csv(promo_file)
        for idx, row in promo_df.iterrows():
            st.markdown(f"**{row['product']}** — {row['retailer']} | {row['promo']}")
    else:
        st.info("No confirmed promotions found.")

except Exception as e:
    st.error("Error loading data. Please ensure CSV files are valid and properly formatted.")
