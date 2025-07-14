import pandas as pd

def analyze_gaps(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Gap"] = df["Price"].pct_change().abs()
    gaps = df[df["Gap"] > 0.02]
    print("\nDetected Gaps:")
    print(gaps[["Date", "Price", "Gap"]].head())
    return gaps
