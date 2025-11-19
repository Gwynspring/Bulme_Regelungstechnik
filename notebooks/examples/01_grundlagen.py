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

    $$G(s) =     rac {KP}{T \cdot s + 1}$$

    - **KP**: Verstärkung (Endwert bei Einheitssprung)
    - **T**: Zeitkonstante (Zeit bis 63% des Endwerts)
    """)
    return


@app.cell
def _():
    # Imports
    from regelung import PT1, simulate_step_scaled, plot_step
    import matplotlib.pyplot as plt
    import numpy as np
    return PT1, plot_step, simulate_step_scaled


@app.cell
def _(mo):
    # Interaktive Parameter
    mo.md("""
    ## Parameter einstellen
    """)
    return


@app.cell
def _(mo):
    K_slider = mo.ui.slider(0.1, 10.0, step=0.1, value=3.0, label="Verstärkung KP")
    T_slider = mo.ui.slider(0.1, 20.0, step=0.1, value=10.0, label="Zeitkonstante T")
    amp_slider = mo.ui.slider(0.5, 20.0, step=0.5, value=10.0, label="Sprungamplitude")

    mo.hstack([K_slider, T_slider, amp_slider])
    return K_slider, T_slider, amp_slider


@app.cell
def _(K_slider, PT1, T_slider, amp_slider, plot_step, simulate_step_scaled):
    # Simulation
    strecke = PT1(KP=K_slider.value, T=T_slider.value)
    t, y = simulate_step_scaled(strecke.tf(), amplitude=amp_slider.value, t_end=15.0)
    plot_step(t,y, title=f"PT1 Strecke mit KP={strecke.KP} und T={strecke.T}", show_input=True, u_amplitude=amp_slider.value)
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
