import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from seven_oxxo_scraper import get_price_7eleven
from uber_scraper import get_ubereats_prices

DATA_FILE = "price_history.csv"
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
    data = []

    # --- Uber Eats 7-Eleven Scraper ---
    uber_url = "https://www.ubereats.com/mx/store/7-eleven-irapuato/tn6HRcEUXT-nIYr5i2XZjQ"
    keywords = ["Electrolit", "Suerox", "Hydrolit"]
    uber_products = get_ubereats_prices(uber_url, keywords)

    for name, price in uber_products:
        data.append({"Timestamp": now, "Product": f"{name} - 7-Eleven (Uber)", "Price": price})
        if price < ALERT_THRESHOLD:
            send_email_alert(name, f"Uber Eats Promo! {name} at ${price:.2f}")
        if "Suerox" in name and price <= 15.25:
            send_email_alert(name, f"⭐ Uber Eats Deal: 2x$30.50 likely active for {name}")
        if "Electrolit" in name and price <= 21.00:
            send_email_alert(name, f"🔥 Uber Eats Promo: 2x$42 likely active for {name}")

    # --- Direct 7-Eleven.com.mx Scraping via Selenium ---
    direct_7e_products = [
        ("Suerox - 7-Eleven", get_price_7eleven("https://7-eleven.com.mx/productos/bebidas/suerox-uva-630-ml")),
        ("Electrolit - 7-Eleven", get_price_7eleven("https://7-eleven.com.mx/productos/bebidas/electrolit-manzana-625-ml"))
    ]

    for product, price in direct_7e_products:
        if price:
            data.append({"Timestamp": now, "Product": product, "Price": price})
            if price < ALERT_THRESHOLD:
                send_email_alert(product, f"Direct 7-Eleven alert: {product} at ${price:.2f}")

    df_new = pd.DataFrame(data)

    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(DATA_FILE, index=False)
    print("✅ Price history updated with Uber Eats and 7-Eleven data.")

if __name__ == "__main__":
    update_prices()
