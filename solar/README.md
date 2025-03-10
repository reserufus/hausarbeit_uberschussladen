# Solarlog Data Retrieval

This repository contains tools for fetching and visualizing solar data from a Solarlog system. The primary script, `solarlog.py`, retrieves solar data for a specified date range from a given hostname, while `surplus_plot.py` generates a bar diagram of average surplus energy by time of day.

## Fetching Solar Data

### Configuration

Before running the data retrieval, configure the `config.json` file with the following parameter:

```
{
    "host": "http://<solarlog host name>"
}
```

Replace `<solarlog host name>` with the actual hostname of your Solarlog system (e.g., "http://solarlog.example.com").

### Running the Script

To fetch solar data, execute the following command:

```
python solarlog.py data --first 20241225 --last 20241226 --datafile mydata.csv --config config.json
```

This retrieves data from December 25, 2024, to December 26, 2024, and saves it to `mydata.csv`.

**Warning**: For long periods (e.g., a full year), the script may take significant time to complete due to the volume of data being fetched.

## Visualizing Surplus Data

The script `surplus_plot.py` processes the retrieved data to create a bar diagram illustrating the average surplus energy by time of day. Refer to its specific usage instructions within the script or an accompanying README if provided.

