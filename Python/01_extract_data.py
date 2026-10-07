import zipfile
from pathlib import Path

# Project folders
zip_file = Path("data/raw/ipl_json.zip")
extract_folder = Path("data/raw/ipl_json")

# Check whether the ZIP exists
if not zip_file.exists():
    print("ERROR: IPL ZIP file not found!")
    exit()

# Create extraction folder
extract_folder.mkdir(parents=True, exist_ok=True)

# Extract ZIP
print("Extracting IPL data...")

with zipfile.ZipFile(zip_file, "r") as zip_ref:
    zip_ref.extractall(extract_folder)

print("IPL data extracted successfully!")
print(f"Location: {extract_folder}")