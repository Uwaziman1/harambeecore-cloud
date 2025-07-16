# live_data_source.py

import requests
import os
from datetime import datetime

GOLD_API_URL = "https://www.goldapi.io/api/XAU/USD"
API_KEY = os.getenv("GOLDAPI_KEY", "goldapi-4c7dtksmd5sxwxx-io")

def get_live_gold_price():
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(GOLD_API_URL, headers=headers)
        data = response.json()
        price = float(data["price"])
        return round(price, 2)
    except Exception as e:
        print(f"Failed to fetch live gold price: {e}")
        return None

def get_current_milestone(price, interval=30):
    return int(price // interval) * interval

def create_live_dataframe(price):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return [
        {
            "Date": now,
            "Price": price
        }
    ]
