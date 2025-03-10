import matplotlib.pyplot as plt

# Daten
methods = ["Unreguliertes Laden", "Voreingestelltes Laden", "Überschussladen \n(mit Akkuinformation)", "Überschussladen \n(ohne Akkuinformation)"]
costs = [1286.51, 1044.23, 931.83, 1031.10]
colors = ['green', 'red', 'orange', 'blue']

# Balkendiagramm erstellen
plt.figure(figsize=(10, 6))
plt.bar(methods, costs, color=colors)

# Titel und Achsenbeschriftung
plt.title("Jährliche Gesamtkosten der Methoden", fontsize=14)
plt.ylabel("Kosten (€)", fontsize=12)

# Gitter
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Werte über den Balken anzeigen
for i, value in enumerate(costs):
    plt.text(i, value + 20, f"{value:.2f} €", ha='center', va='bottom', fontsize=10)

# Rahmen oben und rechts entfernen
for pos in ['right', 'top']:
    plt.gca().spines[pos].set_visible(False)

# Diagramm anzeigen
plt.tight_layout()
plt.show()