# run_pipeline.py

import logging
import pandas as pd
from core.analyze_xau import analyze_gaps
from core.milestone_simulator import simulate_milestones
from core.generate_contracts import generate_contracts
from core.alert_log import generate_alert_log
from core.generate_payment_batch import generate_payment_batch
from core.summary_engine import summarize_project
from live_data_source import (
    get_live_gold_price,
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
            price = get_live_gold_price()
            if price is None:
                return {
                    "error": "Failed to fetch live gold price",
                    "live_price": None,
                    "milestone_price": None,
                    "message": "Could not reach GoldAPI."
                }

            milestone_price = get_current_milestone(price, interval=30)
            last_milestone = load_last_milestone()

            if milestone_price <= last_milestone:
                return {
                    "live_price": price,
                    "milestone_price": milestone_price,
                    "message": f"No new milestone. Last was {last_milestone}"
                }

            save_milestone(milestone_price)

            df = pd.DataFrame(create_live_dataframe(price))
            df["Date"] = pd.to_datetime(df["Date"])

            milestone_log = simulate_milestones(df, step=30)
            contracts = generate_contracts(milestone_log)
            gaps = analyze_gaps(milestone_log)
            alerts = generate_alert_log(contracts)
            payments = generate_payment_batch(contracts)
            summary = summarize_project(milestone_log, contracts)

            contracts["Gap Context"] = ["Live Snapshot"]

            return {
                "milestones": milestone_log,
                "contracts": contracts,
                "gaps": gaps,
                "alerts": alerts,
                "payments": payments,
                "summary": summary,
                "live_price": price,
                "milestone_price": milestone_price,
                "message": f"New milestone triggered at ${milestone_price}"
            }

        else:
            return {"error": "Invalid mode"}

        # Historical flow (unchanged)
        milestone_log = simulate_milestones(df)
        contracts = generate_contracts(milestone_log)
        gaps = analyze_gaps(milestone_log)
        alerts = generate_alert_log(contracts)
        payments = generate_payment_batch(contracts)
        summary = summarize_project(milestone_log, contracts)

        contracts["Gap Context"] = [
            "None",
            "Pre-Crisis Boom + Commodities Rise",
            "2008 Global Financial Crisis",
            "Eurozone Crisis & Quantitative Easing",
            "COVID-19, War in Ukraine, AI-led Hype"
        ][:len(contracts)]

        return {
            "milestones": milestone_log,
            "contracts": contracts,
            "gaps": gaps,
            "alerts": alerts,
            "payments": payments,
            "summary": summary
        }

    except Exception as e:
        logging.exception(f"Pipeline failed: {e}")
        return {
            "error": str(e),
            "live_price": None,
            "milestone_price": None,
            "message": "Exception in pipeline"
        }

if __name__ == "__main__":
    run_pipeline()
