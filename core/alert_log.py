import pandas as pd

def generate_alert_log(df: pd.DataFrame) -> pd.DataFrame:
    alerts = []
    for _, row in df.iterrows():
        alerts.append({
            "Milestone": row["Milestone"],
            "Date": row["Date"],
            "Message": f"Contract triggered for {row['Milestone']} at ${row['Price']}"
        })
    return pd.DataFrame(alerts)
