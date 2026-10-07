import pandas as pd
import numpy as np
import os

print("=" * 60)
print("RCB VENUE SEASON ANALYSIS")
print("=" * 60)


# =========================================================
# FILE PATHS
# =========================================================

match_file = "data/final/rcb_match_master.csv"

delivery_file = "data/processed/ipl_deliveries_cleaned.csv"

output_file = "data/final/rcb_venue_season_master.csv"


# =========================================================
# LOAD MATCH DATA
# =========================================================

print("\nLoading RCB match data...")

matches = pd.read_csv(match_file)

print("Match rows:", len(matches))

print("\nMatch columns:")
print(matches.columns.tolist())


# =========================================================
# LOAD DELIVERY DATA
# =========================================================

print("\nLoading delivery data...")

deliveries = pd.read_csv(delivery_file)

print("Delivery rows:", len(deliveries))

print("\nDelivery columns:")
print(deliveries.columns.tolist())


# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================

matches.columns = [
    str(col).strip().lower()
    for col in matches.columns
]

deliveries.columns = [
    str(col).strip().lower()
    for col in deliveries.columns
]


# =========================================================
# VENUE CLEANING FUNCTION
# =========================================================

def clean_venue(value):

    value = str(value).strip()

    if "Chinnaswamy" in value:
        return "M Chinnaswamy Stadium"

    return value


# =========================================================
# CLEAN VENUES
# =========================================================

matches["venue"] = matches["venue"].apply(
    clean_venue
)

deliveries["venue"] = deliveries["venue"].apply(
    clean_venue
)


# =========================================================
# CREATE WIN / LOSS / NO RESULT
# =========================================================

print("\nCreating match results...")


matches["result"] = (
    matches["result"]
    .astype(str)
    .str.strip()
    .str.lower()
)


matches["wins"] = np.where(
    matches["result"] == "win",
    1,
    0
)


matches["losses"] = np.where(
    matches["result"] == "loss",
    1,
    0
)


matches["no_results"] = np.where(
    matches["result"].isin(
        [
            "no result",
            "no_result",
            "nr"
        ]
    ),
    1,
    0
)


# =========================================================
# VENUE MATCH SUMMARY
# =========================================================

print("\nCreating season-wise venue match data...")


venue_matches = (
    matches.groupby(
        [
            "season",
            "venue"
        ],
        as_index=False
    )
    .agg(
        matches=("match_id", "nunique"),
        wins=("wins", "sum"),
        losses=("losses", "sum"),
        no_results=("no_results", "sum")
    )
)


# =========================================================
# VENUE RUNS
# =========================================================

print("\nCalculating RCB runs by venue...")


# RCB batting deliveries are already present
# in the cleaned IPL delivery dataset.

rcb_deliveries = deliveries[
    deliveries["team"]
    .astype(str)
    .str.strip()
    .str.lower()
    .isin(
        [
            "royal challengers bangalore",
            "royal challengers bengaluru",
            "rcb"
        ]
    )
].copy()


print(
    "RCB delivery rows:",
    len(rcb_deliveries)
)


# Sum RCB batting runs by season and venue

venue_runs = (
    rcb_deliveries.groupby(
        [
            "season",
            "venue"
        ],
        as_index=False
    )
    .agg(
        runs=("batter_runs", "sum")
    )
)


# =========================================================
# MERGE MATCH + RUN DATA
# =========================================================

result = venue_matches.merge(
    venue_runs,
    on=[
        "season",
        "venue"
    ],
    how="left"
)


# Missing runs = 0

result["runs"] = result[
    "runs"
].fillna(0)


# =========================================================
# WIN PERCENTAGE
# =========================================================

result["win_pct"] = np.where(
    result["matches"] > 0,

    (
        result["wins"]
        /
        result["matches"]
    ) * 100,

    0
)


result["win_pct"] = result[
    "win_pct"
].round(2)


# =========================================================
# LOSS PERCENTAGE
# =========================================================

result["loss_pct"] = np.where(
    result["matches"] > 0,

    (
        result["losses"]
        /
        result["matches"]
    ) * 100,

    0
)


result["loss_pct"] = result[
    "loss_pct"
].round(2)


# =========================================================
# ROUND RUNS
# =========================================================

result["runs"] = result[
    "runs"
].round(0).astype(int)


# =========================================================
# SORT
# =========================================================

result = result.sort_values(
    [
        "season",
        "matches"
    ],
    ascending=[
        True,
        False
    ]
)


# =========================================================
# SAVE
# =========================================================

os.makedirs(
    os.path.dirname(output_file),
    exist_ok=True
)


result.to_csv(
    output_file,
    index=False
)


# =========================================================
# SHOW 2026 DATA
# =========================================================

print("\n" + "=" * 60)
print("2026 VENUE ANALYSIS")
print("=" * 60)


data_2026 = result[
    result["season"].astype(str) == "2026"
]


print(
    data_2026.to_string(
        index=False
    )
)


# =========================================================
# SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)


print(
    "Total rows:",
    len(result)
)


print(
    "Unique venues:",
    result["venue"].nunique()
)


print(
    "Seasons:",
    result["season"].nunique()
)


print("\nSaved to:")

print(output_file)


print("=" * 60)