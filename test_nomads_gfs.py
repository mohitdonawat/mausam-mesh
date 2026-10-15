import urllib.request
import re
import json

def test_nomads():
    base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/"
    print(f"Connecting to NOAA NOMADS: {base_url} ...")
    req = urllib.request.Request(base_url, headers={'User-Agent': 'MausamMesh-Client/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            # Extract date directories like gfs.YYYYMMDD
            folders = re.findall(r'href=["\'](gfs\.\d{8})/?["\']', html)
            unique_folders = sorted(list(set(folders)), reverse=True)
            print(f"Successfully connected! Found {len(unique_folders)} active GFS production dates on NOMADS:")
            for f in unique_folders[:5]:
                print(f"  - {f}")
            
            if unique_folders:
                latest = unique_folders[0]
                check_sub = f"{base_url}{latest}/00/atmos/"
                print(f"\nChecking latest cycle atmos directory: {check_sub}")
                sub_req = urllib.request.Request(check_sub, headers={'User-Agent': 'MausamMesh-Client/1.0'})
                with urllib.request.urlopen(sub_req, timeout=10) as sub_resp:
                    sub_html = sub_resp.read().decode('utf-8', errors='ignore')
                    files = re.findall(r'href=["\'](gfs\.t00z\.pgrb2\.0p25\.f\d{3}[^"\']*)["\']', sub_html)
                    print(f"Found {len(files)} 0.25-degree GFS GRIB2 forecast files in cycle!")
                    for fl in files[:5]:
                        print(f"  * {fl}")
    except Exception as e:
        print(f"Connection error or timeout: {e}")

if __name__ == "__main__":
    test_nomads()
