import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Geschlossener Regelkreis

    ## P-Regler mit PT1-Strecke

    Experimentiere mit verschiedenen Reglerparametern!
    """)
    return


@app.cell
def _():
    from regelung import PT1, P, PI, PID, closed_loop, simulate_step
    import matplotlib.pyplot as plt
    import numpy as np
    return P, PI, PID, PT1, closed_loop, np, plt, simulate_step


@app.cell(hide_code=True)
def _(mo):
    regler_typ = mo.ui.dropdown(
        options=["P", "PI", "PID"],
        value="P",
        label="Regler-Typ"
    )
    regler_typ
    return (regler_typ,)


@app.cell(hide_code=True)
def _(mo):
    # Streckenparameter
    K_s = mo.ui.slider(0.5, 5.0, step=0.5, value=2.0, label="Strecke K")
    T_s = mo.ui.slider(0.5, 5.0, step=0.5, value=1.0, label="Strecke T")

    mo.md("### Streckenparameter")
    mo.hstack([K_s, T_s])
    return K_s, T_s


@app.cell(hide_code=True)
def _(mo, regler_typ):
    # Reglerparameter
    mo.md("### Reglerparameter")

    Kp = mo.ui.slider(0.1, 5.0, step=0.1, value=1.0, label="Kp")

    if regler_typ.value in ["PI", "PID"]:
        Ti = mo.ui.slider(0.1, 5.0, step=0.1, value=1.0, label="Ti")
    else:
        Ti = None

    if regler_typ.value == "PID":
        Td = mo.ui.slider(0.0, 2.0, step=0.1, value=0.3, label="Td")
    else:
        Td = None

    # Anzeige
    if regler_typ.value == "P":
        mo.hstack([Kp])
    elif regler_typ.value == "PI":
        mo.hstack([Kp, Ti])
    else:
        mo.hstack([Kp, Ti, Td])
    return Kp, Td, Ti


@app.cell(hide_code=True)
def _(
    K_s,
    Kp,
    P,
    PI,
    PID,
    PT1,
    T_s,
    Td,
    Ti,
    closed_loop,
    np,
    plt,
    regler_typ,
    simulate_step,
):
    # Strecke
    strecke_r = PT1(KP=K_s.value, T=T_s.value)

    # Regler erstellen
    if regler_typ.value == "P":
        regler_r = P(Kp=Kp.value)
        regler_info = f"P(Kp={Kp.value})"
    elif regler_typ.value == "PI":
        regler_r = PI(Kp=Kp.value, Ti=Ti.value)
        regler_info = f"PI(Kp={Kp.value}, Ti={Ti.value})"
    else:
        regler_r = PID(Kp=Kp.value, Ti=Ti.value, Td=Td.value)
        regler_info = f"PID(Kp={Kp.value}, Ti={Ti.value}, Td={Td.value})"

    # Regelkreis
    system_r = closed_loop(regler_r, strecke_r)
    t_r, y_r = simulate_step(system_r, t_end=15.0)

    # Sollwert
    w_r = np.ones_like(t_r)

    # Plot
    fig_r, ax_r = plt.subplots(figsize=(12, 6))

    ax_r.plot(t_r, w_r, 'r--', linewidth=2, alpha=0.7, label='Sollwert w(t)')
    ax_r.plot(t_r, y_r, 'b-', linewidth=2.5, label='Istwert y(t)')

    # Regelgüte
    steady_state_r = y_r[-1]
    overshoot_r = (np.max(y_r) - steady_state_r) / steady_state_r * 100 if steady_state_r != 0 else 0

    ax_r.axhline(y=1.0, color='green', linestyle='--', 
                 linewidth=1, alpha=0.5, label='Ziel: 1.0')

    # 2% Band
    ax_r.axhline(y=1.02, color='orange', linestyle=':', linewidth=1, alpha=0.3)
    ax_r.axhline(y=0.98, color='orange', linestyle=':', linewidth=1, alpha=0.3, label='±2% Band')

    ax_r.grid(True, alpha=0.3)
    ax_r.set_xlabel("Zeit [s]", fontsize=12)
    ax_r.set_ylabel("Signal", fontsize=12)
    ax_r.set_title(f"Regelkreis: {regler_info} + PT1(K={K_s.value}, T={T_s.value})", 
                   fontsize=14, fontweight='bold')
    ax_r.legend(loc='best')
    ax_r.set_ylim([-0.1, max(1.5, np.max(y_r) * 1.1)])

    plt.tight_layout()
    fig_r
    return overshoot_r, steady_state_r


@app.cell(hide_code=True)
def _(mo, overshoot_r, steady_state_r):
    # Regelgüte anzeigen
    mo.md(
        f"""
        ## Regelgüte

        - **Endwert**: {steady_state_r:.4f}
        - **Regelabweichung**: {abs(1.0 - steady_state_r):.4f}
        - **Überschwingen**: {overshoot_r:.2f}%

        ### Interpretation

        - **P-Regler**: Bleibende Regelabweichung
        - **PI-Regler**: Keine bleibende Regelabweichung, aber langsamer
        - **PID-Regler**: Schneller, aber kann überschwingen
        """
    )
    return


if __name__ == "__main__":
    app.run()
