import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Totzeit-Approximation mit Padé

    ## Totzeit (Dead Time)

    Eine ideale Totzeit verzögert das Signal um $T_t$ Sekunden:

    $$G(s) = e^{-T_t \cdot s}$$

    Problem: Nicht-rationale Funktion → schwer zu simulieren!

    ## Padé-Approximation

    Approximiert die Totzeit als rationale Funktion:

    **1. Ordnung:**
    $$G(s) \approx \frac{1 - \frac{T_t}{2} s}{1 + \frac{T_t}{2} s}$$

    **2. Ordnung:**
    $$G(s) \approx \frac{1 - \frac{T_t}{2} s + \frac{T_t^2}{12} s^2}{1 + \frac{T_t}{2} s + \frac{T_t^2}{12} s^2}$$
    """)
    return


@app.cell
def _():
    from regelung.strecken.totzeit import Totzeit
    from regelung import simulate_signal
    import matplotlib.pyplot as plt
    import numpy as np
    return Totzeit, np, plt, simulate_signal


@app.cell
def _(mo):
    mo.md("""
    ## Parameter
    """)
    return


@app.cell
def _(mo):
    Tt_slider = mo.ui.slider(0.1, 5.0, step=0.1, value=1.0, label="Totzeit Tt [s]")
    order_select = mo.ui.dropdown(
        options=[1, 2, 3],
        value=2,
        label="Padé-Ordnung"
    )

    mo.hstack([Tt_slider, order_select])
    return Tt_slider, order_select


@app.cell
def _(Totzeit, Tt_slider, np, order_select, plt, simulate_signal):
    # Totzeit-System erstellen
    totzeit_sys = Totzeit(Tt=Tt_slider.value, order=order_select.value)

    # Zeitvektor und Eingangssignal
    t_tot = np.linspace(0, 10, 2000)
    u_tot = np.ones_like(t_tot)
    u_tot[t_tot < 0] = 0

    # Simulation
    t_out_tot, y_tot = simulate_signal(totzeit_sys.tf(), t_tot, u_tot)

    # Ideale Totzeit (zum Vergleich)
    y_ideal = np.zeros_like(t_tot)
    delay_idx = np.argmin(np.abs(t_tot - Tt_slider.value))
    y_ideal[delay_idx:] = u_tot[:-delay_idx] if delay_idx > 0 else u_tot

    # Plot
    fig_tot, ax_tot = plt.subplots(figsize=(12, 7))

    ax_tot.plot(t_tot, u_tot, 'r--', linewidth=2, alpha=0.7, label='Eingang u(t)')
    ax_tot.plot(t_tot, y_ideal, 'g:', linewidth=3, alpha=0.5, label='Ideale Totzeit')
    ax_tot.plot(t_out_tot, y_tot, 'b-', linewidth=2.5, 
                label=f'Padé-Approximation ({order_select.value}. Ordnung)')

    # Markiere Totzeitpunkt
    ax_tot.axvline(x=Tt_slider.value, color='orange', linestyle='--', 
                   linewidth=1.5, alpha=0.7, label=f'Tt = {Tt_slider.value}s')

    ax_tot.grid(True, alpha=0.3)
    ax_tot.set_xlabel("Zeit [s]", fontsize=12)
    ax_tot.set_ylabel("Signal", fontsize=12)
    ax_tot.set_title(f"Totzeit-Approximation: Tt={Tt_slider.value}s, Ordnung={order_select.value}", 
                     fontsize=14, fontweight='bold')
    ax_tot.legend(loc='best', fontsize=11)
    ax_tot.set_ylim([-0.1, 1.3])

    plt.tight_layout()
    fig_tot
    return y_ideal, y_tot


@app.cell
def _(mo, np, order_select, y_ideal, y_tot):
    # Approximationsfehler berechnen
    error_tot = np.mean(np.abs(y_tot - y_ideal))
    max_error_tot = np.max(np.abs(y_tot - y_ideal))

    mo.md(
        f"""
        ## Approximationsqualität

        - **Mittlerer Fehler**: {error_tot:.4f}
        - **Maximaler Fehler**: {max_error_tot:.4f}
        - **Ordnung**: {order_select.value}

        ### Beobachtungen

        - **Niedrige Ordnung (1)**: Schneller, aber ungenau
        - **Höhere Ordnung (2-3)**: Genauer, aber komplexer
        - Bei **kurzen Totzeiten** reicht Ordnung 1-2
        - Bei **langen Totzeiten** ist höhere Ordnung besser
        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## Praktische Anwendung

    Totzeiten treten auf bei:
    - **Transportvorgängen** (Förderbänder, Pipelines)
    - **Messketten** (Sensoren, A/D-Wandler)
    - **Netzwerkverzögerungen** (Remote-Systeme)

    ### Tipps

    1. Totzeit so klein wie möglich halten
    2. Bei langen Totzeiten: Smith-Prädiktor verwenden
    3. Regler-Tuning wird schwieriger mit Totzeit
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
