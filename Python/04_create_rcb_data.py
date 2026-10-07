import pandas as pd
from pathlib import Path

# ======================================
# FILE PATHS
# ======================================

input_file = Path(
    "data/processed/ipl_deliveries_cleaned.csv"
)

output_folder = Path(
    "data/processed"
)

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

# ======================================
# LOAD DATA
# ======================================

print("======================================")
print("RCB DATASET CREATION")
print("======================================")

df = pd.read_csv(
    input_file,
    low_memory=False
)

print(
    "Total deliveries:",
    len(df)
)

# ======================================
# RCB TEAM NAMES
# ======================================

rcb_names = [
    "Royal Challengers Bangalore",
    "Royal Challengers Bengaluru"
]

# ======================================
# SELECT RCB DELIVERIES
# ======================================

rcb_matches = df[
    df["team"].isin(rcb_names)
].copy()

print(
    "RCB innings deliveries:",
    len(rcb_matches)
)

# ======================================
# MATCH RESULT
# ======================================

def get_result(winner):

    if winner in rcb_names:
        return "Win"

    elif pd.isna(winner) or winner == "":
        return "No Result"

    else:
        return "Loss"


rcb_matches["result"] = (
    rcb_matches["winner"]
    .apply(get_result)
)

# ======================================
# VALIDATION
# ======================================

print("\n======================================")
print("DATA VALIDATION")
print("======================================")

missing_opponent = rcb_matches[
    rcb_matches["opponent"].isna()
    | (rcb_matches["opponent"] == "")
]

print("\nMissing opponents:")

if len(missing_opponent) == 0:
    print("None")
else:
    print(
        missing_opponent[
            [
                "match_id",
                "season",
                "team",
                "opponent",
                "winner",
                "result"
            ]
        ].drop_duplicates()
    )

# ======================================
# SAVE
# ======================================

output_file = (
    output_folder /
    "rcb_deliveries.csv"
)

rcb_matches.to_csv(
    output_file,
    index=False
)

# ======================================
# SUMMARY
# ======================================

print("\n======================================")
print("RCB DATASET CREATED")
print("======================================")

print(
    "RCB deliveries:",
    len(rcb_matches)
)

print(
    "Unique RCB matches:",
    rcb_matches[
        "match_id"
    ].nunique()
)

print("\nSeasons:")

print(
    sorted(
        rcb_matches[
            "season"
        ].dropna().unique(),
        key=str
    )
)

print("\nOpponents:")

print(
    rcb_matches[
        "opponent"
    ].value_counts()
)

print("\nResults:")

print(
    rcb_matches[
        "result"
    ].value_counts()
)

print("\nColumns:")

print(
    rcb_matches.columns.tolist()
)

print("\nSample data:")

print(
    rcb_matches[
        [
            "match_id",
            "season",
            "team",
            "opponent",
            "batter",
            "bowler",
            "batter_runs",
            "is_wide",
            "is_noball",
            "wicket_count",
            "result"
        ]
    ].head(10)
)

print("\n======================================")
print("SUCCESS")
print("======================================")

print("Saved to:")

print(output_file)