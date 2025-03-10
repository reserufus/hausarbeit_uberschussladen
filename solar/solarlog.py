import json
import click
from pydantic import BaseModel
import requests
import dateutil
import datetime
import pandas as pd

class Configuration(BaseModel):
    host: str

@click.group()
def cli():
    pass

@click.command()
@click.option("--first", help="First day", required=False)
@click.option("--last", help="Last day", required=False)
@click.option("--datafile", default="data.csv", help="Data *.csv file")
@click.option("--config", default="config.json", help="JSON configuration file")
def data(first:str, last:str, datafile:str, config:str):
    with open(config) as config_file:
        configuration = Configuration(**json.load(config_file))
    date_now = datetime.datetime.now()
    date_first = dateutil.parser.parse(first) if not first == None else date_now
    date_last = dateutil.parser.parse(last) if not last == None else date_first
    data_df = pd.DataFrame()
    for dt in dateutil.rrule.rrule(dateutil.rrule.DAILY, dtstart=date_first, until=date_last):
        click.echo(click.style(f"Retrieving data for {dt.strftime('%Y-%m-%d')} ...", fg='yellow'))
        diff = str((date_now-dt).days)
        resp = requests.post(configuration.host + '/getjp', json = {'776':{diff:None}})
        raw = resp.json()
        dat = [{'time': dt.strftime('%Y-%m-%d') + ' ' + _a[0], 'output': _a[1][0][0], 'consumption': _a[1][1][0]} for _a in raw['776'][diff]]
        data_df = pd.concat([data_df, pd.DataFrame(dat)], ignore_index=True)
        
    data_df.to_csv(datafile, index=False)
    click.echo(click.style(f"File {datafile} written.", fg='green'))

cli.add_command(data)

if __name__ == '__main__':
    cli()