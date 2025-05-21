import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from uber_scraper import get_ubereats_prices

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
    data = []

    # --- Static fallback OXXO pricing ---
    oxxo_prices = {
        "Suerox": 15.25,           # 2x$30.50
        "Electrolit": 21.00        # 2x$42
    }

    for brand, price in oxxo_prices.items():
        product = f"{brand} - OXXO"
        data.append({"Timestamp": now, "Product": product, "Price": price})
        if price < ALERT_THRESHOLD:
            send_email_alert(product, f"OXXO promo: {product} at ${price:.2f}")

    # --- Uber Eats 7-Eleven scrape ---
    uber_url = "https://www.ubereats.com/mx/store/7-eleven-irapuato/tn6HRcEUXT-nIYr5i2XZjQ"
    keywords = ["Electrolit", "Suerox", "Hydrolit"]
    uber_products = get_ubereats_prices(uber_url, keywords)

    for name, price in uber_products:
        product = f"{name} - 7-Eleven (Uber)"
        data.append({"Timestamp": now, "Product": product, "Price": price})
        if price < ALERT_THRESHOLD:
            send_email_alert(product, f"Uber Eats promo: {product} at ${price:.2f}")

    # --- Placeholder for Selenium scrape (disabled for CI) ---
    print("📭 Selenium-based 7-eleven.com.mx scrape is currently disabled for GitHub Actions.")

    df_new = pd.DataFrame(data)

    if os.path.exists(DATA_FILE):
        df_existing = pd.read_csv(DATA_FILE)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_csv(DATA_FILE, index=False)
    print("✅ Price history updated with OXXO and Uber Eats data.")

if __name__ == "__main__":
    update_prices()
