import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# FILE PATHS
# ============================================================

batting_file = Path("data/processed/rcb_batting_metrics.csv")
bowling_file = Path("data/processed/rcb_bowling_metrics.csv")

output_file = Path("data/processed/rcb_player_impact.csv")


# ============================================================
# LOAD DATA
# ============================================================

batting = pd.read_csv(batting_file)
bowling = pd.read_csv(bowling_file)

print("=" * 60)
print("RCB PLAYER IMPACT ANALYSIS")
print("=" * 60)

print(f"Batting players : {len(batting)}")
print(f"Bowling players : {len(bowling)}")


# ============================================================
# HELPER FUNCTION
# ============================================================

def min_max_score(series):
    """
    Convert a numerical column into a 0-100 score.

    Higher value = higher score.
    """

    series = pd.to_numeric(series, errors="coerce").fillna(0)

    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(50.0, index=series.index)

    return ((series - min_value) / (max_value - min_value)) * 100


def inverse_score(series):
    """
    Convert a lower-is-better metric into a 0-100 score.

    Example:
    Lower bowling economy = better score.
    """

    series = pd.to_numeric(series, errors="coerce").fillna(0)

    min_value = series.min()
    max_value = series.max()

    if max_value == min_value:
        return pd.Series(50.0, index=series.index)

    return ((max_value - series) / (max_value - min_value)) * 100


# ============================================================
# BATTING IMPACT
# ============================================================

bat = batting.copy()

print("\nCalculating batting impact...")


# Normalize batting metrics

bat["runs_score"] = min_max_score(bat["runs"])

bat["strike_rate_score"] = min_max_score(
    bat["strike_rate"]
)

bat["average_score"] = min_max_score(
    bat["average"]
)

bat["fifties_score"] = min_max_score(
    bat["fifties"]
)

bat["hundreds_score"] = min_max_score(
    bat["hundreds"]
)

bat["sixes_score"] = min_max_score(
    bat["sixes"]
)


# ------------------------------------------------------------
# Batting Impact Formula
# ------------------------------------------------------------
#
# Runs              = 30%
# Strike Rate       = 20%
# Average           = 20%
# 50s               = 10%
# Hundreds          = 10%
# Sixes             = 10%
#
# Total             = 100%
# ------------------------------------------------------------

bat["batting_impact"] = (
    bat["runs_score"] * 0.30
    + bat["strike_rate_score"] * 0.20
    + bat["average_score"] * 0.20
    + bat["fifties_score"] * 0.10
    + bat["hundreds_score"] * 0.10
    + bat["sixes_score"] * 0.10
)


# ============================================================
# BOWLING IMPACT
# ============================================================

bowl = bowling.copy()

print("Calculating bowling impact...")


# Normalize bowling metrics

bowl["wickets_score"] = min_max_score(
    bowl["wickets"]
)

bowl["economy_score"] = inverse_score(
    bowl["economy"]
)

bowl["bowling_average_score"] = inverse_score(
    bowl["bowling_average"]
)

bowl["strike_rate_score"] = inverse_score(
    bowl["strike_rate"]
)

bowl["dot_ball_score"] = min_max_score(
    bowl["dot_balls"]
)

bowl["death_wicket_score"] = min_max_score(
    bowl["death_wickets"]
)

bowl["hauls_score"] = min_max_score(
    bowl["four_wicket_hauls"]
    + bowl["five_wicket_hauls"]
)


# ------------------------------------------------------------
# Bowling Impact Formula
# ------------------------------------------------------------
#
# Wickets             = 30%
# Economy             = 20%
# Bowling Average     = 15%
# Bowling Strike Rate = 10%
# Dot Balls           = 10%
# Death Wickets       = 10%
# 4/5 wicket hauls    = 5%
#
# Total               = 100%
# ------------------------------------------------------------

bowl["bowling_impact"] = (
    bowl["wickets_score"] * 0.30
    + bowl["economy_score"] * 0.20
    + bowl["bowling_average_score"] * 0.15
    + bowl["strike_rate_score"] * 0.10
    + bowl["dot_ball_score"] * 0.10
    + bowl["death_wicket_score"] * 0.10
    + bowl["hauls_score"] * 0.05
)


# ============================================================
# SELECT IMPORTANT COLUMNS
# ============================================================

bat_result = bat[
    [
        "batter",
        "matches",
        "runs",
        "strike_rate",
        "average",
        "fifties",
        "hundreds",
        "sixes",
        "batting_impact"
    ]
].copy()

bat_result.rename(
    columns={"batter": "player"},
    inplace=True
)


bowl_result = bowl[
    [
        "bowler",
        "matches",
        "wickets",
        "economy",
        "bowling_average",
        "strike_rate",
        "dot_balls",
        "death_wickets",
        "four_wicket_hauls",
        "five_wicket_hauls",
        "bowling_impact"
    ]
].copy()

bowl_result.rename(
    columns={"bowler": "player"},
    inplace=True
)


# ============================================================
# COMBINE BATTERS + BOWLERS
# ============================================================

all_players = pd.concat(
    [
        bat_result[["player", "matches"]],
        bowl_result[["player", "matches"]]
    ],
    ignore_index=True
)

# Keep maximum matches if player appears in both datasets

all_players = (
    all_players
    .groupby("player", as_index=False)["matches"]
    .max()
)


# ============================================================
# MERGE BATTING AND BOWLING
# ============================================================

impact = all_players.merge(
    bat_result,
    on=["player", "matches"],
    how="left"
)

impact = impact.merge(
    bowl_result,
    on=["player", "matches"],
    how="left",
    suffixes=("_bat", "_bowl")
)


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

impact["batting_impact"] = (
    impact["batting_impact"]
    .fillna(0)
)

impact["bowling_impact"] = (
    impact["bowling_impact"]
    .fillna(0)
)


# ============================================================
# DETERMINE PLAYER ROLE
# ============================================================

def determine_role(row):

    has_batting = row["batting_impact"] > 0
    has_bowling = row["bowling_impact"] > 0

    if has_batting and has_bowling:
        return "All-Rounder"

    elif has_batting:
        return "Batter"

    elif has_bowling:
        return "Bowler"

    return "Unknown"


impact["role"] = impact.apply(
    determine_role,
    axis=1
)


# ============================================================
# OVERALL PLAYER IMPACT
# ============================================================

def calculate_overall_impact(row):

    role = row["role"]

    batting_score = row["batting_impact"]
    bowling_score = row["bowling_impact"]

    if role == "Batter":

        return batting_score

    elif role == "Bowler":

        return bowling_score

    elif role == "All-Rounder":

        # Equal contribution from batting and bowling

        return (
            batting_score * 0.50
            + bowling_score * 0.50
        )

    return 0


impact["overall_impact"] = impact.apply(
    calculate_overall_impact,
    axis=1
)


# ============================================================
# EXPERIENCE / MATCH FACTOR
# ============================================================

# Players with more matches have a larger sample.
#
# This factor is intentionally small so that experience
# does not dominate actual performance.

impact["experience_factor"] = np.log1p(
    impact["matches"]
)

impact["experience_score"] = min_max_score(
    impact["experience_factor"]
)


# ============================================================
# FINAL PLAYER IMPACT SCORE
# ============================================================

impact["player_impact_score"] = (
    impact["overall_impact"] * 0.90
    + impact["experience_score"] * 0.10
)


# ============================================================
# ROUND SCORE
# ============================================================

impact["batting_impact"] = (
    impact["batting_impact"].round(2)
)

impact["bowling_impact"] = (
    impact["bowling_impact"].round(2)
)

impact["overall_impact"] = (
    impact["overall_impact"].round(2)
)

impact["experience_score"] = (
    impact["experience_score"].round(2)
)

impact["player_impact_score"] = (
    impact["player_impact_score"].round(2)
)


# ============================================================
# RANK PLAYERS
# ============================================================

impact = impact.sort_values(
    by="player_impact_score",
    ascending=False
)

impact["impact_rank"] = range(
    1,
    len(impact) + 1
)


# ============================================================
# SELECT FINAL COLUMNS
# ============================================================

final_columns = [
    "impact_rank",
    "player",
    "role",
    "matches",
    "batting_impact",
    "bowling_impact",
    "overall_impact",
    "experience_score",
    "player_impact_score"
]

impact = impact[final_columns]


# ============================================================
# SAVE FILE
# ============================================================

impact.to_csv(
    output_file,
    index=False
)


# ============================================================
# DISPLAY TOP PLAYERS
# ============================================================

print("\n" + "=" * 60)
print("TOP RCB PLAYERS BY IMPACT")
print("=" * 60)

print(
    impact.head(20).to_string(index=False)
)


# ============================================================
# ROLE SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ROLE SUMMARY")
print("=" * 60)

print(
    impact["role"].value_counts()
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

print(f"Total players        : {len(impact)}")
print(
    f"Average impact score : "
    f"{impact['player_impact_score'].mean():.2f}"
)

print(
    f"Highest impact score : "
    f"{impact['player_impact_score'].max():.2f}"
)

print(
    f"Top player           : "
    f"{impact.iloc[0]['player']}"
)

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)

print("Saved to:")
print(output_file)