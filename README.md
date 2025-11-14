# Regelung

Eine Python-Bibliothek für Regelungstechnik-Simulationen und -Analysen.

## Features

- 🎯 **Regler**: P, PI, PID
- 📊 **Strecken**: PT1, PT2 (erweiterbar)
- 🔄 **Simulation**: Geschlossene Regelkreise, Sprungantworten
- 📈 **Visualisierung**: Plots mit und ohne Regelgütekriterien
- 🧮 **Metriken**: Überschwingen, Ausregelzeit, Anstiegszeit

## Installation

```bash
# Repository klonen
git clone <repository-url>
cd Regelung

# Mit uv installieren (empfohlen)
uv pip install -e .

# Oder mit pip
pip install -e .
```

### Abhängigkeiten

- Python >= 3.10
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
regler = PID(Kp=2.0, Ti=1.5, Td=0.3)

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

for Kp in [0.5, 1.0, 2.0, 3.0]:
    regler = P(Kp=Kp)
    system = closed_loop(regler, strecke)
    t, y = simulate_step(system)
    plt.plot(t, y, label=f"Kp={Kp}")

plt.grid(True)
plt.legend()
plt.xlabel("Zeit [s]")
plt.ylabel("y(t)")
plt.title("Vergleich verschiedener P-Regler")
plt.show()
```

## Projektstruktur

```
Regelung/
├── examples/           # Beispiel-Skripte
│   └── main.py
├── src/
│   └── regelung/      # Hauptpaket
│       ├── regler/    # Regler-Implementierungen
│       ├── strecken/  # Strecken-Modelle
│       └── simulation/ # Simulation & Visualisierung
├── report/            # Berichte und Grafiken
│   ├── figures/
│   └── report.md
├── pyproject.toml
└── README.md
```

## API-Referenz

### Regler

#### P-Regler
```python
regler = P(Kp=1.5)
```
- `Kp`: Proportionalverstärkung

#### PI-Regler
```python
regler = PI(Kp=2.0, Ti=1.0)
```
- `Kp`: Proportionalverstärkung
- `Ti`: Integrierzeit

#### PID-Regler
```python
regler = PID(Kp=2.0, Ti=1.5, Td=0.3)
```
- `Kp`: Proportionalverstärkung
- `Ti`: Integrierzeit
- `Td`: Differenzierzeit

### Strecken

#### PT1-Strecke
```python
strecke = PT1(K=2.0, T=1.0)
```
Übertragungsfunktion: `G(s) = K / (T·s + 1)`

- `K`: Verstärkung
- `T`: Zeitkonstante

#### PT2-Strecke
```python
strecke = PT2(K=1.0, T1=2.0, T2=0.5)
```
Übertragungsfunktion: `G(s) = K / ((T1·s + 1)(T2·s + 1))`

- `K`: Verstärkung
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

Vollständige Beispiele findest du im `examples/` Verzeichnis:

```bash
uv run examples/main.py
```

## Entwicklung

### Tests ausführen
```bash
# TODO: Tests implementieren
pytest tests/
```

### Code-Qualität
```bash
# Type Checking
pyright

# Linting
ruff check src/
```

## Erweiterungen

### Weitere Strecken hinzufügen

Erstelle neue Strecken in `src/regelung/strecken/`:

```python
# it.py
from control import TransferFunction

class IT1:
    """IT1-Strecke: G(s) = K / (s·(T·s + 1))"""
    def __init__(self, K: float, T: float):
        self.K = K
        self.T = T
        self.G = TransferFunction([K], [T, 1, 0])
    
    def tf(self):
        return self.G
```

Nicht vergessen in `__init__.py` zu exportieren!

### Weitere Regler hinzufügen

Analog können weitere Reglertypen in `src/regelung/regler/control.py` hinzugefügt werden.

## Roadmap

- [ ] Weitere Strecken (IT1, DT1, PT3)
- [ ] Regler-Tuning (Ziegler-Nichols, CHR)
- [ ] Bodediagramme
- [ ] Pol-Nullstellen-Plots
- [ ] Nyquist-Diagramme
- [ ] Stabilitätsanalyse
- [ ] Tests

## Lizenz

MIT

## Kontakt

Bei Fragen oder Problemen erstelle bitte ein Issue im Repository.

---

**Happy Controlling! 🎛️**
