from AutoFileDownload import download_insat_file
from GenerateMap import generate_tcc_map
import argparse

def process_day(year, month, day):
    print(f"--- Processing data for {day}-{month}-{year} ---")
    for hour in range(24):
        for minute in [0, 30]:
            time_utc = f"{hour:02d}{minute:02d}"
            
            data_path = download_insat_file(year, month, day, time_utc)
            
            if data_path:
                generate_tcc_map(data_path)

if __name__ == "__main__":
    process_day("2024", "07", "01")
    process_day("2024", "07", "02")
