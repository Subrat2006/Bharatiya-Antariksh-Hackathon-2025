# Download a file, then generate image
from AutoFileDownload import download_latest_file
from GenerateMap import generate_grayscale_map

filename = download_latest_file()
generate_grayscale_map(filename=filename)