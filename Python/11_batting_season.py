import pandas as pd
import numpy as np
import os

# ---------------------------------------------------------
# 1. Load RCB batting delivery data
# ---------------------------------------------------------

input_file = "data/processed/rcb_deliveries.csv"

df = pd.read_csv(input_file)

print("Loaded rows:", len(df))


# ---------------------------------------------------------
# 2. Make sure boolean columns are actually boolean
# ---------------------------------------------------------

def to_bool(series):
    if series.dtype == bool:
        return series

    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map({
            "true": True,
            "false": False,
            "1": True,
            "0": False
        })
        .fillna(False)
    )


df["is_wide"] = to_bool(df["is_wide"])
df["is_noball"] = to_bool(df["is_noball"])


# ---------------------------------------------------------
# 3. Convert numeric columns
# ---------------------------------------------------------

df["batter_runs"] = pd.to_numeric(
    df["batter_runs"],
    errors="coerce"
).fillna(0)

df["total_runs"] = pd.to_numeric(
    df["total_runs"],
    errors="coerce"
).fillna(0)

df["wicket_count"] = pd.to_numeric(
    df["wicket_count"],
    errors="coerce"
).fillna(0)


# ---------------------------------------------------------
# 4. Ball faced
#    Wides and no-balls are not counted
# ---------------------------------------------------------

df["ball_faced"] = (
    (~df["is_wide"]) &
    (~df["is_noball"])
).astype(int)


# ---------------------------------------------------------
# 5. Create innings-level batting scores
# ---------------------------------------------------------

innings_scores = (
    df.groupby(
        ["season", "match_id", "innings", "batter"],
        as_index=False
    )
    .agg(
        innings_runs=("batter_runs", "sum"),
        balls=("ball_faced", "sum")
    )
)


# ---------------------------------------------------------
# 6. Calculate 50s and 100s
# ---------------------------------------------------------

innings_scores["fifty"] = (
    (innings_scores["innings_runs"] >= 50) &
    (innings_scores["innings_runs"] < 100)
).astype(int)

innings_scores["hundred"] = (
    (innings_scores["innings_runs"] >= 100)
).astype(int)


# ---------------------------------------------------------
# 7. Aggregate player-season batting statistics
# ---------------------------------------------------------

batting = (
    df.groupby(
        ["season", "batter"],
        as_index=False
    )
    .agg(
        matches=("match_id", "nunique"),
        runs=("batter_runs", "sum"),
        balls=("ball_faced", "sum"),
        fours=("batter_runs", lambda x: (x == 4).sum()),
        sixes=("batter_runs", lambda x: (x == 6).sum())
    )
)


# ---------------------------------------------------------
# 8. Add innings count
# ---------------------------------------------------------

innings_count = (
    innings_scores.groupby(
        ["season", "batter"],
        as_index=False
    )
    .agg(
        innings=("innings_runs", "count"),
        fifties=("fifty", "sum"),
        hundreds=("hundred", "sum")
    )
)

batting = batting.merge(
    innings_count,
    on=["season", "batter"],
    how="left"
)


# ---------------------------------------------------------
# 9. Calculate dismissals
# ---------------------------------------------------------

df["is_dismissed_batter"] = (
    df["player_out"].notna() &
    (df["player_out"] == df["batter"])
)

dismissals = (
    df[df["is_dismissed_batter"]]
    .groupby(
        ["season", "batter"],
        as_index=False
    )
    .size()
    .rename(columns={"size": "dismissals"})
)

batting = batting.merge(
    dismissals,
    on=["season", "batter"],
    how="left"
)

batting["dismissals"] = batting["dismissals"].fillna(0)


# ---------------------------------------------------------
# 10. Strike Rate
# ---------------------------------------------------------

batting["strike_rate"] = np.where(
    batting["balls"] > 0,
    (batting["runs"] / batting["balls"]) * 100,
    0
)


# ---------------------------------------------------------
# 11. Batting Average
# ---------------------------------------------------------

batting["average"] = np.where(
    batting["dismissals"] > 0,
    batting["runs"] / batting["dismissals"],
    batting["runs"]
)


# ---------------------------------------------------------
# 12. Clean column order
# ---------------------------------------------------------

batting = batting[
    [
        "season",
        "batter",
        "matches",
        "innings",
        "runs",
        "balls",
        "fours",
        "sixes",
        "fifties",
        "hundreds",
        "dismissals",
        "strike_rate",
        "average"
    ]
]


# ---------------------------------------------------------
# 13. Round decimal values
# ---------------------------------------------------------

batting["strike_rate"] = batting["strike_rate"].round(2)
batting["average"] = batting["average"].round(2)


# ---------------------------------------------------------
# 14. Sort
# ---------------------------------------------------------

batting = batting.sort_values(
    ["season", "runs"],
    ascending=[True, False]
)


# ---------------------------------------------------------
# 15. Save
# ---------------------------------------------------------

output_file = "data/final/rcb_batting_season_master.csv"

os.makedirs(
    os.path.dirname(output_file),
    exist_ok=True
)

batting.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# 16. Validation
# ---------------------------------------------------------

print("\n------------------------------------")
print("BATTTING SEASON MASTER CREATED")
print("------------------------------------")

print("Rows:", len(batting))

print("\nSeasons:")
print(batting["season"].unique())

print("\nTop 10 batters - 2026:")

print(
    batting[
        batting["season"] == "2026"
    ]
    .head(10)
    .to_string(index=False)
)

print("\nSaved to:")
print(output_file)