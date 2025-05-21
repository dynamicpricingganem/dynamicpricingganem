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

    # Show current prices
    latest = df.sort_values('Timestamp').groupby('Product').last().reset_index()
    st.subheader("📌 Current Prices")
    st.dataframe(latest[['Product', 'Price', 'Timestamp']])

    # Plot trends
    st.subheader("📈 Price Trends Over Time")
    fig = px.line(df, x='Timestamp', y='Price', color='Product', markers=True)
    st.plotly_chart(fig)
st.sidebar.header("🔍 Filter")
selected_product = st.sidebar.multiselect("Select Product:", options=sorted(df['Product'].unique()), default=list(df['Product'].unique()))
...
st.subheader("🎯 Promotions & Highlights")
    # Export HTML snapshot
    df.to_html("dashboard_snapshot.html")
else:
    st.warning("No data yet. Please upload a 'price_history.csv' file to begin.")
