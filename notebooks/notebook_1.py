import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from regelung import D, DT1, PT2
    from regelung import simulate_step
    from regelung import plot_step
    return DT1, PT2, mo, plot_step, simulate_step


@app.cell
def _(DT1, plot_step, simulate_step):
    strecke = DT1(3,T1=1.5)

    t,y = simulate_step(system=strecke.tf(), t_end=15)

    plot_step(t,y)
    return


@app.cell
def _(PT2, plot_step, simulate_step):
    D_1,T_1 = PT2.identify_from_step(h1=87.5,h_inf=60,t1=0.35)

    strecke_1 = PT2.from_damping(K=6,D=D_1,T=T_1)
    t_1,y_1 = simulate_step(strecke_1.tf())

    plot_step(t_1,y_1, show_input=True ,title=f"Schwingfähige PT2 Strecke")
    return


@app.cell
def _(mo):
    mo.md(r"""
 
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
