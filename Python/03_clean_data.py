import json
import pandas as pd
from pathlib import Path

# ======================================
# FILE PATHS
# ======================================

data_folder = Path("data/raw/ipl_json")
output_folder = Path("data/processed")

output_folder.mkdir(parents=True, exist_ok=True)

json_files = list(data_folder.rglob("*.json"))

print("======================================")
print("RCB IPL DATA CLEANING")
print("======================================")

print("Total matches found:", len(json_files))

rows = []

# ======================================
# PROCESS MATCHES
# ======================================

for file in json_files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    match_id = file.stem

    season = info.get("season")

    teams = info.get("teams", [])

    venue = info.get("venue", "")

    city = info.get("city", "")

    outcome = info.get("outcome", {})

    winner = outcome.get("winner", "")

    # ==================================
    # PROCESS INNINGS
    # ==================================

    for innings_number, innings in enumerate(
        match.get("innings", []),
        start=1
    ):

        team = innings.get("team", "")

        opponent = ""

        for other_team in teams:

            if other_team != team:
                opponent = other_team
                break

        # ==================================
        # PROCESS OVERS
        # ==================================

        for over_data in innings.get("overs", []):

            over_number = over_data.get("over")

            # ==================================
            # PROCESS DELIVERIES
            # ==================================

            for delivery in over_data.get(
                "deliveries",
                []
            ):

                batter = delivery.get(
                    "batter",
                    ""
                )

                bowler = delivery.get(
                    "bowler",
                    ""
                )

                non_striker = delivery.get(
                    "non_striker",
                    ""
                )

                runs = delivery.get(
                    "runs",
                    {}
                )

                batter_runs = runs.get(
                    "batter",
                    0
                )

                extras = runs.get(
                    "extras",
                    0
                )

                total_runs = runs.get(
                    "total",
                    0
                )

                # ==================================
                # EXTRA TYPES
                # ==================================

                extra_data = delivery.get(
                    "extras",
                    {}
                )

                # In Cricsheet, extras can be a
                # dictionary such as:
                # {"wides": 1}
                # {"noballs": 1}

                extra_types = []

                if isinstance(extra_data, dict):

                    extra_types = list(
                        extra_data.keys()
                    )

                is_wide = (
                    "wides" in extra_types
                )

                is_noball = (
                    "noballs" in extra_types
                )

                is_bye = (
                    "byes" in extra_types
                )

                is_legbye = (
                    "legbyes" in extra_types
                )

                is_penalty = (
                    "penalty" in extra_types
                )

                # ==================================
                # WICKETS
                # ==================================

                wickets = delivery.get(
                    "wickets",
                    []
                )

                wicket_count = len(wickets)

                player_out = ""

                wicket_kind = ""

                if wickets:

                    player_out = wickets[0].get(
                        "player_out",
                        ""
                    )

                    wicket_kind = wickets[0].get(
                        "kind",
                        ""
                    )

                # ==================================
                # STORE ROW
                # ==================================

                rows.append({

                    "match_id": match_id,

                    "season": season,

                    "venue": venue,

                    "city": city,

                    "team": team,

                    "opponent": opponent,

                    "innings": innings_number,

                    "over": over_number,

                    "delivery": delivery.get(
                        "actual_delivery",
                        ""
                    ),

                    "batter": batter,

                    "bowler": bowler,

                    "non_striker": non_striker,

                    "batter_runs": batter_runs,

                    "extras": extras,

                    "total_runs": total_runs,

                    "wicket_count": wicket_count,

                    "player_out": player_out,

                    "wicket_kind": wicket_kind,

                    "is_wide": is_wide,

                    "is_noball": is_noball,

                    "is_bye": is_bye,

                    "is_legbye": is_legbye,

                    "is_penalty": is_penalty,

                    "winner": winner
                })


# ======================================
# CREATE DATAFRAME
# ======================================

df = pd.DataFrame(rows)

print("\n======================================")
print("DATASET CREATED")
print("======================================")

print(
    "Total deliveries:",
    len(df)
)

print("\nColumns:")

print(
    df.columns.tolist()
)

print("\nFirst 5 rows:")

print(
    df.head()
)

# ======================================
# SAVE
# ======================================

output_file = (
    output_folder /
    "ipl_deliveries_cleaned.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("\n======================================")
print("SUCCESS")
print("======================================")

print("Saved to:")

print(output_file)