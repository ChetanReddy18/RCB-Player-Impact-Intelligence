import json
from pathlib import Path

# Location of IPL JSON files
data_folder = Path("data/raw/ipl_json")

# Find JSON files
json_files = list(data_folder.rglob("*.json"))

print("======================================")
print("RCB IPL PLAYER IMPACT PROJECT")
print("======================================")

print(f"Total JSON files: {len(json_files)}")

if not json_files:
    print("ERROR: No JSON files found!")
    exit()

# Read first match
first_file = json_files[0]

print(f"\nChecking file: {first_file.name}")

with open(first_file, "r", encoding="utf-8") as file:
    match = json.load(file)

# Basic information
info = match["info"]

print("\n========== MATCH INFORMATION ==========")
print("Season:", info.get("season"))
print("Teams:", info.get("teams"))
print("Venue:", info.get("venue"))
print("Toss:", info.get("toss"))
print("Outcome:", info.get("outcome"))

# Check innings
innings = match.get("innings", [])

print("\n========== INNINGS ==========")
print("Number of innings:", len(innings))

# Show first innings structure
if innings:

    first_innings = innings[0]

    print("\nFirst innings:")
    print(first_innings)
