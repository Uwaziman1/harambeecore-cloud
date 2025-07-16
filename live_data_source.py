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
    headers = {
        "x-access-token": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(GOLD_API_URL, headers=headers)
        data = r.json()
        return {
            "price": round(float(data["price"]), 2),
            "open_price": round(float(data["open_price"]), 2)
        }
    except Exception as e:
        print(f"GoldAPI fetch error: {e}")
        return None

def get_current_milestone(price, interval=30):
    return int(price // interval) * interval

def create_live_dataframe(price):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    return [{"Date": now, "Price": price}]

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"last_milestone": 0, "last_direction": "neutral"}

def save_state(milestone, direction):
    with open(STATE_FILE, "w") as f:
        json.dump({"last_milestone": milestone, "last_direction": direction}, f)
