import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random
from seven_oxxo_scraper import get_price_7eleven, get_price_oxxo

DATA_FILE = "hydration_price_tracker/price_history.csv"
ALERT_THRESHOLD = 20.0

EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_email_alert(product, msg):
    subject = f"🔔 Alert: {product}"
    body = msg

    msg_obj = MIMEMultipart()
    msg_obj["From"] = EMAIL_FROM
    msg_obj["To"] = EMAIL_TO
    msg_obj["Subject"] = subject
    msg_obj.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg_obj.as_string())
        server.quit()
        print(f"Email sent for {product}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def update_prices():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    oxxo_prices = get_price_oxxo()
    data = []

    products = [
        ("Electrolit - OXXO", oxxo_prices.get("Electrolit")),
        ("Suerox - OXXO", oxxo_prices.get("Suerox")),
        ("Suerox - 7-Eleven", get_price_7eleven("https://7-eleven.com.mx/productos/bebidas/suerox-uva-630-ml")),
        ("Electrolit - 7-Eleven", get_price_7eleven("https://7-eleven.com.mx/productos/bebidas/electrolit-manzana-625-ml"))
    ]

    for product, price in products:
        if price is not None:
            data.append({"Timestamp": now, "Product": product, "Price": price})

            # Alerts
            if price < ALERT_THRESHOLD:
                send_email_alert(product, f"⚠️ {product} is below ${ALERT_THRESHOLD:.2f}: now at ${price:.2f}")
            if "Suerox" in product and price <= 15.25:
                send_email_alert(product, f"⭐ Promo Alert: 2x$30.50 detected for {product}")
            if "Electrolit" in product and price <= 21.00:
                send_email_alert(product, f"🔥 Promo Alert: 2x$42 likely active for {product}")
        else:
            print(f"Price not found for {product}")

    df_new = pd.DataFrame(data)

    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(DATA_FILE, index=False)
    print("Price history updated.")

if __name__ == "__main__":
    update_prices()
