import pandas as pd

def create_alerts(df: pd.DataFrame) -> None:
    print("\nAlerts:")
    for _, row in df.iterrows():
        print(f"[ALERT] {row['Milestone']} reached at ${row['Price']} on {row['Date']}")


