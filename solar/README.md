# solarlog data retrieval

The script `solarlog.py` fetches the solar data from the specified host name for the specified date period.

Adjust file `config.json`:
```
{
    "host": "http://<solarlog host name>"
}
``` 

Then run

```
python solarlog.py data --first 20241225 --last 20241226 --datafile mydata.csv --config config.json
```

This fetches the data from December 25th 2024 until December 26th 2024 and saves it in file `mydata.csv`.
**Warning: If the period is long (e.g. 1 Year), the script might run for some time.**


The script `surplus_plot.py` uses the data to create a bar diagram to plot the average surplus by time of day.

