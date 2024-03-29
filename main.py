# Exercise 5
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import matplotlib.pyplot as plt
import wget as wget

input_dir  = Path("data")
output_dir = Path("solution")

# 1. Go to http://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles
#    and download the 0.25 deg. file for daily mean temperature.
#    Save the file into the data directory but don't commit it to github!!! [2P]

url = "https://www.ecad.eu/download/ensembles/data/Grid_0.25deg_reg_ensemble/tg_ens_mean_0.25deg_reg_v19.0e.nc"
wget.download(url, out=input_dir / "climdat.nc")
# 2. Read the file using xarray. Get to know your data. What's in the file?
#    Calculate monthly means for the reference periode 1981-2010 for Europe (Extent: Lon_min:-13, Lon_max: 25, Lat_min: 30, Lat_max: 72). [2P]
data=xr.open_dataset(input_dir / "climdat.nc")
data

datatile=data.sel(latitude=slice(30, 72), longitude=slice(-13, 25), time=slice("1981-01-01", "2010-12-31"))

means = datatile.groupby("time.month").mean("time")

# 3. Calculate monthly anomalies from the reference period for the year 2018 (use the same extent as in #2).
#    Make a quick plot of the anomalies for the region. [2P]

dat18=data.sel(latitude=slice(30, 72), longitude=slice(-13, 25), time=slice("2018-01-01", "2018-12-31")).groupby("time.month").mean("time")
anomalies = dat18 - means

anomalies["tg"].plot(x="longitude", col="month")

# 4. Calculate the mean anomaly for the year 2018 for Europe (over all pixels of the extent from #2) 
#    Compare this overall mean anomaly to the anomaly of the pixel which contains Marburg. 
#    Is the anomaly of Marburg lower or higher than the one for Europe? [2P] 

anomeans=anomalies.mean()["tg"]
coords = [8.77, 50.80]
anomarburg = anomalies.sel(latitude = 50.80, longitude = 8.77, method = "nearest").mean()

if anomarburg > anomeans:
    print("Marburg's anomaly is higher.")
else:
    print("Marburg's anomaly is lower")

        
# 5. Write the monthly anomalies from task 3 to a netcdf file with name "europe_anom_2018.nc" to the solution directory.
#    Write the monthly anomalies for Marburg to a csv file with name "marburg_anom_2018.csv" to the solution directory. [2P]

anomalies.to_netcdf(output_dir / "europe_anom_2018.nc")
anomarburg_tab = anomalies.sel(latitude = 50.80, longitude = 8.77, method = "nearest").to_dataframe()
anomarburg_tab.to_csv(output_dir / "marburg_anom_2018.csv")
