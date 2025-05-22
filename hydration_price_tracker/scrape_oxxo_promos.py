from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

def scrape_oxxo_hydration_promos():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)

    url = "https://www.oxxo.com/promociones?s=suero"
    driver.get(url)
    time.sleep(5)

    promos = []

    cards = driver.find_elements(By.CLASS_NAME, "ProductCard_card__3wUNM")
    for card in cards:
        try:
            title_elem = card.find_element(By.CLASS_NAME, "ProductCard_title__3vRtp")
            desc_elem = card.find_element(By.CLASS_NAME, "ProductCard_description__33c8H")
            img_elem = card.find_element(By.TAG_NAME, "img")

            promo = {
                "title": desc_elem.text.strip(),
                "promo": title_elem.text.strip(),
                "img_url": img_elem.get_attribute("src")
            }
            promos.append(promo)
        except Exception as e:
            print("Error parsing promo card:", e)

    driver.quit()

    return promos

if __name__ == "__main__":
    promos = scrape_oxxo_hydration_promos()
    df = pd.DataFrame(promos)
    df.to_csv("hydration_price_tracker/oxxo_promos.csv", index=False)
    print("✅ Scraped", len(promos), "hydration promos from OXXO.")
