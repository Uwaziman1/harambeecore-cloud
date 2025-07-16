# live_data_source.py

import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GOLD_API_URL = "https://www.goldapi.io/api/XAU/USD"
API_KEY = os.getenv("GOLDAPI_KEY")
STATE_FILE = "milestone_state.json"

def get_live_gold_data():
    if not API_KEY:
        raise EnvironmentError("GOLDAPI_KEY not set")

    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(GOLD_API_URL, headers=headers)
        data = response.json()
        return {
            "price": round(float(data["price"]), 2),
            "open_price": round(float(data["open_price"]), 2)
        }
    except Exception as e:
        print(f"Error fetching gold data: {e}")
        return None

def get_current_milestone(price, interval=30):
    return int(price // interval) * interval

def create_live_dataframe(price):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return [{"Date": now, "Price": price}]

def load_last_milestone():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("last_milestone", 0)
    except FileNotFoundError:
        return 0

def save_milestone(new_milestone):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_milestone": new_milestone}, f)
