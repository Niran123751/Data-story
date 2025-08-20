"""
Analyze quarterly customer retention trends and generate visualizations.
"""
import os
import json
import pandas as pd
import matplotlib.pyplot as plt

DATA_PATH = "data/retention_2024.csv"
CHARTS_DIR = "charts"
REPORTS_DIR = "reports"
INDUSTRY_TARGET = 85.0

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(DATA_PATH)
order = ["Q1", "Q2", "Q3", "Q4"]
df["quarter"] = pd.Categorical(df["quarter"], order, ordered=True)
df = df.sort_values("quarter")

# Basic stats
avg = df["retention_rate"].mean()
gap_to_target = INDUSTRY_TARGET - avg

# Save a small machine-readable report
report = {
    "average_retention": round(float(avg), 2),
    "industry_target": INDUSTRY_TARGET,
    "gap_to_target": round(float(gap_to_target), 2),
    "latest_quarter": df["quarter"].iloc[-1],
    "latest_retention": round(float(df["retention_rate"].iloc[-1]), 2),
}
with open(os.path.join(REPORTS_DIR, "summary.json"), "w") as f:
    json.dump(report, f, indent=2)

# --- Chart 1: Trend with benchmark line ---
plt.figure(figsize=(8, 5))
plt.plot(df["quarter"], df["retention_rate"], marker="o")
plt.axhline(INDUSTRY_TARGET, linestyle="--")
plt.title("Customer Retention Rate – 2024 Quarterly Trend vs. Industry Target")
plt.xlabel("Quarter")
plt.ylabel("Retention Rate")
plt.ylim(0, max(INDUSTRY_TARGET, df["retention_rate"].max()) + 10)
for x, y in zip(df["quarter"], df["retention_rate"]):
    plt.text(x, y + 1, f"{y:.2f}", ha="center", va="bottom", fontsize=9)
plt.text(0.05, 0.9, f"Avg 2024: {avg:.2f}", transform=plt.gca().transAxes)
plt.text(0.05, 0.84, f"Target: {INDUSTRY_TARGET:.0f}", transform=plt.gca().transAxes)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "retention_trend.png"), dpi=160)
plt.close()

# --- Chart 2: Gap to target by quarter and average ---
plot_df = df[["quarter", "retention_rate"]].copy()
avg_row = pd.DataFrame({"quarter": ["Avg"], "retention_rate": [avg]})
plot_df = pd.concat([plot_df, avg_row], ignore_index=True)
plot_df["gap"] = INDUSTRY_TARGET - plot_df["retention_rate"]

plt.figure(figsize=(8, 5))
plt.bar(plot_df["quarter"], plot_df["gap"])
plt.title("Gap to Industry Target (85) – Lower Is Better")
plt.xlabel("Quarter (and 2024 Avg)")
plt.ylabel("Points below target")
for x, y in zip(plot_df["quarter"], plot_df["gap"]):
    plt.text(x, y + 0.6, f"{y:.2f}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "retention_gap_to_target.png"), dpi=160)
plt.close()

print(json.dumps(report, indent=2))
