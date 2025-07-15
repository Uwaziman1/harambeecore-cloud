# run_pipeline.py

import logging
import pandas as pd

from core.analyze_xau import analyze_gaps
from core.milestone_simulator import simulate_milestones
from core.generate_contracts import generate_contracts
from core.create_alerts import create_alerts
from core.generate_payment_batch import generate_payment_batch
from core.alert_log import generate_alert_log
from core.summary_engine import summarize_project

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline() -> dict:
    """Run Build The Bridge simulation pipeline."""
    logging.info("🚀 Build The Bridge Simulation Starting...")

    try:
        logging.info("Reading XAUUSD data from gap/XAUUSD_historical.csv...")
        df = pd.read_csv("gap/XAUUSD_historical.csv", sep=';')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d %H:%M')
        logging.info(f"Loaded {len(df)} rows of data")

        milestone_log = simulate_milestones(df)
        logging.info(f"Milestones found: {len(milestone_log)}")

        contracts = generate_contracts(milestone_log)
        gaps = analyze_gaps(milestone_log)
        alerts = generate_alert_log(contracts)
        payments = generate_payment_batch(contracts)
        summary = summarize_project(milestone_log, contracts)

        gap_contexts = [
            "None",
            "Pre-Crisis Boom + Commodities Rise",
            "2008 Global Financial Crisis",
            "Eurozone Crisis & Quantitative Easing",
            "COVID-19, War in Ukraine, AI-led Hype"
        ]
        contracts["Gap Context"] = gap_contexts[:len(contracts)]

        return {
            "milestones": milestone_log,
            "contracts": contracts,
            "gaps": gaps,
            "alerts": alerts,
            "payments": payments,
            "summary": summary
        }

    except Exception as e:
        logging.exception(f"Pipeline failed due to: {e}")
        return {}

if __name__ == "__main__":
    run_pipeline()
