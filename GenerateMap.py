import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import time
import datetime
import os

os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

preprocess_time_start = time.time()

file = os.path.join('data', '3RIMG_02JUL2025_0015_L1B_STD_V01R00.h5')

with h5py.File(file, 'r') as f:
    minutes_since_2000 = f['time'][0]
    dn = f['IMG_TIR1'][0, :, :].astype(np.uint16)         # Shape (2816, 2805)
    temp_LUT = f['IMG_TIR1_TEMP'][:]                      # Shape (1024,)
    lat = f['Latitude'][:].astype(np.float32)
    lon = f['Longitude'][:].astype(np.float32)
    bt_attrs = dict(f['IMG_TIR1'].attrs)
    lat_attrs = dict(f['Latitude'].attrs)
    lon_attrs = dict(f['Longitude'].attrs)

# Mask invalid values
dn = np.where(dn == bt_attrs['_FillValue'][0], 0, dn)   # Replace invalid DN with 0 temporarily
bt_k = temp_LUT[dn]                                     # Map DN to temperature

bt_k = np.where(dn == bt_attrs['_FillValue'][0], np.nan, bt_k)  # Re-mask

# Apply scale to lat/lon
lat[lat == lat_attrs['_FillValue'][0]] = np.nan
lon[lon == lon_attrs['_FillValue'][0]] = np.nan
lat *= lat_attrs['scale_factor'][0]
lon *= lon_attrs['scale_factor'][0]

# Create mask and flatten
mask = np.isfinite(bt_k) & np.isfinite(lat) & np.isfinite(lon)
flat_bt = bt_k[mask]
flat_lat = lat[mask]
flat_lon = lon[mask]

# Time in minutes since 2000-01-01 00:00:00\
base_time = datetime.datetime(2000, 1, 1, 0, 0, 0)

# Add the minutes
dt = base_time + datetime.timedelta(minutes=minutes_since_2000)

# Paths to save image
plasma_img_path = os.path.join('output', 'tir1_bt_map.png')
grayscale_img_path = os.path.join('output', 'tir1_bt_cloud_bw.png')

preprocess_time_end = time.time()

# Uncomment to plot in plasma
plt.figure(figsize=(16, 16))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=82.5, central_latitude=0))
ax.coastlines()
sc = ax.scatter(flat_lon, flat_lat, c=flat_bt, cmap='plasma', s=0.5, transform=ccrs.PlateCarree())
plt.colorbar(sc, label='Brightness Temperature (K)')
plt.title(f'INSAT-3DR TIR1 Brightness Temperature\n{dt.strftime("%Y-%m-%d %H:%M UTC")}')
plt.tight_layout()
plt.savefig(plasma_img_path, dpi=300, bbox_inches='tight')

plasma_graph_end = time.time()

# Plot in greyscale
norm = mcolors.Normalize(vmin=330, vmax=180) 
plt.figure(figsize=(16, 16))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=82.5, central_latitude=0))
ax.coastlines(resolution='50m')
ax.gridlines(draw_labels=True, linestyle='--', color='gray')
sc = ax.scatter(flat_lon, flat_lat, c=flat_bt, cmap='Greys', s=0.5, norm=norm, transform=ccrs.PlateCarree())
plt.colorbar(sc, label='Brightness Temperature (K)', shrink=0.6, pad=0.05)
plt.title(f'INSAT-3DR TIR1 Brightness Temperature\n(Cloud Enhancement - Grayscale)\n{dt.strftime("%Y-%m-%d %H:%M UTC")}', fontsize=14)
plt.tight_layout()
plt.savefig(grayscale_img_path, dpi=300)

grayscale_graph_end = time.time()

print(f'''Preprocessing Time: {preprocess_time_end - preprocess_time_start}
Plasma Graph Time: {plasma_graph_end - preprocess_time_end}
Greyscale Graph Time: {grayscale_graph_end - plasma_graph_end}''')
