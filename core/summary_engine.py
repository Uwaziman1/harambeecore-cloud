import pandas as pd

def summarize_project(milestones: pd.DataFrame, contracts: pd.DataFrame) -> dict:
    summary = {
        "Total Milestones": len(milestones),
        "Total Contracts": len(contracts),
        "Start Date": milestones["Date"].min(),
        "End Date": milestones["Date"].max(),
        "Duration (days)": (milestones["Date"].max() - milestones["Date"].min()).days
    }
    return summary
