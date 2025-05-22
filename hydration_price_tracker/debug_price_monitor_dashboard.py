
import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

st.set_page_config(page_title="Hydration Price Tracker (Debug Mode)", layout="wide")
st.title("🔍 Hydration Price Tracker — Debug Mode")

# Display current directory and contents
st.subheader("Environment Diagnostics")
cwd = os.getcwd()
files = os.listdir()
st.code(f"Current Working Directory: {cwd}")
st.code(f"Files in directory: {files}")

# Try loading from subfolder or root
data_paths = ["hydration_price_tracker/price_history.csv", "price_history.csv"]
df = None

for path in data_paths:
    if os.path.exists(path):
        st.success(f"✅ Found file: {path}")
        df = pd.read_csv(path)
        break

if df is not None:
    df.dropna(inplace=True)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df['Brand'] = df['Product'].str.extract(r'^(FlashLyte|GatorLyte|Electrolit|Suerox|Hydrolit)', expand=False)
    df['Retailer'] = df['Product'].str.extract(r'- ([\w\s\(\)]+)$', expand=False)
    df['Brand'] = df['Brand'].fillna("Unknown")
    df['Retailer'] = df['Retailer'].fillna("Unknown")

    st.subheader("📊 Preview of Loaded Data")
    st.dataframe(df.head())

    st.subheader("📈 Price Trends")
    fig = px.line(df, x="Timestamp", y="Price", color="Product", markers=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error("❌ Could not find price_history.csv in expected locations.")
