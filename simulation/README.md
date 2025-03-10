# charging simulation using solarlog data


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

Find data in file `mydata.csv`.