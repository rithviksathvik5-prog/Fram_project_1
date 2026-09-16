"""
Download the eight Kenneth French datasets needed for FIN F414 FRAM Lab 1,
unzip them, and rename them exactly as data.docx requires.

Run from the project folder (the one containing the notebooks):
    python get_data.py

Creates raw_data/ and puts eight correctly named CSVs in it.
"""

import io
import sys
import zipfile
from pathlib import Path
from urllib.request import urlopen, Request

BASE = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"

# zip filename on the site  ->  name data.docx wants
DATASETS = {
    "Developed_3_Factors_CSV.zip": "developed_3_factors.csv",
    "Japan_3_Factors_CSV.zip": "japan_3_factors.csv",
    "Developed_MOM_Factor_CSV.zip": "developed_momentum.csv",
    "Japan_MOM_Factor_CSV.zip": "japan_momentum.csv",
    "Developed_25_Portfolios_ME_BE-ME_CSV.zip": "developed_25_size_bm.csv",
    "Japan_25_Portfolios_ME_BE-ME_CSV.zip": "japan_25_size_bm.csv",
    "Developed_25_Portfolios_ME_Prior_12_2_CSV.zip": "developed_25_size_momentum.csv",
    "Japan_25_Portfolios_ME_Prior_12_2_CSV.zip": "japan_25_size_momentum.csv",
}

OUT = Path("raw_data")
OUT.mkdir(exist_ok=True)

failed = []

for zip_name, target_name in DATASETS.items():
    url = BASE + zip_name
    print(f"\n{zip_name}")
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=60) as resp:
            blob = resp.read()
    except Exception as exc:
        print(f"  DOWNLOAD FAILED: {exc}")
        failed.append((zip_name, str(exc)))
        continue

    try:
        with zipfile.ZipFile(io.BytesIO(blob)) as z:
            members = [m for m in z.namelist() if m.lower().endswith(".csv")]
            if len(members) != 1:
                print(f"  UNEXPECTED ZIP CONTENTS: {z.namelist()}")
                failed.append((zip_name, f"expected 1 csv, found {z.namelist()}"))
                continue
            data = z.read(members[0])
            print(f"  extracted {members[0]}  ({len(data):,} bytes)")
    except Exception as exc:
        print(f"  UNZIP FAILED: {exc}")
        failed.append((zip_name, str(exc)))
        continue

    (OUT / target_name).write_bytes(data)
    print(f"  saved as raw_data/{target_name}")

print("\n" + "=" * 60)
present = sorted(p.name for p in OUT.glob("*.csv"))
print(f"raw_data/ now contains {len(present)} CSV files:")
for name in present:
    size = (OUT / name).stat().st_size
    print(f"  {name:38s} {size:>10,} bytes")

expected = set(DATASETS.values())
missing = expected - set(present)

if missing:
    print("\nMISSING:")
    for name in sorted(missing):
        print(f"  {name}")

if failed:
    print("\nFAILURES:")
    for zip_name, reason in failed:
        print(f"  {zip_name}: {reason}")
    print(
        "\nIf a URL 404s, the site has renamed that file. Open the data library\n"
        "page, find the dataset under 'Developed Markets Factors and Returns',\n"
        "download it manually and rename it per the table in data.docx."
    )
    sys.exit(1)

print("\nAll eight files present. Next: run 00_clean_data.ipynb and confirm")
print("245 observations, Nov 1990 to Mar 2011, zero missing, zero duplicate dates.")
