
import pandas as pd
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def generate_summary():
    # Load data
    df = pd.read_csv("hydration_price_tracker/price_history.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    last_week = df[df['Timestamp'] > datetime.datetime.now() - datetime.timedelta(days=7)]

    # Latest prices
    latest = last_week.sort_values("Timestamp").groupby("Product").last()

    # First prices from the week
    first = last_week.sort_values("Timestamp").groupby("Product").first()

    # Join and calculate delta
    comparison = latest[['Price']].rename(columns={'Price': 'Last Price'}).join(
        first[['Price']].rename(columns={'Price': 'First Price'})
    )
    comparison['Change'] = comparison['Last Price'] - comparison['First Price']
    comparison['% Change'] = (comparison['Change'] / comparison['First Price']) * 100
    comparison = comparison.sort_values('% Change')

    # Generate HTML content
    html = "<h2>🧃 Weekly Hydration Price Summary</h2>"
    html += "<ul>"
    for product, row in comparison.iterrows():
        sign = "🔻" if row['Change'] < 0 else "🔺"
        html += f"<li><strong>{product}</strong>: {sign} {row['Change']:.2f} MXN ({row['% Change']:.1f}%)</li>"
    html += "</ul>"

    return html

def send_email(html_content):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📊 Weekly Hydration Price Summary"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = os.getenv("EMAIL_TO")

    part = MIMEText(html_content, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        server.sendmail(msg["From"], msg["To"], msg.as_string())

if __name__ == "__main__":
    html_summary = generate_summary()
    send_email(html_summary)
    print("✅ Weekly summary email sent.")
