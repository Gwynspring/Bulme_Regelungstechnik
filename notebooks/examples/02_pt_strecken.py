import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _():
    from regelung import PT1, PT2, simulate_step, plot_step
    import matplotlib.pyplot as plt
    return PT1, PT2, plt, simulate_step


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # PT1 vs PT2 Strecken

    Interaktiver Vergleich von PT1- und PT2-Übertragungsfunktionen mit Sprungantworten.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## PT1 Strecke
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    kp_pt1 = mo.ui.slider(0.5, 5.0, step=0.1, value=2.0, label="Verstärkung K")
    t_pt1 = mo.ui.slider(0.5, 5.0, step=0.1, value=1.0, label="Zeitkonstante T")
    mo.hstack([kp_pt1, t_pt1], justify="center", gap=2)
    return kp_pt1, t_pt1


@app.cell(hide_code=True)
def _(PT1, kp_pt1, simulate_step, t_pt1):
    strecke_pt1 = PT1(KP=kp_pt1.value, T=t_pt1.value)
    t1, y1 = simulate_step(strecke_pt1.tf())
    return strecke_pt1, t1, y1


@app.cell(hide_code=True)
def _(mo, plt, strecke_pt1, t1, y1):
    fig_1 = plt.figure(figsize=(10,6))
    plt.plot(t1, y1, label=f"PT1: K={strecke_pt1.KP:.1f}, T={strecke_pt1.T:.1f}", linewidth=2)
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Eingangssignal')
    plt.grid(True, alpha=0.3)
    plt.xlabel('Zeit [s]')
    plt.ylabel('Amplitude')
    plt.title('PT1 Strecke')
    plt.legend()
    plt.tight_layout()
    axis = plt.gca()
    mo.as_html(axis)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## PT2 Strecke
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    kp_pt2 = mo.ui.slider(0.5, 5.0, step=0.1, value=1.0, label="Verstärkung K")
    t1_pt2 = mo.ui.slider(0.5, 5.0, step=0.1, value=2.0, label="Zeitkonstante T1")
    t2_pt2 = mo.ui.slider(0.5, 5.0, step=0.1, value=0.5, label="Zeitkonstante T2")
    mo.hstack([kp_pt2, t1_pt2, t2_pt2], justify="center", gap=2)
    return kp_pt2, t1_pt2, t2_pt2


@app.cell(hide_code=True)
def _(PT2, kp_pt2, t1_pt2, t2_pt2):
    strecke_pt2 = PT2(KP=kp_pt2.value, T1=t1_pt2.value, T2=t2_pt2.value)
    return (strecke_pt2,)


@app.cell(hide_code=True)
def _(mo, plt, simulate_step, strecke_pt2):
    t2, y2 = simulate_step(strecke_pt2.tf())

    fig_2 = plt.figure(figsize=(10,6))
    label = f"PT2: K={strecke_pt2.KP:.1f}, T1={strecke_pt2.T1:.1f}, T2={strecke_pt2.T2}"
    plt.plot(t2, y2, linewidth=2, label=label)
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Eingangssignal')
    plt.grid(True, alpha=0.3)
    plt.xlabel('Zeit [s]')
    plt.ylabel('Amplitude')
    plt.title('PT2 Strecke')
    plt.legend()
    plt.tight_layout()
    axis_2 = plt.gca()
    mo.as_html(axis_2)
    return t2, y2


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Vergleich

    Beide Sprungantworten im direkten Vergleich:
    """)
    return


@app.cell(hide_code=True)
def _(mo, plt, strecke_pt1, strecke_pt2, t1, t2, y1, y2):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t1, y1, label=f"PT1: K={strecke_pt1.KP:.1f}, T={strecke_pt1.T:.1f}", linewidth=2)
    ax.plot(t2, y2, label=f"PT2: K={strecke_pt2.KP:.1f}, T1={strecke_pt2.T1:.1f}, T2={strecke_pt2.T2:.1f}", linewidth=2)
    ax.axhline(y=1, color='red', linestyle='--', alpha=0.5, label='Eingangssignal')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('Zeit [s]')
    ax.set_ylabel('Amplitude')
    ax.set_title('Vergleich PT1 vs PT2')
    ax.legend()
    plt.tight_layout()
    mo.as_html(fig)
    return


@app.cell(hide_code=True)
def _():
    return


if __name__ == "__main__":
    app.run()
