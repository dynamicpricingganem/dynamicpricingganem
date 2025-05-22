
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.image("ganem_logo.png", width=180)
st.title("Hydration Drink Price Tracker")

try:
    df = pd.read_csv("hydration_price_tracker/price_history.csv")

    # Convert Timestamp safely
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')
    df = df.dropna(subset=['Timestamp'])

    # Product & Retailer selectors
    st.sidebar.header("Filter")
    selected_product = st.sidebar.multiselect("Select Product", options=df["Product"].unique(), default=None)
    selected_retailer = st.sidebar.multiselect("Select Retailer", options=df["Product"].str.extract(r'- (.*)')[0].unique(), default=None)

    # Apply filters
    if selected_product:
        df = df[df["Product"].isin(selected_product)]
    if selected_retailer:
        df = df[df["Product"].str.contains('|'.join(selected_retailer))]

    # Price Trends Over Time
    st.subheader("📈 Price Trends Over Time")
    fig = px.line(df, x="Timestamp", y="Price", color="Product", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Retailer Comparison Chart
    st.subheader("🏪 Retailer Price Comparison")
    latest = df.sort_values("Timestamp").drop_duplicates("Product", keep="last")
    latest["Retailer"] = latest["Product"].str.extract(r"- (.*)")
    bar = px.bar(latest, x="Retailer", y="Price", color="Product", barmode="group")
    st.plotly_chart(bar, use_container_width=True)

    # Price Table
    st.subheader("🧾 Latest Price Table")
    st.dataframe(latest.sort_values(by="Product")[["Timestamp", "Product", "Price"]])

    # Confirmed Promos
    promo_file = "hydration_price_tracker/all_confirmed_promos.csv"
    try:
        promo_df = pd.read_csv(promo_file)
        st.subheader("💸 Confirmed Hydration Promos")
        for idx, row in promo_df.iterrows():
            st.markdown(f"**{row['product']}** — {row['retailer']} | **{row['promo']}**")
    except Exception as e:
        st.warning("Promo data unavailable.")

except Exception as e:
    st.error("Error loading data. Please check that price_history.csv is correctly formatted and available.")
