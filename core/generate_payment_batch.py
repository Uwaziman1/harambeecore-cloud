import pandas as pd

def generate_payment_batch(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Amount"] = df["Price"] * 100  # mock calculation
    df["Recipient"] = "Contractor ABC Ltd"
    df["Payment Status"] = "Pending Verification"
    return df[["Milestone", "Amount", "Recipient", "Date", "Payment Status"]]
