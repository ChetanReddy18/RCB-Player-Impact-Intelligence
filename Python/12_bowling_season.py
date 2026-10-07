import pandas as pd
import numpy as np
import os

# =========================================================
# 1. LOAD CLEANED IPL DATA
# =========================================================

input_file = "data/processed/ipl_deliveries_cleaned.csv"

df = pd.read_csv(
    input_file,
    low_memory=False
)

print("======================================")
print("RCB BOWLING SEASON MASTER")
print("======================================")

print("Total IPL deliveries:", len(df))


# =========================================================
# 2. RCB TEAM NAMES
# =========================================================

rcb_names = [
    "Royal Challengers Bangalore",
    "Royal Challengers Bengaluru"
]


# =========================================================
# 3. FIND RCB MATCHES
# =========================================================

rcb_match_ids = (
    df[
        df["team"].isin(rcb_names)
    ]["match_id"]
    .unique()
)

print("RCB matches:", len(rcb_match_ids))


# =========================================================
# 4. KEEP ONLY RCB MATCHES
# =========================================================

rcb_match_data = df[
    df["match_id"].isin(rcb_match_ids)
].copy()


# =========================================================
# 5. SELECT RCB BOWLING INNINGS
#
# When team = RCB -> RCB batting
# When team != RCB -> opponent batting
# Therefore team != RCB = RCB bowling
# =========================================================

bowling = rcb_match_data[
    ~rcb_match_data["team"].isin(rcb_names)
].copy()

print(
    "RCB bowling deliveries:",
    len(bowling)
)


# =========================================================
# 6. CONVERT NUMERIC COLUMNS
# =========================================================

numeric_columns = [
    "total_runs",
    "batter_runs",
    "wicket_count"
]

for column in numeric_columns:

    bowling[column] = pd.to_numeric(
        bowling[column],
        errors="coerce"
    ).fillna(0)


# =========================================================
# 7. BOOLEAN CONVERSION
# =========================================================

def to_bool(series):

    if series.dtype == bool:
        return series

    return (
        series.astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False,
            "1": True,
            "0": False
        })
        .fillna(False)
    )


boolean_columns = [
    "is_wide",
    "is_noball",
    "is_bye",
    "is_legbye",
    "is_penalty"
]

for column in boolean_columns:

    if column in bowling.columns:

        bowling[column] = to_bool(
            bowling[column]
        )


# =========================================================
# 8. LEGAL BALL
#
# Wide and no-ball are not legal deliveries
# =========================================================

bowling["legal_ball"] = (
    (~bowling["is_wide"]) &
    (~bowling["is_noball"])
).astype(int)


# =========================================================
# 9. BOWLER RUNS CONCEDED
#
# Same logic as Python 06
#
# Batter runs -> charged to bowler
# Wides -> charged to bowler
# No-balls -> charged to bowler
# Byes -> NOT charged
# Leg-byes -> NOT charged
# Penalty runs -> NOT charged
# =========================================================

bowling["bowler_runs"] = (
    bowling["total_runs"]
)


# Remove byes and leg-byes from bowler runs

bowling.loc[
    bowling["is_bye"] |
    bowling["is_legbye"],
    "bowler_runs"
] = bowling["batter_runs"]


# Penalty runs are not charged to bowler

bowling.loc[
    bowling["is_penalty"],
    "bowler_runs"
] = 0


# =========================================================
# 10. BOWLER-CREDITED WICKET TYPES
#
# IMPORTANT:
# Do NOT simply sum wicket_count.
# Only these wickets belong to the bowler.
# =========================================================

bowler_wicket_kinds = [
    "bowled",
    "caught",
    "caught and bowled",
    "lbw",
    "stumped",
    "hit wicket"
]


# =========================================================
# 11. CREATE BOWLER-CREDITED WICKET FLAG
# =========================================================

bowling["bowler_wicket"] = (
    bowling["wicket_kind"].isin(
        bowler_wicket_kinds
    )
).astype(int)


# =========================================================
# 12. DOT BALL
# =========================================================

bowling["dot_ball"] = (
    (bowling["legal_ball"] == 1) &
    (bowling["total_runs"] == 0)
).astype(int)


# =========================================================
# 13. DEATH OVER
#
# Same logic as Python 06
#
# Cricsheet over numbering is zero-based:
# 0-5   = Powerplay
# 6-14  = Middle overs
# 15-19 = Death overs
# =========================================================

bowling["death_ball"] = (
    bowling["over"] >= 15
).astype(int)


# =========================================================
# 14. DEATH WICKET
# =========================================================

bowling["death_wicket"] = (
    (bowling["death_ball"] == 1) &
    (bowling["bowler_wicket"] == 1)
).astype(int)


# =========================================================
# 15. PLAYER-SEASON BOWLING AGGREGATION
# =========================================================

result = (
    bowling
    .groupby(
        ["season", "bowler"],
        as_index=False
    )
    .agg(
        matches=(
            "match_id",
            "nunique"
        ),

        balls=(
            "legal_ball",
            "sum"
        ),

        runs_conceded=(
            "bowler_runs",
            "sum"
        ),

        wickets=(
            "bowler_wicket",
            "sum"
        ),

        dot_balls=(
            "dot_ball",
            "sum"
        ),

        death_wickets=(
            "death_wicket",
            "sum"
        )
    )
)


# =========================================================
# 16. OVERS
# =========================================================

result["overs"] = (
    result["balls"] / 6
).round(2)


# =========================================================
# 17. ECONOMY
# =========================================================

result["economy"] = np.where(
    result["balls"] > 0,

    result["runs_conceded"] /
    (result["balls"] / 6),

    0
)


# =========================================================
# 18. BOWLING AVERAGE
# =========================================================

result["bowling_average"] = np.where(
    result["wickets"] > 0,

    result["runs_conceded"] /
    result["wickets"],

    np.nan
)


# =========================================================
# 19. BOWLING STRIKE RATE
# =========================================================

result["bowling_strike_rate"] = np.where(
    result["wickets"] > 0,

    result["balls"] /
    result["wickets"],

    np.nan
)


# =========================================================
# 20. ROUND DECIMAL VALUES
# =========================================================

result["economy"] = (
    result["economy"]
    .round(2)
)

result["bowling_average"] = (
    result["bowling_average"]
    .round(2)
)

result["bowling_strike_rate"] = (
    result["bowling_strike_rate"]
    .round(2)
)


# =========================================================
# 21. SORT
# =========================================================

result = result.sort_values(
    ["season", "wickets"],
    ascending=[True, False]
)


# =========================================================
# 22. SAVE
# =========================================================

output_file = (
    "data/final/rcb_bowling_season_master.csv"
)

os.makedirs(
    os.path.dirname(output_file),
    exist_ok=True
)

result.to_csv(
    output_file,
    index=False
)


# =========================================================
# 23. VALIDATION
# =========================================================

print("\n======================================")
print("BOWLING SEASON MASTER CREATED")
print("======================================")

print(
    "Rows:",
    len(result)
)

print(
    "Unique bowlers:",
    result["bowler"].nunique()
)

print(
    "Total wickets:",
    result["wickets"].sum()
)

print(
    "Total dot balls:",
    result["dot_balls"].sum()
)

print(
    "Total runs conceded:",
    result["runs_conceded"].sum()
)


# =========================================================
# 24. SEASON WICKET TOTALS
# =========================================================

print("\n======================================")
print("SEASON WICKET TOTALS")
print("======================================")

season_wickets = (
    result
    .groupby("season")["wickets"]
    .sum()
)

print(
    season_wickets.to_string()
)


# =========================================================
# 25. TOP 10 BOWLERS - 2026
# =========================================================

print("\n======================================")
print("TOP 10 RCB BOWLERS - 2026")
print("======================================")

top_2026 = (
    result[
        result["season"] == "2026"
    ]
    .head(10)
)

print(
    top_2026.to_string(
        index=False
    )
)


# =========================================================
# 26. SUCCESS
# =========================================================

print("\n======================================")
print("SUCCESS")
print("======================================")

print(
    "Saved to:"
)

print(
    output_file
)