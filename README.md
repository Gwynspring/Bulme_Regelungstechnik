# Regelung

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![uv](https://img.shields.io/badge/uv-managed-blueviolet.svg)
![Control Systems](https://img.shields.io/badge/control--systems-0.10.2-orange.svg)
![Matplotlib](https://img.shields.io/badge/matplotlib-latest-red.svg)

Eine Python-Bibliothek für Regelungstechnik-Simulationen und -Analysen,
basierend auf der [Python Control Systems Library](https://python-control.readthedocs.io/en/0.10.2/).


## Features

- 🎯 **Regler**: P, PI, PID
- 📊 **Strecken**: PT1, PT2, I, IT1, D, DT1 und Totzeiten 
- 🔄 **Simulation**: Geschlossene Regelkreise, Sprungantworten mit verschiedenen Eingangssignalen
- 📈 **Visualisierung**: Plots mit und ohne Regelgütekriterien

## Installation

```bash
git clone https://github.com/Gwynspring/Bulme_Regelungstechnik.git
cd Bulme_Regelungstechnik
``` 

 Mit [UV](https://docs.astral.sh/uv/getting-started/installation/) installieren (empfohlen)

```bash
uv pip install -e .

# Oder mit pip
pip install -e .
```

### Abhängigkeiten

- Python >= 3.12
- control
- matplotlib
- numpy

## Schnellstart

### Einfache PT1-Strecke

```python
from regelung import PT1, simulate_step, plot_step

# PT1-Strecke erstellen
strecke = PT1(K=2.0, T=1.0)

# Sprungantwort simulieren
t, y = simulate_step(strecke.tf())

# Plotten
plot_step(t, y, title="PT1-Strecke")
```

### Geschlossener Regelkreis

```python
from regelung import PT2, PID, closed_loop, simulate_step, plot_step_with_metrics

# Strecke und Regler definieren
strecke = PT2(K=1.0, T1=2.0, T2=0.5)
regler = PID(KP=2.0, TI=1.5, TD=0.3)

# Regelkreis schließen
system = closed_loop(regler, strecke)

# Simulieren und plotten mit Metriken
t, y = simulate_step(system)
plot_step_with_metrics(t, y, 
                       title="PT2 mit PID-Regler",
                       save="figures/pt2_pid.png")
```

### Verschiedene Regler vergleichen

```python
from regelung import PT1, P, closed_loop, simulate_step
import matplotlib.pyplot as plt

strecke = PT1(K=2.0, T=1.0)

plt.figure(figsize=(10, 6))

for KP in [0.5, 1.0, 2.0, 3.0]:
    regler = P(KP=Kp)
    system = closed_loop(regler, strecke)
    t, y = simulate_step(system)
    plt.plot(t, y, label=f"Kp={regler.KP}")

plt.grid(True)
plt.legend()
plt.xlabel("Zeit [s]")
plt.ylabel("y(t)")
plt.title("Vergleich verschiedener P-Regler")
plt.show()
```

## Projektstruktur

```
Bulme_Regelungstechnik/
├── examples/                    # Beispiel-Skripte
│   ├── example_signal.py
│   ├── example_strecke.py
│   └── totzeit.py
├── notebooks/                   # Interaktive Notebooks (Marimo)
│   ├── examples/
│   │   ├── 01_grundlagen.py
│   │   ├── 02_pt_strecken.py
│   │   ├── 03_regler.py
│   │   └── 04_totzeit.py
│   └── test.py
├── src/
│   └── regelung/               # Hauptpaket
│       ├── regler/             # Regler-Implementierungen
│       │   └── control.py
│       ├── strecken/           # Strecken-Modelle
│       │   ├── pt.py           # PT1, PT2
│       │   ├── int.py          # I, IT1
│       │   ├── diff.py         # D, DT1
│       │   └── totzeit.py      # Totzeit
│       └── simulation/         # Simulation & Visualisierung
│           ├── core.py
│           └── plot.py
├── report/                     # Berichte und Grafiken
│   ├── figures/
│   └── report.md
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```

## API-Referenz

### Regler

#### P-Regler
```python
regler = P(KP=1.5)
```
- `KP`: Proportionalverstärkung

#### PI-Regler
```python
regler = PI(KP=2.0, TI=1.0)
```
- `KP`: Proportionalverstärkung
- `TI`: Integrierzeit

#### PID-Regler
```python
regler = PID(KP=2.0, TI=1.5, TD=0.3)
```
- `KP`: Proportionalverstärkung
- `TI`: Integrierzeit
- `TD`: Differenzierzeit

### Strecken

#### PT1-Strecke
```python
strecke = PT1(KP=2.0, T=1.0)
```
Übertragungsfunktion: `G(s) = KP / (T·s + 1)`

- `KP`: Verstärkung
- `T`: Zeitkonstante

#### PT2-Strecke
```python
strecke = PT2(KP=1.0, T1=2.0, T2=0.5)
```
Übertragungsfunktion: `G(s) = KP / ((T1·s + 1)(T2·s + 1))`

- `KP`: Verstärkung
- `T1`, `T2`: Zeitkonstanten

### Simulation

#### Geschlossener Regelkreis
```python
system = closed_loop(regler, strecke)
```
Erstellt ein Feedback-System mit Regler und Strecke.

#### Sprungantwort simulieren
```python
t, y = simulate_step(system, t_end=10.0)
```
- `system`: Transfer-Funktion oder Regelkreis
- `t_end`: Simulationsende (optional)
- Returns: `(t, y)` - Zeit- und Ausgangsvektoren

#### Beliebiges Signal simulieren
```python
t, y = simulate_signal(system, t, u)
```
- `system`: Transfer-Funktion
- `t`: Zeitvektor
- `u`: Eingangssignal

### Visualisierung

#### Einfacher Plot
```python
plot_step(t, y, 
          title="Sprungantwort",
          save="figures/plot.png",
          show=True)
```

#### Plot mit Regelgütekriterien
```python
plot_step_with_metrics(t, y,
                       title="Sprungantwort mit Metriken",
                       save="figures/metrics.png")
```

Zeigt automatisch:
- Endwert (stationärer Wert)
- Überschwingen in %
- Ausregelzeit (2%-Kriterium)
- Anstiegszeit (10%-90%)

## Beispiele

Vollständige Beispiele findest du im [examples](./examples) Verzeichnis:

```bash
uv run examples/example_signal.py
```

Oder interaktive Notebooks mit [Marimo](https://marimo.io/):

```bash
uv run marimo edit notebooks/examples/01_grundlagen.py
```

## Lizenz

MIT

## Kontakt

Bei Fragen oder Problemen erstelle bitte ein Issue im Repository.
