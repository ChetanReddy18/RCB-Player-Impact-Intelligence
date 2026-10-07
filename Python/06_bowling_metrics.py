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
print("RCB BOWLING METRICS")
print("======================================")

df = pd.read_csv(
    input_file,
    low_memory=False
)

print(
    "Total IPL deliveries:",
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
# SELECT RCB BOWLING DELIVERIES
# ======================================
#
# When team = RCB:
# RCB is batting.
#
# When team != RCB:
# RCB may be bowling.
#
# We identify RCB bowling deliveries by
# finding matches where RCB participated
# and selecting the innings where the
# batting team is the opponent.
#
# ======================================

# Find RCB matches
rcb_match_ids = (
    df[
        df["team"].isin(rcb_names)
    ]["match_id"]
    .unique()
)

# Keep only matches involving RCB
rcb_match_data = df[
    df["match_id"].isin(
        rcb_match_ids
    )
].copy()

# RCB bowling = opponent batting innings
bowling = rcb_match_data[
    ~rcb_match_data["team"].isin(
        rcb_names
    )
].copy()

print(
    "RCB bowling deliveries:",
    len(bowling)
)

# ======================================
# LEGAL BALL
# ======================================

bowling["legal_ball"] = (
    (~bowling["is_wide"]) &
    (~bowling["is_noball"])
).astype(int)

# ======================================
# BOWLER RUNS CONCEDED
# ======================================
#
# Batter runs are charged to the bowler.
# Wides are charged to the bowler.
# No-balls are charged to the bowler.
# Byes and leg-byes are NOT charged.
#
# ======================================

bowling["bowler_runs"] = (
    bowling["total_runs"]
)

# Remove byes and leg-byes from bowler
# runs.

bowling.loc[
    bowling["is_bye"] |
    bowling["is_legbye"],
    "bowler_runs"
] = bowling["batter_runs"]

# Penalty runs are not normally charged
# to the bowler.

bowling.loc[
    bowling["is_penalty"],
    "bowler_runs"
] = 0

# ======================================
# BASIC BOWLING METRICS
# ======================================

bowler_metrics = (
    bowling
    .groupby("bowler")
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
        )
    )
    .reset_index()
)

# ======================================
# BOWLER-CREDITED WICKETS
# ======================================

bowler_wicket_kinds = [
    "bowled",
    "caught",
    "caught and bowled",
    "lbw",
    "stumped",
    "hit wicket"
]

wickets = (
    bowling[
        bowling["wicket_kind"].isin(
            bowler_wicket_kinds
        )
    ]
    .groupby("bowler")
    .size()
    .reset_index(
        name="wickets"
    )
)

bowler_metrics = bowler_metrics.merge(
    wickets,
    on="bowler",
    how="left"
)

bowler_metrics["wickets"] = (
    bowler_metrics["wickets"]
    .fillna(0)
    .astype(int)
)

# ======================================
# DOT BALLS
# ======================================

dot_balls = (
    bowling[
        (bowling["legal_ball"] == 1)
        &
        (bowling["total_runs"] == 0)
    ]
    .groupby("bowler")
    .size()
    .reset_index(
        name="dot_balls"
    )
)

bowler_metrics = bowler_metrics.merge(
    dot_balls,
    on="bowler",
    how="left"
)

bowler_metrics["dot_balls"] = (
    bowler_metrics["dot_balls"]
    .fillna(0)
    .astype(int)
)

# ======================================
# OVERS
# ======================================

bowler_metrics["overs"] = (
    bowler_metrics["balls"] // 6
).astype(int).astype(str) + "." + (
    bowler_metrics["balls"] % 6
).astype(int).astype(str)

# ======================================
# ECONOMY
# ======================================

bowler_metrics["economy"] = (
    bowler_metrics["runs_conceded"]
    /
    (bowler_metrics["balls"] / 6)
)

bowler_metrics["economy"] = (
    bowler_metrics["economy"]
    .replace(
        [float("inf"), -float("inf")],
        0
    )
    .fillna(0)
    .round(2)
)

# ======================================
# BOWLING AVERAGE
# ======================================

bowler_metrics["bowling_average"] = (
    bowler_metrics["runs_conceded"]
    /
    bowler_metrics["wickets"]
)

bowler_metrics.loc[
    bowler_metrics["wickets"] == 0,
    "bowling_average"
] = pd.NA

bowler_metrics["bowling_average"] = (
    bowler_metrics["bowling_average"]
    .round(2)
)

# ======================================
# BOWLING STRIKE RATE
# ======================================

bowler_metrics["strike_rate"] = (
    bowler_metrics["balls"]
    /
    bowler_metrics["wickets"]
)

bowler_metrics.loc[
    bowler_metrics["wickets"] == 0,
    "strike_rate"
] = pd.NA

bowler_metrics["strike_rate"] = (
    bowler_metrics["strike_rate"]
    .round(2)
)

# ======================================
# WICKETS PER MATCH
# ======================================

bowler_metrics["wickets_per_match"] = (
    bowler_metrics["wickets"]
    /
    bowler_metrics["matches"]
)

bowler_metrics["wickets_per_match"] = (
    bowler_metrics["wickets_per_match"]
    .round(2)
)

# ======================================
# MATCH-LEVEL WICKETS
# ======================================

match_wickets = (
    bowling[
        bowling["wicket_kind"].isin(
            bowler_wicket_kinds
        )
    ]
    .groupby(
        [
            "match_id",
            "bowler"
        ]
    )
    .size()
    .reset_index(
        name="match_wickets"
    )
)

# ======================================
# FOUR-WICKET HAULS
# ======================================

four_wickets = (
    match_wickets[
        match_wickets["match_wickets"] >= 4
    ]
    .groupby("bowler")
    .size()
    .reset_index(
        name="four_wicket_hauls"
    )
)

# ======================================
# FIVE-WICKET HAULS
# ======================================

five_wickets = (
    match_wickets[
        match_wickets["match_wickets"] >= 5
    ]
    .groupby("bowler")
    .size()
    .reset_index(
        name="five_wicket_hauls"
    )
)

# ======================================
# MERGE HAULS
# ======================================

bowler_metrics = bowler_metrics.merge(
    four_wickets,
    on="bowler",
    how="left"
)

bowler_metrics = bowler_metrics.merge(
    five_wickets,
    on="bowler",
    how="left"
)

bowler_metrics["four_wicket_hauls"] = (
    bowler_metrics[
        "four_wicket_hauls"
    ]
    .fillna(0)
    .astype(int)
)

bowler_metrics["five_wicket_hauls"] = (
    bowler_metrics[
        "five_wicket_hauls"
    ]
    .fillna(0)
    .astype(int)
)

# ======================================
# DEATH OVER WICKETS
# ======================================
#
# Over numbers are zero-based:
# 0-5   = powerplay
# 6-14  = middle overs
# 15-19 = death overs
#
# ======================================

death_wickets = (
    bowling[
        (bowling["over"] >= 15)
        &
        bowling["wicket_kind"].isin(
            bowler_wicket_kinds
        )
    ]
    .groupby("bowler")
    .size()
    .reset_index(
        name="death_wickets"
    )
)

bowler_metrics = bowler_metrics.merge(
    death_wickets,
    on="bowler",
    how="left"
)

bowler_metrics["death_wickets"] = (
    bowler_metrics[
        "death_wickets"
    ]
    .fillna(0)
    .astype(int)
)

# ======================================
# INTEGER COLUMNS
# ======================================

integer_columns = [
    "matches",
    "balls",
    "runs_conceded",
    "wickets",
    "dot_balls",
    "four_wicket_hauls",
    "five_wicket_hauls",
    "death_wickets"
]

for column in integer_columns:

    bowler_metrics[column] = (
        bowler_metrics[column]
        .fillna(0)
        .astype(int)
    )

# ======================================
# SORT BY WICKETS
# ======================================

bowler_metrics = bowler_metrics.sort_values(
    "wickets",
    ascending=False
)

# ======================================
# SAVE
# ======================================

output_file = (
    output_folder /
    "rcb_bowling_metrics.csv"
)

bowler_metrics.to_csv(
    output_file,
    index=False
)

# ======================================
# DISPLAY
# ======================================

print("\n======================================")
print("TOP RCB BOWLERS")
print("======================================")

print(
    bowler_metrics.head(15).to_string(
        index=False
    )
)

# ======================================
# SUMMARY
# ======================================

print("\n======================================")
print("SUMMARY")
print("======================================")

print(
    "Bowlers:",
    len(bowler_metrics)
)

print(
    "Total wickets:",
    bowler_metrics["wickets"].sum()
)

print(
    "Total dot balls:",
    bowler_metrics["dot_balls"].sum()
)

print(
    "Total runs conceded:",
    bowler_metrics[
        "runs_conceded"
    ].sum()
)

# ======================================
# SUCCESS
# ======================================

print("\n======================================")
print("SUCCESS")
print("======================================")

print("Saved to:")

print(output_file)