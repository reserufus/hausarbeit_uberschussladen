import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# CSV-Datei einlesen
df = pd.read_csv("entire_2024.csv", parse_dates=["time"])

# Überschuss berechnen
df['surplus'] = df['output'] - df['consumption']

df['time'] = df['time'].dt.time

avg_surplus = df.groupby('time')['surplus'].mean()

plt.figure(figsize=(12, 6))
avg_surplus.plot(kind='bar', color='skyblue')
plt.xlabel('Uhrzeit')
plt.ylabel('Durchschnittlicher Überschuss')

tick_labels = [str(t)[:-3] for t in avg_surplus.index]
ticks = np.arange(0, len(avg_surplus), step=12)  # Jede 12. Position für 60 Minuten (5 Minuten Intervalle)
plt.xticks(ticks=ticks, labels=np.array(tick_labels)[ticks], fontsize=10)
plt.grid()
plt.tight_layout()
plt.show()