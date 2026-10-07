import pandas as pd
import numpy as np
import os

print("=" * 60)
print("RCB PLAYER SEASON IMPACT ANALYSIS")
print("=" * 60)


# =========================================================
# FILE PATHS
# =========================================================

batting_file = "data/final/rcb_batting_season_master.csv"
bowling_file = "data/final/rcb_bowling_season_master.csv"

output_file = "data/final/rcb_player_season_impact.csv"


# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading batting data...")
batting = pd.read_csv(batting_file)

print("Loading bowling data...")
bowling = pd.read_csv(bowling_file)

print("Batting rows:", len(batting))
print("Bowling rows:", len(bowling))


# =========================================================
# DISPLAY COLUMNS
# =========================================================

print("\nBatting columns:")
print(batting.columns.tolist())

print("\nBowling columns:")
print(bowling.columns.tolist())


# =========================================================
# STANDARDIZE PLAYER COLUMN
# =========================================================

if "player" not in batting.columns and "batter" in batting.columns:
    batting = batting.rename(
        columns={"batter": "player"}
    )

if "player" not in bowling.columns and "bowler" in bowling.columns:
    bowling = bowling.rename(
        columns={"bowler": "player"}
    )


# =========================================================
# BATTING IMPACT
# =========================================================

print("\nCalculating batting impact...")


# ---------------------------------------------------------
# RUNS - 30%
# ---------------------------------------------------------

batting["runs_score"] = batting.groupby(
    "season"
)["runs"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# STRIKE RATE - 20%
# ---------------------------------------------------------

batting["strike_rate_score"] = batting.groupby(
    "season"
)["strike_rate"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# BATTING AVERAGE - 20%
# Actual column = average
# ---------------------------------------------------------

batting["average_score"] = batting.groupby(
    "season"
)["average"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# FIFTIES - 10%
# ---------------------------------------------------------

batting["fifties_score"] = batting.groupby(
    "season"
)["fifties"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# HUNDREDS - 10%
# ---------------------------------------------------------

batting["hundreds_score"] = batting.groupby(
    "season"
)["hundreds"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# SIXES - 10%
# ---------------------------------------------------------

batting["sixes_score"] = batting.groupby(
    "season"
)["sixes"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------------

batting["runs_score"] = batting["runs_score"].fillna(0)
batting["strike_rate_score"] = batting["strike_rate_score"].fillna(0)
batting["average_score"] = batting["average_score"].fillna(0)
batting["fifties_score"] = batting["fifties_score"].fillna(0)
batting["hundreds_score"] = batting["hundreds_score"].fillna(0)
batting["sixes_score"] = batting["sixes_score"].fillna(0)


# ---------------------------------------------------------
# FINAL BATTING IMPACT
# ---------------------------------------------------------

batting["batting_impact"] = (
    batting["runs_score"] * 0.30
    + batting["strike_rate_score"] * 0.20
    + batting["average_score"] * 0.20
    + batting["fifties_score"] * 0.10
    + batting["hundreds_score"] * 0.10
    + batting["sixes_score"] * 0.10
) * 100


# =========================================================
# BOWLING IMPACT
# =========================================================

print("Calculating bowling impact...")


# ---------------------------------------------------------
# WICKETS - 30%
# ---------------------------------------------------------

bowling["wickets_score"] = bowling.groupby(
    "season"
)["wickets"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# ECONOMY - 20%
# LOWER IS BETTER
# ---------------------------------------------------------

bowling["economy_score"] = bowling.groupby(
    "season"
)["economy"].transform(
    lambda x: (-x).rank(pct=True)
)


# ---------------------------------------------------------
# BOWLING AVERAGE - 15%
# LOWER IS BETTER
# ---------------------------------------------------------

bowling["bowling_average_score"] = bowling.groupby(
    "season"
)["bowling_average"].transform(
    lambda x: (-x).rank(pct=True)
)


# ---------------------------------------------------------
# BOWLING STRIKE RATE - 10%
# LOWER IS BETTER
# ---------------------------------------------------------

bowling["bowling_sr_score"] = bowling.groupby(
    "season"
)["bowling_strike_rate"].transform(
    lambda x: (-x).rank(pct=True)
)


# ---------------------------------------------------------
# DOT BALLS - 10%
# ---------------------------------------------------------

bowling["dot_balls_score"] = bowling.groupby(
    "season"
)["dot_balls"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# DEATH WICKETS - 10%
# ---------------------------------------------------------

bowling["death_wickets_score"] = bowling.groupby(
    "season"
)["death_wickets"].transform(
    lambda x: x.rank(pct=True)
)


# ---------------------------------------------------------
# 4/5 WICKET HAULS
#
# The season bowling CSV does NOT contain this column.
# Therefore this component cannot be calculated directly
# from the current season master.
#
# We use 0 here and rescale the available 95% components
# to maintain a 0-100 impact scale.
# ---------------------------------------------------------

bowling["four_five_wickets_score"] = 0


# ---------------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------------

bowling["wickets_score"] = bowling["wickets_score"].fillna(0)
bowling["economy_score"] = bowling["economy_score"].fillna(0)
bowling["bowling_average_score"] = bowling[
    "bowling_average_score"
].fillna(0)

bowling["bowling_sr_score"] = bowling[
    "bowling_sr_score"
].fillna(0)

bowling["dot_balls_score"] = bowling[
    "dot_balls_score"
].fillna(0)

bowling["death_wickets_score"] = bowling[
    "death_wickets_score"
].fillna(0)


# ---------------------------------------------------------
# BOWLING IMPACT
#
# Available weights total = 95%
# We divide by 0.95 to rescale to 100.
# ---------------------------------------------------------

bowling["bowling_impact"] = (
    bowling["wickets_score"] * 0.30
    + bowling["economy_score"] * 0.20
    + bowling["bowling_average_score"] * 0.15
    + bowling["bowling_sr_score"] * 0.10
    + bowling["dot_balls_score"] * 0.10
    + bowling["death_wickets_score"] * 0.10
) / 0.95 * 100


# =========================================================
# CREATE PLAYER LIST
# =========================================================

print("Combining batting and bowling players...")


batting_players = batting[
    ["season", "player"]
].copy()


bowling_players = bowling[
    ["season", "player"]
].copy()


players = pd.concat(
    [
        batting_players,
        bowling_players
    ],
    ignore_index=True
).drop_duplicates()


# =========================================================
# MERGE BATTING IMPACT
# =========================================================

result = players.merge(
    batting[
        [
            "season",
            "player",
            "batting_impact"
        ]
    ],
    on=[
        "season",
        "player"
    ],
    how="left"
)


# =========================================================
# MERGE BOWLING IMPACT
# =========================================================

result = result.merge(
    bowling[
        [
            "season",
            "player",
            "bowling_impact"
        ]
    ],
    on=[
        "season",
        "player"
    ],
    how="left"
)


# =========================================================
# FILL MISSING IMPACT
# =========================================================

result["batting_impact"] = result[
    "batting_impact"
].fillna(0)


result["bowling_impact"] = result[
    "bowling_impact"
].fillna(0)


# =========================================================
# PLAYER ROLE
# =========================================================

result["role"] = np.select(
    [
        (
            (result["batting_impact"] > 0)
            &
            (result["bowling_impact"] > 0)
        ),

        result["batting_impact"] > 0,

        result["bowling_impact"] > 0
    ],

    [
        "All-Rounder",
        "Batter",
        "Bowler"
    ],

    default="Unknown"
)


# =========================================================
# OVERALL IMPACT
# =========================================================

result["overall_impact"] = np.where(

    (
        (result["batting_impact"] > 0)
        &
        (result["bowling_impact"] > 0)
    ),

    (
        result["batting_impact"]
        +
        result["bowling_impact"]
    ) / 2,

    np.maximum(
        result["batting_impact"],
        result["bowling_impact"]
    )
)


# =========================================================
# MATCHES
# =========================================================

print("Calculating player matches...")


# ---------------------------------------------------------
# BATTING MATCHES
# ---------------------------------------------------------

batting_matches = batting[
    [
        "season",
        "player",
        "matches"
    ]
].rename(
    columns={
        "matches": "batting_matches"
    }
)


# ---------------------------------------------------------
# BOWLING MATCHES
# ---------------------------------------------------------

bowling_matches = bowling[
    [
        "season",
        "player",
        "matches"
    ]
].rename(
    columns={
        "matches": "bowling_matches"
    }
)


# ---------------------------------------------------------
# MERGE BATTING MATCHES
# ---------------------------------------------------------

result = result.merge(
    batting_matches,
    on=[
        "season",
        "player"
    ],
    how="left"
)


# ---------------------------------------------------------
# MERGE BOWLING MATCHES
# ---------------------------------------------------------

result = result.merge(
    bowling_matches,
    on=[
        "season",
        "player"
    ],
    how="left"
)


# ---------------------------------------------------------
# FILL MISSING MATCHES
# ---------------------------------------------------------

result["batting_matches"] = result[
    "batting_matches"
].fillna(0)


result["bowling_matches"] = result[
    "bowling_matches"
].fillna(0)


# ---------------------------------------------------------
# PLAYER MATCHES
# ---------------------------------------------------------

result["matches"] = result[
    [
        "batting_matches",
        "bowling_matches"
    ]
].max(axis=1)


# =========================================================
# EXPERIENCE SCORE
# =========================================================

print("Calculating experience score...")


result["experience_score"] = np.log1p(
    result["matches"]
)


# Normalize experience within each season
result["experience_score"] = result.groupby(
    "season"
)["experience_score"].transform(
    lambda x:
        (
            x / x.max()
            if x.max() != 0
            else 0
        )
) * 100


# =========================================================
# FINAL PLAYER IMPACT SCORE
# =========================================================

print("Calculating final player impact score...")


result["player_impact_score"] = (
    result["overall_impact"] * 0.90
    +
    result["experience_score"] * 0.10
)


# =========================================================
# IMPACT RANK
# =========================================================

print("Ranking players within each season...")


result["impact_rank"] = result.groupby(
    "season"
)["player_impact_score"].rank(
    ascending=False,
    method="dense"
)


# =========================================================
# ROUND VALUES
# =========================================================

numeric_columns = [
    "batting_impact",
    "bowling_impact",
    "overall_impact",
    "experience_score",
    "player_impact_score"
]


for column in numeric_columns:

    result[column] = result[
        column
    ].round(2)


result["impact_rank"] = result[
    "impact_rank"
].astype(int)


# =========================================================
# SORT DATA
# =========================================================

result = result.sort_values(
    [
        "season",
        "impact_rank"
    ]
)


# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

os.makedirs(
    os.path.dirname(output_file),
    exist_ok=True
)


# =========================================================
# SAVE FILE
# =========================================================

result.to_csv(
    output_file,
    index=False
)


# =========================================================
# DISPLAY 2026 TOP 10
# =========================================================

print("\n" + "=" * 60)
print("2026 TOP 10 PLAYERS")
print("=" * 60)


top_2026 = result[
    result["season"].astype(str) == "2026"
].head(10)


print(
    top_2026[
        [
            "impact_rank",
            "player",
            "role",
            "matches",
            "batting_impact",
            "bowling_impact",
            "player_impact_score"
        ]
    ].to_string(index=False)
)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)


print(
    "Total rows:",
    len(result)
)


print(
    "Unique players:",
    result["player"].nunique()
)


print(
    "Total seasons:",
    result["season"].nunique()
)


print("\nOutput saved to:")

print(output_file)


print("=" * 60)