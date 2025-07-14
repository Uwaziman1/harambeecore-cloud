import logging
import pandas as pd
from core.analyze_xau import analyze_gaps
from core.milestone_simulator import simulate_milestones
from core.generate_contracts import generate_contracts
from core.create_alerts import create_alerts
from core.generate_payment_batch import generate_payment_batch

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline() -> dict:
    """Run Build The Bridge simulation pipeline and return structured results."""
    logging.info("🚀 Build The Bridge Simulation Starting...")

    try:
        logging.info("Reading XAUUSD data from gap/XAUUSD_historical.csv...")
        df = pd.read_csv("gap/XAUUSD_historical.csv", sep=';')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d %H:%M')
        logging.info(f"Loaded {len(df)} rows of data.")

        milestone_log = simulate_milestones(df)
        logging.info(f"Milestones found: {len(milestone_log)}")

        contracts = generate_contracts(milestone_log)
        gaps = analyze_gaps(milestone_log)
        alerts = create_alerts(contracts)
        payments = generate_payment_batch(contracts)

        # Attach textual gap contexts (you can extend logic as needed)
        gap_contexts = [
            "None",
            "Pre‑Crisis Boom + Commodities Rise",
            "2008 Global Financial Crisis",
            "Eurozone Crisis & Quantitative Easing",
            "COVID‑19, War in Ukraine, AI‑led Hype"
        ]
        contracts["Gap Context"] = gap_contexts[:len(contracts)]

        # Build a summary
        summary = {
            "Start Date": milestone_log["Date"].min(),
            "End Date": milestone_log["Date"].max(),
            "Total Milestones": len(milestone_log),
            "Total Contracts": len(contracts),
            "Total Gaps Detected": len(gaps)
        }

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
    output = run_pipeline()
    if output:
        print("✅ Simulation completed successfully.")
    else:
        print("❌ Simulation failed.")
