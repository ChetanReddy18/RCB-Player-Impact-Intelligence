import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# FILE PATHS
# ============================================================

financial_file = Path(
    "data/raw/rcb_financial_data.csv"
)

impact_file = Path(
    "data/processed/rcb_player_impact.csv"
)

batting_file = Path(
    "data/processed/rcb_batting_metrics.csv"
)

bowling_file = Path(
    "data/processed/rcb_bowling_metrics.csv"
)

cleaned_file = Path(
    "data/processed/ipl_deliveries_cleaned.csv"
)

output_file = Path(
    "data/processed/rcb_financial_analysis.csv"
)

season_output_file = Path(
    "data/processed/rcb_player_season_finance.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("RCB SALARY & AUCTION ANALYSIS")
print("=" * 70)

financial = pd.read_csv(
    financial_file,
    low_memory=False
)

impact = pd.read_csv(
    impact_file,
    low_memory=False
)

batting = pd.read_csv(
    batting_file,
    low_memory=False
)

bowling = pd.read_csv(
    bowling_file,
    low_memory=False
)

cleaned = pd.read_csv(
    cleaned_file,
    low_memory=False
)


print(
    f"Financial records : {len(financial)}"
)

print(
    f"Impact players    : {len(impact)}"
)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

for dataframe in [
    financial,
    impact,
    batting,
    bowling,
    cleaned
]:

    dataframe.columns = (
        dataframe.columns
        .str.strip()
        .str.lower()
    )


# ============================================================
# PLAYER NAME STANDARDIZATION
# ============================================================

player_name_mapping = {

    # Batters
    "Virat Kohli": "V Kohli",
    "Virat": "V Kohli",

    "Chris Gayle": "CH Gayle",

    "Faf du Plessis": "F du Plessis",
    "Faf Du Plessis": "F du Plessis",

    "Glenn Maxwell": "GJ Maxwell",

    "Dinesh Karthik": "KD Karthik",

    "Rahul Dravid": "R Dravid",

    "Jacques Kallis": "JH Kallis",

    "Cameron White": "CL White",

    "Mark Boucher": "MV Boucher",

    "Ross Taylor": "LRPL Taylor",

    "Shivnarine Chanderpaul": "S Chanderpaul",

    # Bowlers
    "Anil Kumble": "A Kumble",

    "Zaheer Khan": "Z Khan",

    "Dale Steyn": "DW Steyn",

    "Praveen Kumar": "P Kumar",

    "Vinay Kumar": "R Vinay Kumar",

    "Harshal Patel": "HV Patel",

    "Sreenath Aravind": "S Aravind",

    "Mohammed Siraj": "Mohammed Siraj",

    "Yash Dayal": "Yash Dayal",

    # Other
    "Misbah Ul Haq": "Misbah-ul-Haq",
    "Misbah-ul-Haq": "Misbah-ul-Haq"
}


def standardize_player_name(series):

    return (
        series
        .astype(str)
        .str.strip()
        .replace(player_name_mapping)
    )


financial["player"] = standardize_player_name(
    financial["player"]
)

impact["player"] = standardize_player_name(
    impact["player"]
)

batting["player"] = standardize_player_name(
    batting["batter"]
)

bowling["player"] = standardize_player_name(
    bowling["bowler"]
)


# ============================================================
# CLEAN FINANCIAL DATA
# ============================================================

financial["price_crore"] = pd.to_numeric(
    financial["price_crore"],
    errors="coerce"
)

financial["season"] = (
    financial["season"]
    .astype(str)
    .str.strip()
)

financial["transaction_type"] = (
    financial["transaction_type"]
    .astype(str)
    .str.strip()
)

financial = financial[
    financial["price_crore"].notna()
    &
    (financial["price_crore"] > 0)
].copy()


# ============================================================
# PLAYER CAREER PERFORMANCE
# ============================================================

career_batting = batting[
    [
        "player",
        "matches",
        "runs"
    ]
].copy()


career_batting = (
    career_batting
    .groupby("player", as_index=False)
    .agg(
        batting_matches=("matches", "max"),
        career_runs=("runs", "max")
    )
)


career_bowling = bowling[
    [
        "player",
        "matches",
        "wickets"
    ]
].copy()


career_bowling = (
    career_bowling
    .groupby("player", as_index=False)
    .agg(
        bowling_matches=("matches", "max"),
        career_wickets=("wickets", "max")
    )
)


# ============================================================
# CAREER FINANCIAL SUMMARY
# ============================================================

career_finance = (
    financial
    .groupby("player", as_index=False)
    .agg(

        financial_seasons=(
            "season",
            "nunique"
        ),

        total_recorded_investment_crore=(
            "price_crore",
            "sum"
        ),

        average_recorded_price_crore=(
            "price_crore",
            "mean"
        ),

        highest_recorded_price_crore=(
            "price_crore",
            "max"
        )
    )
)


# ============================================================
# MERGE CAREER INFORMATION
# ============================================================

career_analysis = (
    career_finance
    .merge(
        impact[
            [
                "player",
                "role",
                "matches",
                "player_impact_score"
            ]
        ],
        on="player",
        how="left"
    )
)


career_analysis = (
    career_analysis
    .merge(
        career_batting,
        on="player",
        how="left"
    )
)


career_analysis = (
    career_analysis
    .merge(
        career_bowling,
        on="player",
        how="left"
    )
)


# ============================================================
# CAREER EFFICIENCY
# ============================================================

career_analysis[
    "impact_per_recorded_crore"
] = np.where(

    career_analysis[
        "total_recorded_investment_crore"
    ] > 0,

    career_analysis[
        "player_impact_score"
    ]
    /
    career_analysis[
        "total_recorded_investment_crore"
    ],

    np.nan
)


career_analysis[
    "runs_per_recorded_crore"
] = np.where(

    career_analysis[
        "total_recorded_investment_crore"
    ] > 0,

    career_analysis[
        "career_runs"
    ]
    /
    career_analysis[
        "total_recorded_investment_crore"
    ],

    np.nan
)


career_analysis[
    "wickets_per_recorded_crore"
] = np.where(

    career_analysis[
        "total_recorded_investment_crore"
    ] > 0,

    career_analysis[
        "career_wickets"
    ]
    /
    career_analysis[
        "total_recorded_investment_crore"
    ],

    np.nan
)


# ============================================================
# ROUND CAREER VALUES
# ============================================================

career_numeric_columns = [

    "total_recorded_investment_crore",

    "average_recorded_price_crore",

    "highest_recorded_price_crore",

    "player_impact_score",

    "impact_per_recorded_crore",

    "runs_per_recorded_crore",

    "wickets_per_recorded_crore"
]


for column in career_numeric_columns:

    if column in career_analysis.columns:

        career_analysis[column] = (
            career_analysis[column]
            .round(2)
        )


# ============================================================
# SORT
# ============================================================

career_analysis = career_analysis.sort_values(
    by="impact_per_recorded_crore",
    ascending=False,
    na_position="last"
)


# ============================================================
# SEASON-LEVEL PERFORMANCE
# ============================================================

print("\nCalculating player-season performance...")


# RCB batting data from cleaned deliveries

rcb_cleaned = cleaned[
    cleaned["team"].isin(
        [
            "Royal Challengers Bangalore",
            "Royal Challengers Bengaluru"
        ]
    )
].copy()


rcb_cleaned["player"] = standardize_player_name(
    rcb_cleaned["batter"]
)


# ------------------------------------------------------------
# Batting season totals
# ------------------------------------------------------------

season_batting = (
    rcb_cleaned
    .groupby(
        [
            "season",
            "player"
        ],
        as_index=False
    )
    .agg(
        runs=("batter_runs", "sum"),
        batting_matches=("match_id", "nunique")
    )
)


# ============================================================
# RCB BOWLING SEASON DATA
# ============================================================

rcb_match_ids = (
    rcb_cleaned["match_id"]
    .dropna()
    .unique()
)


rcb_bowling = cleaned[
    (
        cleaned["match_id"]
        .isin(rcb_match_ids)
    )
    &
    (
        ~cleaned["team"].isin(
            [
                "Royal Challengers Bangalore",
                "Royal Challengers Bengaluru"
            ]
        )
    )
].copy()


rcb_bowling["player"] = standardize_player_name(
    rcb_bowling["bowler"]
)


# ------------------------------------------------------------
# Valid bowler wickets
# ------------------------------------------------------------

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


season_bowling = (
    rcb_bowling
    .groupby(
        [
            "season",
            "player"
        ],
        as_index=False
    )
    .agg(
        wickets=("bowler_wicket", "sum"),
        bowling_matches=("match_id", "nunique")
    )
)


# ============================================================
# COMBINE SEASON PERFORMANCE
# ============================================================

season_performance = (
    season_batting
    .merge(
        season_bowling,
        on=[
            "season",
            "player"
        ],
        how="outer"
    )
)


season_performance["runs"] = (
    season_performance["runs"]
    .fillna(0)
)


season_performance["wickets"] = (
    season_performance["wickets"]
    .fillna(0)
)


season_performance["batting_matches"] = (
    season_performance["batting_matches"]
    .fillna(0)
)


season_performance["bowling_matches"] = (
    season_performance["bowling_matches"]
    .fillna(0)
)


season_performance["matches"] = (
    season_performance[
        [
            "batting_matches",
            "bowling_matches"
        ]
    ]
    .max(axis=1)
)


# ============================================================
# MERGE FINANCIAL DATA WITH SEASON PERFORMANCE
# ============================================================

season_analysis = financial.merge(

    season_performance,

    on=[
        "season",
        "player"
    ],

    how="left"
)


# ============================================================
# MERGE OVERALL PLAYER IMPACT
# ============================================================

season_analysis = season_analysis.merge(

    impact[
        [
            "player",
            "role",
            "player_impact_score"
        ]
    ],

    on="player",

    how="left"
)


# ============================================================
# IMPORTANT NOTE:
# player_impact_score IS CAREER LEVEL.
#
# We do NOT use it as a season-level impact score.
# Instead, we calculate simple season performance measures.
# ============================================================


season_analysis[
    "runs_per_crore"
] = np.where(

    season_analysis["price_crore"] > 0,

    season_analysis["runs"]
    /
    season_analysis["price_crore"],

    np.nan
)


season_analysis[
    "wickets_per_crore"
] = np.where(

    season_analysis["price_crore"] > 0,

    season_analysis["wickets"]
    /
    season_analysis["price_crore"],

    np.nan
)


# ============================================================
# SIMPLE SEASON PRODUCTION INDEX
# ============================================================

# This is NOT an official IPL rating.
#
# It is only a simple project metric based on:
#
# runs / 100
# wickets * 5
#
# It should be used as a descriptive production index.

season_analysis[
    "season_production_index"
] = (

    season_analysis["runs"] / 100

    +

    season_analysis["wickets"] * 5
)


season_analysis[
    "production_per_crore"
] = np.where(

    season_analysis["price_crore"] > 0,

    season_analysis[
        "season_production_index"
    ]
    /
    season_analysis["price_crore"],

    np.nan
)


# ============================================================
# ROUND SEASON VALUES
# ============================================================

season_numeric_columns = [

    "price_crore",

    "runs",

    "wickets",

    "runs_per_crore",

    "wickets_per_crore",

    "season_production_index",

    "production_per_crore"
]


for column in season_numeric_columns:

    if column in season_analysis.columns:

        season_analysis[column] = (
            season_analysis[column]
            .round(2)
        )


# ============================================================
# SORT SEASON DATA
# ============================================================

season_analysis = season_analysis.sort_values(

    [
        "season",
        "production_per_crore"
    ],

    ascending=[
        True,
        False
    ],

    na_position="last"
)


# ============================================================
# SAVE CAREER ANALYSIS
# ============================================================

career_analysis.to_csv(
    output_file,
    index=False
)


# ============================================================
# SAVE SEASON ANALYSIS
# ============================================================

season_analysis.to_csv(
    season_output_file,
    index=False
)


# ============================================================
# DISPLAY CAREER ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("CAREER INVESTMENT & IMPACT")
print("=" * 70)


career_display = [

    "player",

    "role",

    "financial_seasons",

    "total_recorded_investment_crore",

    "average_recorded_price_crore",

    "highest_recorded_price_crore",

    "player_impact_score",

    "impact_per_recorded_crore",

    "career_runs",

    "career_wickets"
]


print(
    career_analysis[
        career_display
    ]
    .head(20)
    .to_string(index=False)
)


# ============================================================
# DISPLAY SEASON ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("PLAYER-SEASON INVESTMENT & PERFORMANCE")
print("=" * 70)


season_display = [

    "season",

    "player",

    "transaction_type",

    "price_crore",

    "runs",

    "wickets",

    "runs_per_crore",

    "wickets_per_crore",

    "season_production_index",

    "production_per_crore"
]


print(
    season_analysis[
        season_display
    ]
    .head(30)
    .to_string(index=False)
)


# ============================================================
# MATCHING SUMMARY
# ============================================================

financial_players = set(
    financial["player"]
)

impact_players = set(
    impact["player"]
)

matched_players = (
    financial_players
    &
    impact_players
)

unmatched_players = (
    financial_players
    -
    impact_players
)


print("\n" + "=" * 70)
print("MATCHING SUMMARY")
print("=" * 70)


print(
    f"Financial players : "
    f"{len(financial_players)}"
)

print(
    f"Impact players    : "
    f"{len(impact_players)}"
)

print(
    f"Matched players   : "
    f"{len(matched_players)}"
)

print(
    f"Unmatched players : "
    f"{len(unmatched_players)}"
)


if unmatched_players:

    print("\nUnmatched financial players:")

    for player in sorted(
        unmatched_players
    ):

        print(
            f" - {player}"
        )


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)


print(
    f"Financial records : "
    f"{len(financial)}"
)


print(
    f"Career records    : "
    f"{len(career_analysis)}"
)


print(
    f"Season records    : "
    f"{len(season_analysis)}"
)


print(
    f"Total recorded investment : "
    f"{financial['price_crore'].sum():.2f} crore"
)


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)


print("Career analysis:")
print(output_file)


print("\nSeason analysis:")
print(season_output_file)