# 💧 Hydration Drink Price Tracker

This project is a **real-time dashboard** and **price monitoring tool** for hydration drinks in Mexico, such as **Electrolit**, **Suerox**, and **Hydrolit**.

It scrapes major online retailers including:
- Walmart
- Chedraui
- Soriana
- 7-Eleven

And presents price trends in an interactive **Streamlit** dashboard.

---

## 🔧 Features

- 🕵️ Web scraping with `requests`, `BeautifulSoup`, and `Selenium`
- 📈 Interactive dashboard with `Streamlit` and `Plotly`
- 📬 Email alerts for price drops (optional)
- 🌐 Dashboard snapshot exported as HTML
- ☁️ One-click deployment via Streamlit Community Cloud

---

## 🚀 How to Deploy with Streamlit Cloud

1. Clone or fork this repo
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **New App** and connect your GitHub
4. Choose:
    - Repo: `hydration-price-tracker`
    - Branch: `main`
    - File: `price_monitor_dashboard.py`
5. Click **Deploy**

---

## 📨 Email Alerts (Optional)

To enable alerts:
- Open `price_monitor_dashboard.py`
- Replace:
```python
EMAIL_FROM = "your_email@gmail.com"
EMAIL_PASSWORD = "your_password"
EMAIL_TO = "recipient@gmail.com"
```
- Use Gmail App Password if 2FA is on.

---

## 🛠 Requirements

Install locally with:
```bash
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
.
├── price_monitor_dashboard.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── README.md
```

---

## 📸 Example UI

The dashboard shows:
- 📌 Current prices by brand & retailer
- 📊 Historical price trends
- 💾 Auto-export to `dashboard_snapshot.html`

---

Created with ❤️ by [Your Name]
