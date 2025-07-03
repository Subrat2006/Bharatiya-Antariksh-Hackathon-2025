import os
import requests
DATA_DIR = "insat_data"

def download_insat_file(year, month, day, time_utc):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_name = f"INSAT3D_IRBRT_{year}{month}{day}_{time_utc}.H5"
    local_file_path = os.path.join(DATA_DIR, file_name)

    if os.path.exists(local_file_path):
        print(f"✔️ File already exists: {file_name}. Skipping download.")
        return local_file_path

    print(f"⬇️ Downloading: {file_name}...")
    try:
        url = f"https://example-data-source.com/{year}/{month}/{day}/{file_name}"
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        with open(local_file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Download complete: {file_name}")
        return local_file_path

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {file_name}. Error: {e}")
        return None

#Example:
if __name__ == "__main__":
    download_insat_file("2024", "07", "01", "1200")
    download_insat_file("2024", "07", "01", "1200")
