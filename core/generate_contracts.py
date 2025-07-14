import pandas as pd

def generate_contracts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Contract"] = df["Milestone"].apply(lambda m: f"Contract for {m}")
    print("\nGenerated Contracts:")
    print(df[["Date", "Milestone", "Contract"]])
    return df


