import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("charging_history_full.csv", delimiter=",", parse_dates=["ChargeStartDateTime"])

df["QuantityBase"] = df["QuantityBase"].str.replace(" kwh", "").astype(float)



def showBarDiagram():
    plt.figure(figsize=(10, 5))
    plt.bar(df["ChargeStartDateTime"], df["QuantityBase"], color="b", label="Lademenge (kWh)")
    plt.xlabel("Zeitpunkt des Ladevorgangs")
    plt.ylabel("Lademenge (kWh)")
    plt.grid(False)
    plt.legend()
    plt.show()

def calculateAveragePerDay():
    first_day = df["ChargeStartDateTime"].min().date()
    last_day = df["ChargeStartDateTime"].max().date()
    total_days = (last_day - first_day).days + 1
    total_charge = df["QuantityBase"].sum()
    avg_daily_charge = total_charge / total_days
    print(f"Average daily charge: {avg_daily_charge}")

""""
def showWeeklyAverage():
    df["Week"] = df["ChargeStartDateTime"].dt.isocalendar().week
    weekly_avg = df.groupby("Week")["QuantityBase"].mean()
    plt.figure(figsize=(10, 5))
    plt.bar(weekly_avg.index.astype(str), weekly_avg, color="b", label="Ø Ladeleistung (kWh)")
    plt.xlabel("Woche")
    plt.ylabel("Durchschnittliche Ladeleistung (kWh)")
    plt.title("Durchschnittliche wöchentliche Ladeleistung")
    plt.grid(True)
    plt.legend()
    plt.show()

def showMonthlyAverage():
    df["Month"] = df["ChargeStartDateTime"].dt.to_period("M")
    monthly_avg = df.groupby("Month")["QuantityBase"].mean()
    plt.figure(figsize=(10, 5))
    plt.bar(monthly_avg.index.astype(str), monthly_avg, color="r", label="Ø Ladeleistung (kWh)")
    plt.xlabel("Monat")
    plt.ylabel("Durchschnittliche Ladeleistung (kWh)")
    plt.title("Durchschnittliche monatliche Ladeleistung")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.show()
    """

calculateAveragePerDay()
showBarDiagram()
