import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random

DATA_FILE = "hydration_price_tracker/price_history.csv"
ALERT_THRESHOLD = 20.0

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_email_alert(product, price):
    subject = f"🔔 Price Drop Alert: {product} now at ${price:.2f}"
    body = f"Good news! {product} is now priced at ${price:.2f}. Check it out."

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print(f"Email sent for {product}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def update_prices():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sample_products = [
        "Electrolit - Walmart",
        "Suerox - Chedraui",
        "Hydrolit - Soriana"
    ]

    new_data = []
    for product in sample_products:
        price = round(random.uniform(18.0, 25.0), 2)
        new_data.append({"Timestamp": now, "Product": product, "Price": price})
        if price < ALERT_THRESHOLD:
            send_email_alert(product, price)

    df_new = pd.DataFrame(new_data)

    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(DATA_FILE, index=False)
    print("Prices updated.")

if __name__ == "__main__":
    update_prices()
