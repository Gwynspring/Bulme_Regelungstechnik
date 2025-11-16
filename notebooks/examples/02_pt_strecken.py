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
    # PT1 vs PT2 Strecken

    Vergleich verschiedener Übertragungsglieder
    """)
    return


@app.cell
def _():
    from regelung import PT1, PT2, simulate_step
    import matplotlib.pyplot as plt
    import numpy as np
    return PT1, PT2, np, plt, simulate_step


@app.cell
def _(mo):
    strecken_typ = mo.ui.radio(
        options=["PT1", "PT2"],
        value="PT1",
        label="Streckentyp"
    )
    strecken_typ
    return (strecken_typ,)


@app.cell
def _(mo, strecken_typ):
    # Parameter abhängig vom Typ
    if strecken_typ.value == "PT1":
        K = mo.ui.slider(0.5, 5.0, step=0.5, value=2.0, label="K")
        T = mo.ui.slider(0.5, 5.0, step=0.5, value=1.0, label="T")
        mo.hstack([K, T])
    else:
        K = mo.ui.slider(0.5, 5.0, step=0.5, value=1.0, label="K")
        T1 = mo.ui.slider(0.5, 5.0, step=0.5, value=2.0, label="T1")
        T2 = mo.ui.slider(0.5, 5.0, step=0.5, value=0.5, label="T2")
        mo.hstack([K, T1, T2])
    return K, T, T1, T2


@app.cell
def _(K, PT1, PT2, T, T1, T2, np, plt, simulate_step, strecken_typ):
    # Strecke erstellen
    if strecken_typ.value == "PT1":
        strecke_pt = PT1(K=K.value, T=T.value)
        title_pt = f"PT1: K={K.value}, T={T.value}"
    else:
        strecke_pt = PT2(K=K.value, T1=T1.value, T2=T2.value)
        title_pt = f"PT2: K={K.value}, T1={T1.value}, T2={T2.value}"

    # Simulation
    t_pt, y_pt = simulate_step(strecke_pt.tf(), t_end=15.0)
    u_pt = np.ones_like(t_pt)

    # Plot
    fig_pt, ax_pt = plt.subplots(figsize=(10, 6))

    ax_pt.plot(t_pt, u_pt, 'r--', linewidth=2, alpha=0.7, label='Eingang u(t)')
    ax_pt.plot(t_pt, y_pt, 'b-', linewidth=2.5, label='Ausgang y(t)')

    steady_state_pt = y_pt[-1]
    ax_pt.axhline(y=steady_state_pt, color='green', linestyle='--', 
                  linewidth=1, alpha=0.7, label=f'Endwert: {steady_state_pt:.3f}')

    ax_pt.grid(True, alpha=0.3)
    ax_pt.set_xlabel("Zeit [s]", fontsize=12)
    ax_pt.set_ylabel("Signal", fontsize=12)
    ax_pt.set_title(title_pt, fontsize=14, fontweight='bold')
    ax_pt.legend(loc='best')

    plt.tight_layout()
    fig_pt
    return (steady_state_pt,)


@app.cell
def _(mo, steady_state_pt, strecken_typ):
    info_text = f"""
    ## System-Info

    - **Typ**: {strecken_typ.value}
    - **Endwert**: {steady_state_pt:.3f}
    - **Ordnung**: {'1' if strecken_typ.value == 'PT1' else '2'}
    """

    mo.md(info_text)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
