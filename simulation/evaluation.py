import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import click

@click.group()
def cli():
    """Ein CLI-Tool zur Visualisierung und Analyse von Ladedaten."""
    pass

@cli.command()
@click.option('--csv-file', required=True, type=str, help='Pfad zur CSV-Datei')
@click.option('--method', default='all', type=click.Choice(['all', 'uncontrolled', 'preset', 'surplus_all', 'surplus_no_soc']), help='Ausgewähltes Ladeverfahren (Standard: alle)')
def plot_weekly_pv_share(csv_file, method):
    """
    Zeichnet den wöchentlichen PV-Anteil für ein ausgewähltes Ladeverfahren oder alle Verfahren über den gesamten Zeitraum.
    """
    df = pd.read_csv(csv_file, parse_dates=['time'])

    # Zeitintervall (5 Minuten)
    time_interval_hours = 5 / 60

    # Woche und Jahr extrahieren
    df['year_week'] = df['time'].dt.strftime('%Y-%U')

    methods = ["uncontrolled", "preset", "surplus_all", "surplus_no_soc"]
    method_titles = {
        "uncontrolled": "Unreguliertes Laden",
        "preset": "Voreingestelltes Laden",
        "surplus_all": "Überschussladen mit allen Informationen",
        "surplus_no_soc": "Überschussladen ohne Akkuinformationen"
    }

    colors = {
        "uncontrolled": "green",
        "preset": "red",
        "surplus_all": "orange",
        "surplus_no_soc": "blue"
    }

    selected_methods = methods if method == 'all' else [method]

    weeks = sorted(df['year_week'].unique())
    weekly_pv_shares = {m: [] for m in selected_methods}

    for week in weeks:
        week_df = df[df['year_week'] == week]

        for m in selected_methods:
            charging_power = week_df[f"{m}_charging_power"]
            surplus = week_df["surplus"]

            pv_energy = (charging_power.clip(upper=surplus) * time_interval_hours).sum()
            grid_energy = ((charging_power - surplus).clip(lower=0) * time_interval_hours).sum()

            total_energy = pv_energy + grid_energy
            pv_share_percentage = (pv_energy / total_energy * 100) if total_energy > 0 else 0
            weekly_pv_shares[m].append(pv_share_percentage)

    # Plot erstellen
    plt.figure(figsize=(14, 7))

    for m in selected_methods:
        plt.plot(weeks, weekly_pv_shares[m], marker='o', linestyle='-', label=method_titles[m], color=colors[m])

    title_suffix = 'alle Ladeverfahren' if method == 'all' else method_titles[method]
    plt.title(f"Wöchentlicher PV-Anteil (%) - {title_suffix}")
    plt.xlabel("Kalenderwoche")
    plt.ylabel("PV-Anteil (%)")
    plt.grid(True)
    plt.ylim(0, 100)

    # X-Achse übersichtlich formatieren
    plt.xticks(rotation=45)

    if method == 'all':
        plt.legend()

    plt.tight_layout()
    plt.show()





@cli.command()
@click.option('--csv-file', required=True, type=str, help='Pfad zur CSV-Datei')
@click.option('--selected-date', required=True, type=str, help='Datum im Format YYYY-MM-DD')
@click.option('--start-time', required=True, type=str, help='Startzeit im Format HH:MM')
@click.option('--end-time', required=True, type=str, help='Endzeit im Format HH:MM')
def plot_charging_data(csv_file, selected_date, start_time, end_time):
    """
    Zeichnet ein Diagramm der Ladedaten für einen gegebenen Zeitraum an einem Tag.
    """
    df = pd.read_csv(csv_file, parse_dates=['time'])

    df = df[df['time'].dt.date == pd.to_datetime(selected_date).date()]
    df = df[(df['time'].dt.time >= pd.to_datetime(start_time).time()) & 
            (df['time'].dt.time <= pd.to_datetime(end_time).time())]

    if df.empty:
        click.echo(f"Keine Daten verfügbar für {selected_date}")
        return
    
    offsetY = 60
    offsetX = 1
    offset_timedelta = pd.Timedelta(minutes=offsetX)
    
    plt.figure(figsize=(10, 6))
    plt.fill_between(df['time'], df['surplus'], color='gray', alpha=0.5, label='Überschuss')
    plt.plot(df['time'], df['uncontrolled_charging_power'], label='Unreguliertes Laden', linestyle='-', linewidth=2, color="green")
    plt.plot(df['time'], df['preset_charging_power'], label='Voreingestelltes Laden', linestyle='-', linewidth=2, color="red")
    plt.plot(df['time'] + offset_timedelta, df['surplus_all_charging_power'] + offsetY, 
             label='Überschussladen mit allen Informationen', linestyle='-', linewidth=2, color="orange")
    plt.plot(df['time'], df['surplus_no_soc_charging_power'], 
             label='Überschussladen ohne Akkuinformationen', linestyle='-', linewidth=2, color="blue")
    
    plt.xlabel('Zeit')
    plt.ylabel('Leistung (W)')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

@cli.command()
@click.option('--csv-file', required=True, type=str, help='Pfad zur CSV-Datei')
@click.option('--solar-price', required=True, type=float, help='Preis pro kWh für Solarstrom in €')
@click.option('--grid-price', required=True, type=float, help='Preis pro kWh für Netzstrom in €')
def print_charging_costs(csv_file, solar_price, grid_price):
    """
    Berechnet und gibt die Ladekosten für die verschiedenen Methoden aus.
    """
    df = pd.read_csv(csv_file, parse_dates=['time'])

    time_interval_hours = 5 / 60  # 5 Minuten Intervalle = 5/60 Stunden
    charging_methods = ["uncontrolled", "preset", "surplus_all", "surplus_no_soc"]
    costs = {}

    for method in charging_methods:
        charging_power = df[f"{method}_charging_power"]
        surplus = df["surplus"]
        
        pv_energy = (charging_power.clip(upper=surplus) * time_interval_hours).sum()
        grid_energy = ((charging_power - surplus).clip(lower=0) * time_interval_hours).sum()
        
        pv_energy /= 1000  # Umrechnung in Kilowattstunden
        grid_energy /= 1000
        
        pv_cost = pv_energy * solar_price
        grid_cost = grid_energy * grid_price
        total_cost = pv_cost + grid_cost
        total_energy = pv_energy + grid_energy
        pv_share = pv_energy / total_energy * 100 if total_energy > 0 else 0

        costs[method] = {
            "PV Energie (kWh)": pv_energy,
            "Netz Energie (kWh)": grid_energy,
            "Gesamtenergie (kWh)": total_energy,
            "PV-Anteil (%)": pv_share,
            "PV Kosten (€)": pv_cost,
            "Netz Kosten (€)": grid_cost,
            "Gesamtkosten (€)": total_cost,
        }

    method_titles = {
        "uncontrolled": "Unreguliertes Laden",
        "preset": "Voreingestelltes Laden",
        "surplus_all": "Überschussladen mit allen Informationen",
        "surplus_no_soc": "Überschussladen ohne Akkuinformationen"
    }
    
    for method, values in costs.items():
        click.echo(f"\n{method_titles[method]}")
        for key, value in values.items():
            click.echo(f"  {key}: {value:.2f}")

if __name__ == '__main__':
    cli()