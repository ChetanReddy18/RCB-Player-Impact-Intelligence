import pandas as pd
import numpy as np
import os

print("=" * 60)
print("RCB OPPONENT SEASON ANALYSIS")
print("=" * 60)


# =========================================================
# FILE PATH
# =========================================================

input_file = "data/final/rcb_match_master.csv"

output_file = "data/final/rcb_opponent_season_master.csv"


# =========================================================
# LOAD DATA
# =========================================================

print("\nLoading RCB match data...")

df = pd.read_csv(input_file)

print("Rows:", len(df))

print("\nColumns:")
print(df.columns.tolist())


# =========================================================
# STANDARDIZE COLUMN NAMES
# =========================================================

df.columns = [
    str(col).strip().lower()
    for col in df.columns
]


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

print("\nUsing columns:")

for col in df.columns:
    print("-", col)


# =========================================================
# NORMALIZE OPPONENT NAMES
# =========================================================

if "opponent" not in df.columns:

    print("\nERROR: opponent column not found.")

    raise SystemExit


df["opponent"] = df["opponent"].astype(str).str.strip()


df["opponent"] = df["opponent"].replace({

    "Delhi Daredevils":
        "Delhi Capitals",

    "Kings XI Punjab":
        "Punjab Kings",

    "Rising Pune Supergiants":
        "Rising Pune Supergiant",

    "Rising Pune Supergiants ":
        "Rising Pune Supergiant"

})


# =========================================================
# FIND RESULT COLUMN
# =========================================================

result_column = None

possible_result_columns = [
    "result",
    "outcome",
    "match_result",
    "winner"
]


for col in possible_result_columns:

    if col in df.columns:

        result_column = col
        break


print("\nResult column:", result_column)


# =========================================================
# CREATE WIN / LOSS / NO RESULT
# =========================================================

if result_column is None:

    print(
        "\nERROR: Could not find a result/winner column."
    )

    print(
        "Available columns:",
        df.columns.tolist()
    )

    raise SystemExit


df[result_column] = (
    df[result_column]
    .astype(str)
    .str.strip()
)


# =========================================================
# CREATE RESULT FLAGS
# =========================================================

# Handle datasets where result column contains
# Win / Loss / No Result

df["wins"] = np.where(
    df[result_column].str.lower() == "win",
    1,
    0
)


df["losses"] = np.where(
    df[result_column].str.lower() == "loss",
    1,
    0
)


df["no_results"] = np.where(
    df[result_column].str.lower().isin(
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
# IF RESULT COLUMN IS WINNER COLUMN
# =========================================================

winner_values = (
    df[result_column]
    .dropna()
    .astype(str)
    .str.lower()
    .unique()
)


if not any(
    value in ["win", "loss", "no result", "nr"]
    for value in winner_values
):

    print(
        "\nResult column appears to contain winner names."
    )

    # RCB historical names
    rcb_names = [
        "royal challengers bangalore",
        "royal challengers bengaluru",
        "rcb"
    ]

    df["wins"] = np.where(
        df[result_column]
        .astype(str)
        .str.lower()
        .isin(rcb_names),
        1,
        0
    )

    df["no_results"] = np.where(
        df[result_column]
        .astype(str)
        .str.lower()
        .isin(
            [
                "no result",
                "no_result",
                "nr",
                "nan"
            ]
        ),
        1,
        0
    )

    df["losses"] = np.where(
        (
            df["wins"] == 0
        )
        &
        (
            df["no_results"] == 0
        ),
        1,
        0
    )


# =========================================================
# SEASON + OPPONENT AGGREGATION
# =========================================================

print("\nCreating season-wise opponent data...")


result = (
    df.groupby(
        [
            "season",
            "opponent"
        ],
        as_index=False
    )
    .agg(
        matches=("opponent", "count"),
        wins=("wins", "sum"),
        losses=("losses", "sum"),
        no_results=("no_results", "sum")
    )
)


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


# =========================================================
# ROUND VALUES
# =========================================================

result["win_pct"] = result[
    "win_pct"
].round(2)


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
print("2026 OPPONENT ANALYSIS")
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
    "Unique opponents:",
    result["opponent"].nunique()
)


print(
    "Seasons:",
    result["season"].nunique()
)


print("\nSaved to:")

print(output_file)


print("=" * 60)