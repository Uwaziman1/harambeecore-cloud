import pandas as pd

def generate_payment_batch(df: pd.DataFrame) -> None:
    df = df.copy()
    df["Amount"] = df["Price"] * 100  # example calculation
    print("\nPayment Batch:")
    print(df[["Milestone", "Amount"]])

