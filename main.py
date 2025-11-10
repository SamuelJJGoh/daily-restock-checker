import requests
import smtplib
import os
from dotenv import load_dotenv
import sys

load_dotenv()


# public JSON endpoint that Shopify stores provide
PRODUCT_URL_JSON = "https://uk.danielwellington.com/products/emalie-earrings-rose-gold-satin-white.js"
PRODUCT_URL = "https://uk.danielwellington.com/products/emalie-earrings-rose-gold-satin-white"

SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

headers = {
    "Accept-Language": "en-GB,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
}

try:
    response = requests.get(url=PRODUCT_URL_JSON, headers=headers)
    response.raise_for_status()
    website_json = response.json()
except Exception as e:
     print(f"Error fetching product data: {e}")
     sys.exit(1)

product_name = website_json["title"]
variants = website_json["variants"]
for v in variants:
    product_availability = v["available"]

if product_availability == False :
    with smtplib.SMTP(SMTP_SERVER, port=587) as connection :
        connection.starttls()
        connection.login(user=SMTP_USERNAME, password=SMTP_PASSWORD)
        connection.sendmail(
            from_addr=SMTP_USERNAME,
            to_addrs=RECIPIENT_EMAIL,
            msg=f"Subject:UNAVAILABLE! The product {product_name} is still SOLD OUT! 🥲 BUT I LOVE YOU".encode("utf-8")
        )
else :
    with smtplib.SMTP(SMTP_SERVER, port=587) as connection :
            connection.starttls()
            connection.login(user=SMTP_USERNAME, password=SMTP_PASSWORD)
            connection.sendmail(
                from_addr=SMTP_USERNAME,
                to_addrs=RECIPIENT_EMAIL,
                msg=f"Subject:AVAILABLE! The product {product_name} is now available! 🥳\n\nBuy it here : {PRODUCT_URL}".encode("utf-8")
            )