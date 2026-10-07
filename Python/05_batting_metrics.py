import pandas as pd
from pathlib import Path

# ======================================
# FILE PATHS
# ======================================

input_file = Path(
    "data/processed/rcb_deliveries.csv"
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
print("RCB BATTING METRICS")
print("======================================")

df = pd.read_csv(
    input_file,
    low_memory=False
)

print(
    "Total RCB deliveries:",
    len(df)
)

# ======================================
# BALLS FACED
# ======================================
#
# Wide:
#   Does NOT count as a ball faced.
#
# No-ball:
#   Does NOT count as a legal ball.
#
# Therefore, for this analysis we exclude
# both wides and no-balls.
#
# ======================================

df["ball_faced"] = (
    (~df["is_wide"]) &
    (~df["is_noball"])
).astype(int)

# ======================================
# BASIC PLAYER METRICS
# ======================================

player_metrics = (
    df
    .groupby("batter")
    .agg(
        matches=(
            "match_id",
            "nunique"
        ),

        runs=(
            "batter_runs",
            "sum"
        ),

        balls=(
            "ball_faced",
            "sum"
        )
    )
    .reset_index()
)

# ======================================
# FOURS
# ======================================

fours = (
    df[
        df["batter_runs"] == 4
    ]
    .groupby("batter")
    .size()
    .reset_index(
        name="fours"
    )
)

# ======================================
# SIXES
# ======================================

sixes = (
    df[
        df["batter_runs"] == 6
    ]
    .groupby("batter")
    .size()
    .reset_index(
        name="sixes"
    )
)

# ======================================
# MERGE BOUNDARIES
# ======================================

player_metrics = player_metrics.merge(
    fours,
    on="batter",
    how="left"
)

player_metrics = player_metrics.merge(
    sixes,
    on="batter",
    how="left"
)

player_metrics["fours"] = (
    player_metrics["fours"]
    .fillna(0)
    .astype(int)
)

player_metrics["sixes"] = (
    player_metrics["sixes"]
    .fillna(0)
    .astype(int)
)

# ======================================
# INNINGS SCORES
# ======================================

innings_scores = (
    df
    .groupby(
        [
            "match_id",
            "innings",
            "batter"
        ]
    )["batter_runs"]
    .sum()
    .reset_index(
        name="innings_runs"
    )
)

# ======================================
# INNINGS COUNT
# ======================================

innings_count = (
    innings_scores
    .groupby("batter")
    .size()
    .reset_index(
        name="innings"
    )
)

player_metrics = player_metrics.merge(
    innings_count,
    on="batter",
    how="left"
)

# ======================================
# FIFTIES
# ======================================

fifties = (
    innings_scores[
        (innings_scores["innings_runs"] >= 50)
        &
        (innings_scores["innings_runs"] < 100)
    ]
    .groupby("batter")
    .size()
    .reset_index(
        name="fifties"
    )
)

# ======================================
# HUNDREDS
# ======================================

hundreds = (
    innings_scores[
        innings_scores["innings_runs"] >= 100
    ]
    .groupby("batter")
    .size()
    .reset_index(
        name="hundreds"
    )
)

# ======================================
# 30+ SCORES
# ======================================

thirty_plus = (
    innings_scores[
        innings_scores["innings_runs"] >= 30
    ]
    .groupby("batter")
    .size()
    .reset_index(
        name="thirty_plus"
    )
)

# ======================================
# MERGE SCORE METRICS
# ======================================

for metric in [
    fifties,
    hundreds,
    thirty_plus
]:

    player_metrics = player_metrics.merge(
        metric,
        on="batter",
        how="left"
    )

# ======================================
# FILL MISSING SCORE COUNTS
# ======================================

for column in [
    "fifties",
    "hundreds",
    "thirty_plus"
]:

    player_metrics[column] = (
        player_metrics[column]
        .fillna(0)
        .astype(int)
    )

# ======================================
# STRIKE RATE
# ======================================

player_metrics["strike_rate"] = (
    player_metrics["runs"]
    /
    player_metrics["balls"]
    *
    100
)

player_metrics["strike_rate"] = (
    player_metrics["strike_rate"]
    .replace(
        [float("inf"), -float("inf")],
        0
    )
    .fillna(0)
    .round(2)
)

# ======================================
# DISMISSALS
# ======================================

dismissal_kinds = [
    "bowled",
    "caught",
    "caught and bowled",
    "lbw",
    "stumped",
    "hit wicket",
    "hit the ball twice",
    "obstructing the field",
    "run out",
    "retired out"
]

dismissals = (
    df[
        df["player_out"].notna()
        &
        (df["player_out"] != "")
        &
        df["wicket_kind"].isin(
            dismissal_kinds
        )
    ]
    .groupby("player_out")
    .size()
    .reset_index(
        name="dismissals"
    )
)

player_metrics = player_metrics.merge(
    dismissals,
    left_on="batter",
    right_on="player_out",
    how="left"
)

player_metrics = player_metrics.drop(
    columns=["player_out"]
)

player_metrics["dismissals"] = (
    player_metrics["dismissals"]
    .fillna(0)
    .astype(int)
)

# ======================================
# BATTING AVERAGE
# ======================================

player_metrics["average"] = (
    player_metrics["runs"]
    /
    player_metrics["dismissals"]
)

# No dismissal = average is undefined
player_metrics.loc[
    player_metrics["dismissals"] == 0,
    "average"
] = pd.NA

player_metrics["average"] = (
    player_metrics["average"]
    .round(2)
)

# ======================================
# RUNS PER INNINGS
# ======================================

player_metrics["runs_per_innings"] = (
    player_metrics["runs"]
    /
    player_metrics["innings"]
)

player_metrics["runs_per_innings"] = (
    player_metrics["runs_per_innings"]
    .round(2)
)

# ======================================
# INTEGER COLUMNS
# ======================================

integer_columns = [
    "matches",
    "runs",
    "balls",
    "fours",
    "sixes",
    "innings",
    "fifties",
    "hundreds",
    "thirty_plus",
    "dismissals"
]

for column in integer_columns:

    player_metrics[column] = (
        player_metrics[column]
        .fillna(0)
        .astype(int)
    )

# ======================================
# SORT BY RUNS
# ======================================

player_metrics = player_metrics.sort_values(
    "runs",
    ascending=False
)

# ======================================
# SAVE
# ======================================

output_file = (
    output_folder /
    "rcb_batting_metrics.csv"
)

player_metrics.to_csv(
    output_file,
    index=False
)

# ======================================
# DISPLAY TOP BATTERS
# ======================================

print("\n======================================")
print("TOP RCB BATTERS")
print("======================================")

print(
    player_metrics.head(15).to_string(
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
    "Players:",
    len(player_metrics)
)

print(
    "Total runs:",
    player_metrics["runs"].sum()
)

print(
    "Total fours:",
    player_metrics["fours"].sum()
)

print(
    "Total sixes:",
    player_metrics["sixes"].sum()
)

print(
    "Total balls:",
    player_metrics["balls"].sum()
)

# ======================================
# SUCCESS
# ======================================

print("\n======================================")
print("SUCCESS")
print("======================================")

print("Saved to:")

print(output_file)