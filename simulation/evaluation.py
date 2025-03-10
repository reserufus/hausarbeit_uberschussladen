import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

csv_file = "out.csv"

def visualize_results(csv_file, selected_date, start_time, end_time):
    df = pd.read_csv(csv_file, parse_dates=['time'])

    df = df[df['time'].dt.date == pd.to_datetime(selected_date).date()]

    df = df[(df['time'].dt.time >= pd.to_datetime(start_time).time()) & 
            (df['time'].dt.time <= pd.to_datetime(end_time).time())]

    if df.empty:
        print(f"No data available for {selected_date}")
        return
    
    offsetY = 60
    offsetX = 1
    offset_timedelta = pd.Timedelta(minutes=offsetX)
    plt.figure(figsize=(10, 6))
    plt.fill_between(df['time'], df['surplus'], color='gray', alpha=0.5, label='Überschuss')
    plt.plot(df['time'], df['uncontrolled_charging_power'], label='Unreguliertes Laden', linestyle='-', linewidth=2, color="green")
    plt.plot(df['time'], df['preset_charging_power'], label='Voreingestelltes Laden', linestyle='-', linewidth=2, color="red")
    plt.plot(df['time'] + offset_timedelta, df['surplus_all_charging_power'] + offsetY, label='Überschussladen mit allen Informationen', linestyle='-', linewidth=2, color="orange")
    plt.plot(df['time'], df['surplus_no_soc_charging_power'], label='Überschussladen ohne Akkuinformationen', linestyle='-', linewidth=2, color="blue")
  
    
    plt.xlabel('Zeit')
    plt.ylabel('Leistung (W)')
    plt.legend()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

def calculate_charging_costs(csv_file, solar_price, grid_price):
    df = pd.read_csv(csv_file, parse_dates=['time'])

    time_interval_hours = 5 / 60  # 5 Minuten Intervalle = 5/60 Stunden

    charging_methods = ["uncontrolled", "preset", "surplus_all", "surplus_no_soc"]
    costs = {}

    for method in charging_methods:
        charging_power = df[f"{method}_charging_power"]  # Ladeleistung
        surplus = df["surplus"]  # Überschuss
        
        # Aufteilung der geladenen Energie auf PV und Netz
        pv_energy = (charging_power.clip(upper=surplus) * time_interval_hours).sum()  # Nur bis zum Überschuss
        grid_energy = ((charging_power - surplus).clip(lower=0) * time_interval_hours).sum()  # Alles darüber

        pv_energy /= 1000 #Umrechnung in Kilowattstunden
        grid_energy /= 1000
        
        # Kostenberechnung
        pv_cost = pv_energy * solar_price  # Kosten da Strom selbst verbraucht und nicht Eingespeist wird
        grid_cost = grid_energy * grid_price  # Stromkosten
        total_cost = pv_cost + grid_cost
        total_energy = pv_energy + grid_energy
        pv_share = pv_energy / total_energy * 100

        costs[method] = {
            "PV Energie (kWh)": pv_energy,
            "Netz Energie (kWh)": grid_energy,
            "Gesamtenergie (kWh)": total_energy,
            "PV-Anteil (%)": pv_share,
            "PV Kosten (€)": pv_cost,
            "Netz Kosten (€)": grid_cost,
            "Gesamtkosten (€)": total_cost,
        }

    # Ergebnis ausgeben
    method_titles = {
        "uncontrolled" : "Unreguliertes Laden",
        "preset" : "Voreingestelltes Laden",
        "surplus_all" : "Überschussladen mit allen Informationen",
        "surplus_no_soc" : "Überschussladen ohne Akkuinformationen"
    }
    for method, values in costs.items():
        print(method_titles[method])
        for key, value in values.items():
            print(f"  {key}: {value:.2f}")


calculate_charging_costs(csv_file, 0.097, 0.33)
visualize_results(csv_file, "2024-07-12", "08:00", "23:00")