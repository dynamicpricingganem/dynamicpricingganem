import requests
from bs4 import BeautifulSoup

def get_ubereats_prices(store_url, keywords=None):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(store_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []

        for item in soup.find_all('div', class_='ccl-c6'):
            name_tag = item.find('h3')
            price_tag = item.find('div', class_='ccl-13j')

            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True).replace('$', '').replace(',', '')
                try:
                    price_float = float(price)
                    if not keywords or any(k.lower() in name.lower() for k in keywords):
                        products.append((name, price_float))
                except:
                    continue

        return products
    except Exception as e:
        print(f"Uber Eats scrape error: {e}")
        return []

if __name__ == "__main__":
    url = "https://www.ubereats.com/mx/store/7-eleven-irapuato/tn6HRcEUXT-nIYr5i2XZjQ"
    keywords = ["Electrolit", "Suerox", "Hydrolit"]
    for p in get_ubereats_prices(url, keywords):
        print(p)
