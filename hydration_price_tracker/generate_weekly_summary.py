import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")
DATA_FILE = "hydration_price_tracker/price_history.csv"

def generate_summary_html(df):
    summary = ""

    # Lowest prices
    latest = df.sort_values('Timestamp').groupby('Product').last().reset_index()
    lowest_prices = latest.sort_values('Price').groupby('Brand').first()

    summary += "<h2>💧 Lowest Prices This Week</h2><ul>"
    for _, row in lowest_prices.iterrows():
        summary += f"<li><strong>{row['Product']}</strong>: ${row['Price']:.2f}</li>"
    summary += "</ul>"

    # Price drops
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    week_ago = datetime.now() - timedelta(days=7)
    recent = df[df['Timestamp'] > week_ago]

    changes = []
    if not recent.empty:
        for product in recent['Product'].unique():
            prices = recent[recent['Product'] == product].sort_values('Timestamp')['Price']
            if len(prices) > 1:
                change = prices.iloc[-1] - prices.iloc[0]
                changes.append((product, change))

    drops = sorted([c for c in changes if c[1] < 0], key=lambda x: x[1])

    summary += "<h2>📉 Biggest Price Drops</h2><ul>"
    for product, drop in drops[:5]:
        summary += f"<li><strong>{product}</strong>: dropped ${abs(drop):.2f}</li>"
    summary += "</ul>"

    # Promotions
    summary += "<h2>🔥 Detected Promotions</h2><ul>"
    for _, row in latest.iterrows():
        product = row['Product']
        price = row['Price']
        if "Electrolit" in product and price <= 21:
            summary += f"<li>🔥 2x$42 likely active for <strong>{product}</strong></li>"
        elif "Suerox" in product and price <= 15.25:
            summary += f"<li>⭐ 2x$30.50 likely active for <strong>{product}</strong></li>"
        elif "FlashLyte" in product and price <= 18:
            summary += f"<li>⚡ FlashLyte under $18 at <strong>{product}</strong></li>"
    summary += "</ul>"

    return summary

def send_email(html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "🧃 Weekly Hydration Price Summary"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print("✅ Weekly summary email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def main():
    if not os.path.exists(DATA_FILE):
        print("⚠️ No data file found.")
        return

    df = pd.read_csv(DATA_FILE)
    df.dropna(inplace=True)
    df['Brand'] = df['Product'].str.extract(r'^(FlashLyte|GatorLyte|Electrolit|Suerox|Hydrolit)', expand=False)
    df = df[df['Brand'].notna()]

    html = "<html><body>"
    html += "<h1>🧃 Weekly Hydration Market Report</h1>"
    html += generate_summary_html(df)
    html += "<p><i>Generated on " + datetime.now().strftime("%Y-%m-%d %H:%M") + "</i></p>"
    html += "</body></html>"

    send_email(html)

if __name__ == "__main__":
    main()
