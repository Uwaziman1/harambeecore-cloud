import pandas as pd
import matplotlib.pyplot as plt

def simulate_milestones(df: pd.DataFrame) -> pd.DataFrame:
    milestones = [
        {"label": "Foundation Laid",     "min": 380,  "max": 800},
        {"label": "Pillars Complete",    "min": 800,  "max": 1200},
        {"label": "Deck Installed",      "min": 1200, "max": 1800},
        {"label": "Railings Added",      "min": 1800, "max": 2400},
        {"label": "Bridge Topped Off",   "min": 2400, "max": 3500}
    ]

    milestone_hits = []

    for milestone in milestones:
        condition = (df['Close'] >= milestone["min"]) & (df['Close'] < milestone["max"])
        milestone_df = df[condition]

        if not milestone_df.empty:
            first_hit = milestone_df.iloc[0]
            milestone_hits.append({
                "Date": first_hit["Date"],
                "Price": first_hit["Close"],
                "Milestone": milestone["label"]
            })

    milestone_log = pd.DataFrame(milestone_hits)
    print("\nMilestone Log:")
    print(milestone_log)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(milestone_log["Date"], milestone_log["Price"], marker='o', linestyle='-', color='gold')
    for i, row in milestone_log.iterrows():
        plt.text(row["Date"], row["Price"] + 50, row["Milestone"], ha='center')
    plt.title("\U0001F4C8 Kilimani Bridge Construction Timeline (Gold-Pegged)")
    plt.xlabel("Date")
    plt.ylabel("XAUUSD Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("gap/milestone_plot.png")
    return milestone_log

