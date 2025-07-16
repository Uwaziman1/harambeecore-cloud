import logging
import pandas as pd
from core.analyze_xau import analyze_gaps
from core.milestone_simulator import simulate_milestones
from core.generate_contracts import generate_contracts
from core.alert_log import generate_alert_log
from core.generate_payment_batch import generate_payment_batch
from core.summary_engine import summarize_project
from live_data_source import (
    get_live_gold_data,
    get_current_milestone,
    create_live_dataframe,
    load_last_milestone,
    save_milestone
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline(mode="historical") -> dict:
    logging.info(f"Starting HarambeeCore simulation [{mode}]")

    try:
        if mode == "historical":
            df = pd.read_csv("gap/XAUUSD_historical.csv", sep=';')
            df["Date"] = pd.to_datetime(df["Date"], format="%Y.%m.%d %H:%M")

    elif mode == "live":
    data = get_live_gold_data()
    if not data:
        return {
            "error": "Failed to fetch live gold data",
            "live_price": None,
            "open_price": None,
            "milestone_price": None,
            "message": "Could not reach GoldAPI."
        }

    price = data["price"]
    open_price = data["open_price"]
    delta = round(price - open_price, 2)

    milestone_price = get_current_milestone(price, interval=30)
    state = load_state()
    last_milestone = state.get("last_milestone", 0)

    if milestone_price == last_milestone:
        direction = "neutral"
        return {
            "live_price": price,
            "open_price": open_price,
            "delta": delta,
            "milestone_price": milestone_price,
            "milestone_direction": direction,
            "message": f"No milestone change. Still at ${milestone_price}"
        }

    direction = "progress" if milestone_price > last_milestone else "delay"
    save_state(milestone_price, direction)

    df = pd.DataFrame(create_live_dataframe(price))
    df["Date"] = pd.to_datetime(df["Date"])

    milestone_log = simulate_milestones(df, step=30)
    contracts = generate_contracts(milestone_log)
    gaps = analyze_gaps(milestone_log)
    alerts = generate_alert_log(contracts)
    payments = generate_payment_batch(contracts)
    summary = summarize_project(milestone_log, contracts)

    contracts["Gap Context"] = [f"Live Snapshot - {direction}"]

    return {
        "milestones": milestone_log,
        "contracts": contracts,
        "gaps": gaps,
        "alerts": alerts,
        "payments": payments,
        "summary": summary,
        "live_price": price,
        "open_price": open_price,
        "delta": delta,
        "milestone_price": milestone_price,
        "milestone_direction": direction,
        "message": f"{'New milestone' if direction == 'progress' else 'Delay'} detected at ${milestone_price}"
    }
