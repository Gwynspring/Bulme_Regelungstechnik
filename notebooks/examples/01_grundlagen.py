import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Regelungstechnik - Grundlagen

    ## PT1-Strecken verstehen

    Eine PT1-Strecke hat die Übertragungsfunktion:

    $$G(s) = \frac{K}{T \cdot s + 1}$$

    - **K**: Verstärkung (Endwert bei Einheitssprung)
    - **T**: Zeitkonstante (Zeit bis 63% des Endwerts)
    """)
    return


@app.cell
def _():
    # Imports
    from regelung import PT1, simulate_step_scaled, plot_step
    import matplotlib.pyplot as plt
    import numpy as np
    return PT1, np, plt, simulate_step_scaled


@app.cell
def _(mo):
    # Interaktive Parameter
    mo.md("""
    ## Parameter einstellen
    """)
    return


@app.cell
def _(mo):
    K_slider = mo.ui.slider(0.1, 5.0, step=0.1, value=2.0, label="Verstärkung K")
    T_slider = mo.ui.slider(0.1, 5.0, step=0.1, value=1.0, label="Zeitkonstante T")
    amp_slider = mo.ui.slider(0.5, 5.0, step=0.5, value=1.0, label="Sprungamplitude")

    mo.hstack([K_slider, T_slider, amp_slider])
    return K_slider, T_slider, amp_slider


@app.cell
def _(K_slider, PT1, T_slider, amp_slider, np, plt, simulate_step_scaled):
    # Simulation
    strecke = PT1(K=K_slider.value, T=T_slider.value)
    t, y = simulate_step_scaled(strecke.tf(), amplitude=amp_slider.value, t_end=15.0)

    # Eingangssignal
    u = np.ones_like(t) * amp_slider.value

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(t, u, 'r--', linewidth=2, alpha=0.7, label=f'Eingang u(t) = {amp_slider.value}')
    ax.plot(t, y, 'b-', linewidth=2.5, label='Ausgang y(t)')

    # Endwert
    steady_state = y[-1]
    ax.axhline(y=steady_state, color='green', linestyle='--', 
               linewidth=1, alpha=0.7, label=f'Endwert: {steady_state:.3f}')

    # Zeitkonstante markieren
    y_63 = steady_state * 0.632
    idx_63 = np.argmin(np.abs(y - y_63))
    ax.plot(t[idx_63], y[idx_63], 'ro', markersize=8)
    ax.axvline(x=t[idx_63], color='orange', linestyle=':', 
               linewidth=1, alpha=0.7, label=f'T = {t[idx_63]:.2f}s (63%)')

    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Zeit [s]", fontsize=12)
    ax.set_ylabel("Signal", fontsize=12)
    ax.set_title(f"PT1-Strecke: K={K_slider.value}, T={T_slider.value}", 
                 fontsize=14, fontweight='bold')
    ax.legend(loc='best')

    plt.tight_layout()
    fig
    return (steady_state,)


@app.cell
def _(mo, steady_state):
    mo.md(f"""
    ## Ergebnisse

    - **Endwert**: {steady_state:.3f}
    - **Theoretischer Endwert**: K × Amplitude = {steady_state:.3f}
    - **Ausregelzeit (98%)**: ca. {4 * 1.0:.1f}s (≈ 4×T)
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Aufgaben zum Experimentieren

    1. **Verstärkung K verdoppeln** - Was passiert mit dem Endwert?
    2. **Zeitkonstante T verdoppeln** - Wie ändert sich die Geschwindigkeit?
    3. **Sprungamplitude ändern** - Ist das System linear?
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
