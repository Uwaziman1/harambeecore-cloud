import logging
import pandas as pd

from core.analyze_xau import analyze_gaps
from core.milestone_simulator import simulate_milestones
from core.generate_contracts import generate_contracts
from core.create_alerts import create_alerts
from core.generate_payment_batch import generate_payment_batch

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline() -> pd.DataFrame:
    """Run Build The Bridge simulation pipeline."""
    logging.info("\U0001F680 Build The Bridge Simulation Starting...")

    try:
        logging.info("Reading XAUUSD data from gap/XAUUSD_historical.csv...")
        df = pd.read_csv("gap/XAUUSD_historical.csv", sep=';')
        df['Date'] = pd.to_datetime(df['Date'], format='%Y.%m.%d %H:%M')
        logging.info(f"Loaded {len(df)} rows of data")

        milestone_log = simulate_milestones(df)
        logging.info(f"Milestones found: {len(milestone_log)}")

        contracts = generate_contracts(milestone_log)
        gaps = analyze_gaps(milestone_log)
        create_alerts(contracts)
        generate_payment_batch(contracts)

        return contracts

    except Exception as e:
        logging.exception(f"Pipeline failed due to: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    run_pipeline()
