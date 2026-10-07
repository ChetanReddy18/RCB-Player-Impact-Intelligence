import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

input_file = Path(
    "data/processed/ipl_deliveries_cleaned.csv"
)

opponent_output = Path(
    "data/processed/rcb_opponent_analysis.csv"
)

venue_output = Path(
    "data/processed/rcb_venue_analysis.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    input_file,
    low_memory=False
)

print("=" * 70)
print("RCB OPPONENT & VENUE ANALYSIS")
print("=" * 70)

print(
    f"Total IPL deliveries : {len(df)}"
)


# ============================================================
# RCB TEAM NAMES
# ============================================================

rcb_names = [
    "Royal Challengers Bangalore",
    "Royal Challengers Bengaluru"
]


# ============================================================
# HISTORICAL TEAM NAME MAPPING
# ============================================================

opponent_mapping = {

    "Delhi Daredevils":
        "Delhi Capitals",

    "Kings XI Punjab":
        "Punjab Kings",

    "Rising Pune Supergiants":
        "Rising Pune Supergiant",

    "Rising Pune Supergiant":
        "Rising Pune Supergiant",

    "Royal Challengers Bangalore":
        "Royal Challengers Bangalore",

    "Royal Challengers Bengaluru":
        "Royal Challengers Bangalore"
}


# ============================================================
# GET RCB BATTING DELIVERIES
# ============================================================

rcb_batting = df[
    df["team"].isin(rcb_names)
].copy()


# ============================================================
# GET RCB MATCH IDS
# ============================================================

rcb_match_ids = (
    rcb_batting["match_id"]
    .dropna()
    .unique()
)


print(
    f"RCB matches found     : {len(rcb_match_ids)}"
)


# ============================================================
# NORMALIZE OPPONENT
# ============================================================

rcb_batting["opponent_normalized"] = (
    rcb_batting["opponent"]
    .replace(opponent_mapping)
)


# ============================================================
# GET ONE ROW PER RCB MATCH
# ============================================================

match_info = (
    rcb_batting
    .sort_values(
        [
            "match_id",
            "innings",
            "over",
            "delivery"
        ]
    )
    .groupby(
        "match_id",
        as_index=False
    )
    .first()
)


# ============================================================
# MATCH RESULT
# ============================================================

def get_result(row):

    winner = row["winner"]

    if pd.isna(winner):
        return "No Result"

    winner = str(winner).strip()

    if winner == "":
        return "No Result"

    if winner in rcb_names:
        return "Win"

    return "Loss"


match_info["result"] = (
    match_info.apply(
        get_result,
        axis=1
    )
)


# ============================================================
# OPPONENT ANALYSIS
# ============================================================

print("\nCalculating opponent analysis...")


opponent_analysis = (
    match_info
    .groupby(
        "opponent_normalized"
    )
    .agg(

        matches=(
            "match_id",
            "nunique"
        ),

        wins=(
            "result",
            lambda x:
            (x == "Win").sum()
        ),

        losses=(
            "result",
            lambda x:
            (x == "Loss").sum()
        ),

        no_results=(
            "result",
            lambda x:
            (x == "No Result").sum()
        )
    )
    .reset_index()
)


# ============================================================
# DECIDED MATCHES
# ============================================================

opponent_analysis["decided_matches"] = (
    opponent_analysis["wins"]
    + opponent_analysis["losses"]
)


# ============================================================
# WIN PERCENTAGE
# ============================================================

opponent_analysis["win_percentage"] = np.where(

    opponent_analysis["decided_matches"] > 0,

    (
        opponent_analysis["wins"]
        /
        opponent_analysis["decided_matches"]
        * 100
    ),

    0
)


# ============================================================
# RUNS SCORED AGAINST EACH OPPONENT
# ============================================================

runs_by_opponent = (
    rcb_batting
    .groupby(
        "opponent_normalized"
    )["batter_runs"]
    .sum()
    .reset_index()
)


runs_by_opponent.rename(
    columns={
        "batter_runs":
        "runs_scored"
    },
    inplace=True
)


# ============================================================
# RCB BOWLING DELIVERIES
# ============================================================

# IMPORTANT:
#
# RCB bowling happens when the OTHER team is batting.
#
# Therefore:
#
# match_id belongs to an RCB match
# AND
# team is NOT RCB
#
# This is different from rcb_batting.

rcb_bowling = df[
    (
        df["match_id"]
        .isin(rcb_match_ids)
    )
    &
    (
        ~df["team"]
        .isin(rcb_names)
    )
].copy()


print(
    f"RCB bowling deliveries : "
    f"{len(rcb_bowling)}"
)


# ============================================================
# OPPONENT FOR RCB BOWLING
# ============================================================

# When RCB is bowling,
# the batting team is the opponent.

rcb_bowling["opponent_normalized"] = (
    rcb_bowling["team"]
    .replace(opponent_mapping)
)


# ============================================================
# VALID BOWLER WICKETS
# ============================================================

valid_wicket_kinds = [

    "bowled",

    "caught",

    "caught and bowled",

    "lbw",

    "stumped",

    "hit wicket"
]


rcb_bowling["bowler_wicket"] = (

    rcb_bowling["wicket_kind"]
    .isin(valid_wicket_kinds)
    .astype(int)

)


# ============================================================
# WICKETS AGAINST EACH OPPONENT
# ============================================================

wickets_by_opponent = (
    rcb_bowling
    .groupby(
        "opponent_normalized"
    )["bowler_wicket"]
    .sum()
    .reset_index()
)


wickets_by_opponent.rename(
    columns={
        "bowler_wicket":
        "wickets_taken"
    },
    inplace=True
)


# ============================================================
# MERGE OPPONENT METRICS
# ============================================================

opponent_analysis = (
    opponent_analysis
    .merge(
        runs_by_opponent,
        on="opponent_normalized",
        how="left"
    )
)


opponent_analysis = (
    opponent_analysis
    .merge(
        wickets_by_opponent,
        on="opponent_normalized",
        how="left"
    )
)


# ============================================================
# FILL MISSING VALUES
# ============================================================

opponent_analysis[
    "runs_scored"
] = (
    opponent_analysis[
        "runs_scored"
    ]
    .fillna(0)
)


opponent_analysis[
    "wickets_taken"
] = (
    opponent_analysis[
        "wickets_taken"
    ]
    .fillna(0)
)


# ============================================================
# AVERAGE RUNS PER MATCH
# ============================================================

opponent_analysis[
    "avg_runs_per_match"
] = np.where(

    opponent_analysis["matches"] > 0,

    opponent_analysis["runs_scored"]
    /
    opponent_analysis["matches"],

    0
)


# ============================================================
# ROUND VALUES
# ============================================================

opponent_analysis[
    "win_percentage"
] = (
    opponent_analysis[
        "win_percentage"
    ]
    .round(2)
)


opponent_analysis[
    "avg_runs_per_match"
] = (
    opponent_analysis[
        "avg_runs_per_match"
    ]
    .round(2)
)


# ============================================================
# SORT OPPONENTS
# ============================================================

opponent_analysis = (
    opponent_analysis
    .sort_values(
        by="matches",
        ascending=False
    )
)


# ============================================================
# SAVE OPPONENT ANALYSIS
# ============================================================

opponent_analysis.to_csv(
    opponent_output,
    index=False
)


# ============================================================
# DISPLAY OPPONENT ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RCB PERFORMANCE AGAINST OPPONENTS")
print("=" * 70)

print(
    opponent_analysis
    .to_string(index=False)
)


# ============================================================
# VENUE ANALYSIS
# ============================================================

print("\nCalculating venue analysis...")


venue_analysis = (
    match_info
    .groupby(
        [
            "venue",
            "city"
        ],
        dropna=False
    )
    .agg(

        matches=(
            "match_id",
            "nunique"
        ),

        wins=(
            "result",
            lambda x:
            (x == "Win").sum()
        ),

        losses=(
            "result",
            lambda x:
            (x == "Loss").sum()
        ),

        no_results=(
            "result",
            lambda x:
            (x == "No Result").sum()
        )
    )
    .reset_index()
)


# ============================================================
# VENUE DECIDED MATCHES
# ============================================================

venue_analysis[
    "decided_matches"
] = (
    venue_analysis["wins"]
    +
    venue_analysis["losses"]
)


# ============================================================
# VENUE WIN %
# ============================================================

venue_analysis[
    "win_percentage"
] = np.where(

    venue_analysis[
        "decided_matches"
    ] > 0,

    (
        venue_analysis["wins"]
        /
        venue_analysis[
            "decided_matches"
        ]
        * 100
    ),

    0
)


# ============================================================
# RUNS SCORED BY VENUE
# ============================================================

runs_by_venue = (
    rcb_batting
    .groupby(
        [
            "venue",
            "city"
        ],
        dropna=False
    )["batter_runs"]
    .sum()
    .reset_index()
)


runs_by_venue.rename(
    columns={
        "batter_runs":
        "runs_scored"
    },
    inplace=True
)


# ============================================================
# WICKETS TAKEN BY VENUE
# ============================================================

wickets_by_venue = (
    rcb_bowling
    .groupby(
        [
            "venue",
            "city"
        ],
        dropna=False
    )["bowler_wicket"]
    .sum()
    .reset_index()
)


wickets_by_venue.rename(
    columns={
        "bowler_wicket":
        "wickets_taken"
    },
    inplace=True
)


# ============================================================
# MERGE VENUE RUNS
# ============================================================

venue_analysis = (
    venue_analysis
    .merge(
        runs_by_venue,
        on=[
            "venue",
            "city"
        ],
        how="left"
    )
)


# ============================================================
# MERGE VENUE WICKETS
# ============================================================

venue_analysis = (
    venue_analysis
    .merge(
        wickets_by_venue,
        on=[
            "venue",
            "city"
        ],
        how="left"
    )
)


# ============================================================
# FILL MISSING VALUES
# ============================================================

venue_analysis[
    "runs_scored"
] = (
    venue_analysis[
        "runs_scored"
    ]
    .fillna(0)
)


venue_analysis[
    "wickets_taken"
] = (
    venue_analysis[
        "wickets_taken"
    ]
    .fillna(0)
)


# ============================================================
# AVERAGE RUNS PER MATCH
# ============================================================

venue_analysis[
    "avg_runs_per_match"
] = np.where(

    venue_analysis["matches"] > 0,

    venue_analysis["runs_scored"]
    /
    venue_analysis["matches"],

    0
)


# ============================================================
# ROUND VALUES
# ============================================================

venue_analysis[
    "win_percentage"
] = (
    venue_analysis[
        "win_percentage"
    ]
    .round(2)
)


venue_analysis[
    "avg_runs_per_match"
] = (
    venue_analysis[
        "avg_runs_per_match"
    ]
    .round(2)
)


# ============================================================
# SORT VENUES
# ============================================================

venue_analysis = (
    venue_analysis
    .sort_values(
        by="matches",
        ascending=False
    )
)


# ============================================================
# SAVE VENUE ANALYSIS
# ============================================================

venue_analysis.to_csv(
    venue_output,
    index=False
)


# ============================================================
# DISPLAY VENUE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("RCB VENUE PERFORMANCE")
print("=" * 70)

print(
    venue_analysis
    .to_string(index=False)
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)

print(
    "RCB bowling deliveries :",
    len(rcb_bowling)
)

print(
    "Total RCB wickets      :",
    int(
        rcb_bowling[
            "bowler_wicket"
        ].sum()
    )
)

print(
    "Opponent rows          :",
    len(opponent_analysis)
)

print(
    "Venue rows             :",
    len(venue_analysis)
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    f"Opponents analyzed : "
    f"{len(opponent_analysis)}"
)

print(
    f"Venues analyzed    : "
    f"{len(venue_analysis)}"
)

print(
    f"Total RCB matches  : "
    f"{len(match_info)}"
)


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print("Opponent file:")
print(opponent_output)

print("\nVenue file:")
print(venue_output)