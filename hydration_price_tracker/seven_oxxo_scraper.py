from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def setup_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def get_price_7eleven(url):
    try:
        driver = setup_driver()
        driver.get(url)
        time.sleep(5)
        price_element = driver.find_element(By.CLASS_NAME, 'price')
        price_text = price_element.text.strip().replace('$', '').replace(',', '')
        driver.quit()
        return float(price_text)
    except Exception as e:
        print(f"7-Eleven scrape error: {e}")
        return None

def get_price_oxxo(url=None):
    # OXXO doesn't list prices online; fallback to manual detection
    print("OXXO site does not provide dynamic pricing. Returning static promo prices.")
    fallback_prices = {
        "Electrolit": 21.00,
        "Suerox": 15.25  # represents 2x$30.50 promo
    }
    return fallback_prices
