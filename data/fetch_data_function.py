import os
import requests
from datetime import datetime, timedelta
from urllib.parse import quote_plus

def fetch_exoplanet_tap(sql, fmt="csv", save_path="data/exoplanets_data.csv"):
    """
    Downloads data from the NASA Exoplanet Archive via TAP and saves the CSV file.

    Parameters:
        sql (str): SQL query to execute.
        fmt (str): Output format (default: "csv").
        save_path (str): File path to save the CSV (default: "data/exoplanets_data.csv").
    """

    # Check if CSV exists
    if os.path.exists(save_path):
        mtime = datetime.fromtimestamp(os.path.getmtime(save_path))
        age = datetime.now() - mtime

        # If file is recent (< 1 day), don't update
        if age < timedelta(days=1):
            print(f"✅ Using cached data (last updated {age.seconds // 3600} hours ago).")
            return 

        else:
            print("🕒 Cached data is older than 1 day — refreshing...")

    else:
        print("📂 No CSV found — downloading data...")

    # Build the TAP URL
    url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query={quote_plus(sql)}&format={fmt}"
    print(f"Fetching data from: {url}")

    # Make the request
    r = requests.get(url, timeout=60)
    r.raise_for_status()

    # Ensure directory exists and save the file
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(r.text)

    print(f"✅ File saved as: {save_path}")

sql = "select pl_name,hostname,sy_snum,sy_pnum,sy_mnum,discoverymethod,disc_year,disc_facility,disc_instrument,pl_orbper,pl_rade,pl_radj,pl_masse,pl_massj,pl_dens,st_rad,st_mass,sy_dist,releasedate from ps"
exoplanets = fetch_exoplanet_tap(sql)