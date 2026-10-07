import pandas as pd
from pathlib import Path


# ============================================================
# STEP 10 - FINAL DATA EXPORT
# RCB IPL ANALYTICS PROJECT
# ============================================================

print("=" * 70)
print("STEP 10 - FINAL DATA EXPORT")
print("=" * 70)


# ------------------------------------------------------------
# 1. PATHS
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
FINAL_DIR = BASE_DIR / "data" / "final"

FINAL_DIR.mkdir(parents=True, exist_ok=True)

print("\nProcessed folder:")
print(PROCESSED_DIR)

print("\nFinal folder:")
print(FINAL_DIR)


# ------------------------------------------------------------
# 2. FUNCTION TO EXPORT CSV
# ------------------------------------------------------------

def export_csv(input_file, output_file):
    """
    Read a processed CSV, remove duplicate rows,
    clean column names and export to final folder.
    """

    input_path = PROCESSED_DIR / input_file
    output_path = FINAL_DIR / output_file

    if not input_path.exists():
        print(f"\nWARNING: File not found -> {input_file}")
        return None

    df = pd.read_csv(input_path, low_memory=False)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Save
    df.to_csv(output_path, index=False)

    print(
        f"\nExported: {output_file}"
        f"\nRows: {len(df):,}"
        f"\nDuplicates removed: {before - after}"
    )

    return df


# ------------------------------------------------------------
# 3. PLAYER MASTER
# ------------------------------------------------------------

player_master = export_csv(
    "rcb_player_impact.csv",
    "rcb_player_master.csv"
)


# ------------------------------------------------------------
# 4. BATTING MASTER
# ------------------------------------------------------------

batting_master = export_csv(
    "rcb_batting_metrics.csv",
    "rcb_batting_master.csv"
)


# ------------------------------------------------------------
# 5. BOWLING MASTER
# ------------------------------------------------------------

bowling_master = export_csv(
    "rcb_bowling_metrics.csv",
    "rcb_bowling_master.csv"
)


# ------------------------------------------------------------
# 6. OPPONENT MASTER
# ------------------------------------------------------------

opponent_master = export_csv(
    "rcb_opponent_analysis.csv",
    "rcb_opponent_master.csv"
)


# ------------------------------------------------------------
# 7. VENUE MASTER
# ------------------------------------------------------------

venue_master = export_csv(
    "rcb_venue_analysis.csv",
    "rcb_venue_master.csv"
)


# ------------------------------------------------------------
# 8. FINANCIAL MASTER
# ------------------------------------------------------------

financial_master = export_csv(
    "rcb_financial_analysis.csv",
    "rcb_financial_master.csv"
)


# ------------------------------------------------------------
# 9. PLAYER-SEASON-FINANCE MASTER
# ------------------------------------------------------------

player_season_finance = export_csv(
    "rcb_player_season_finance.csv",
    "rcb_player_season_finance_master.csv"
)


# ============================================================
# 10. CREATE SEASON SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("CREATING SEASON SUMMARY")
print("=" * 70)


cleaned_file = PROCESSED_DIR / "ipl_deliveries_cleaned.csv"

if cleaned_file.exists():

    df = pd.read_csv(
        cleaned_file,
        low_memory=False
    )

    # RCB team names
    rcb_names = [
        "Royal Challengers Bangalore",
        "Royal Challengers Bengaluru"
    ]

    # Keep only RCB batting rows
    rcb_batting = df[
        df["team"].isin(rcb_names)
    ].copy()

    # Normalize RCB name
    rcb_batting["team"] = "Royal Challengers Bangalore"

    # --------------------------------------------------------
    # Match-level information
    # --------------------------------------------------------

    match_info = (
        rcb_batting[
            [
                "match_id",
                "season",
                "venue",
                "city",
                "winner"
            ]
        ]
        .drop_duplicates("match_id")
        .copy()
    )

    # Determine result
    match_info["result"] = match_info["winner"].apply(
        lambda x:
        "No Result"
        if pd.isna(x) or str(x).strip() == ""
        else
        "Win"
        if x in rcb_names
        else
        "Loss"
    )

    # --------------------------------------------------------
    # Season match summary
    # --------------------------------------------------------

    season_matches = (
        match_info
        .groupby("season")
        .agg(
            matches_played=("match_id", "nunique"),
            wins=("result", lambda x: (x == "Win").sum()),
            losses=("result", lambda x: (x == "Loss").sum()),
            no_results=("result", lambda x: (x == "No Result").sum())
        )
        .reset_index()
    )

    # Decided matches
    season_matches["decided_matches"] = (
        season_matches["wins"]
        + season_matches["losses"]
    )

    # Win percentage
    season_matches["win_percentage"] = (
        season_matches["wins"]
        / season_matches["decided_matches"]
        * 100
    )

    season_matches["win_percentage"] = (
        season_matches["win_percentage"]
        .round(2)
    )

    # --------------------------------------------------------
    # Runs by season
    # --------------------------------------------------------

    season_runs = (
        rcb_batting
        .groupby("season")["batter_runs"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "batter_runs": "total_runs"
            }
        )
    )

    # --------------------------------------------------------
    # Merge season information
    # --------------------------------------------------------

    season_summary = season_matches.merge(
        season_runs,
        on="season",
        how="left"
    )

    # --------------------------------------------------------
    # RCB wickets by season
    # --------------------------------------------------------

    rcb_match_ids = rcb_batting["match_id"].unique()

    rcb_bowling = df[
        (df["match_id"].isin(rcb_match_ids))
        & (~df["team"].isin(rcb_names))
    ].copy()

    season_wickets = (
        rcb_bowling
        .groupby("season")["wicket_count"]
        .sum()
        .reset_index()
        .rename(
            columns={
                "wicket_count": "total_wickets"
            }
        )
    )

    # Merge wickets
    season_summary = season_summary.merge(
        season_wickets,
        on="season",
        how="left"
    )

    # Fill missing values
    season_summary["total_runs"] = (
        season_summary["total_runs"]
        .fillna(0)
        .astype(int)
    )

    season_summary["total_wickets"] = (
        season_summary["total_wickets"]
        .fillna(0)
        .astype(int)
    )

    # Sort seasons using chronological order
    season_order = [
        "2007/08",
        "2009",
        "2009/10",
        "2011",
        "2012",
        "2013",
        "2014",
        "2015",
        "2016",
        "2017",
        "2018",
        "2019",
        "2020/21",
        "2021",
        "2022",
        "2023",
        "2024",
        "2025",
        "2026"
    ]

    season_summary["season_order"] = (
        season_summary["season"]
        .apply(
            lambda x:
            season_order.index(x)
            if x in season_order
            else 999
        )
    )

    season_summary = (
        season_summary
        .sort_values("season_order")
        .drop(columns=["season_order"])
    )

    # Export
    season_summary_file = (
        FINAL_DIR / "rcb_season_summary.csv"
    )

    season_summary.to_csv(
        season_summary_file,
        index=False
    )

    print("\nSeason summary created:")
    print(season_summary)

else:

    print(
        "\nWARNING:"
        "\nipl_deliveries_cleaned.csv not found."
    )


# ============================================================
# 11. CREATE MATCH MASTER
# ============================================================

print("\n" + "=" * 70)
print("CREATING MATCH MASTER")
print("=" * 70)


if cleaned_file.exists():

    # Use RCB batting rows
    match_master = rcb_batting[
        [
            "match_id",
            "season",
            "venue",
            "city",
            "team",
            "opponent",
            "winner"
        ]
    ].drop_duplicates("match_id").copy()

    # Normalize RCB team
    match_master["team"] = (
        "Royal Challengers Bangalore"
    )

    # Result
    match_master["result"] = match_master["winner"].apply(
        lambda x:
        "No Result"
        if pd.isna(x) or str(x).strip() == ""
        else
        "Win"
        if x in rcb_names
        else
        "Loss"
    )

    # Reorder columns
    match_master = match_master[
        [
            "match_id",
            "season",
            "team",
            "opponent",
            "venue",
            "city",
            "winner",
            "result"
        ]
    ]

    # Remove duplicates
    match_master = match_master.drop_duplicates(
        "match_id"
    )

    # Export
    match_master_file = (
        FINAL_DIR / "rcb_match_master.csv"
    )

    match_master.to_csv(
        match_master_file,
        index=False
    )

    print("\nMatch master created:")
    print(
        f"Matches: {len(match_master):,}"
    )


# ============================================================
# 12. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL VALIDATION")
print("=" * 70)


final_files = list(
    FINAL_DIR.glob("*.csv")
)

print(
    f"\nTotal final CSV files: "
    f"{len(final_files)}"
)

for file in sorted(final_files):

    try:

        df_check = pd.read_csv(
            file,
            low_memory=False
        )

        print(
            f"{file.name:<45} "
            f"{len(df_check):>8,} rows"
        )

    except Exception as e:

        print(
            f"{file.name:<45} ERROR"
        )
        print(e)


# ============================================================
# 13. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("STEP 10 COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nFinal data is available in:")

print(FINAL_DIR)

print("\nYou can now use these files for:")

print("1. Power BI")
print("2. MySQL / SQL")
print("3. Data analysis")
print("4. Dashboard creation")
print("5. ML modelling")
print("6. GitHub project documentation")

print("\nNext major stage: POWER BI DASHBOARD")