        if price < ALERT_THRESHOLD:
            send_email_alert(product, price)

        # Additional promo alerts
        if "Electrolit" in product and price <= 21:
            send_email_alert(product, f"Promo alert: 2x$42 may be active — price at ${price}")
        if "Suerox" in product and price <= 19:
            send_email_alert(product, f"Promo alert: 2x$30.50 may be active — price at ${price}")
