# examples/totzeit.py
from regelung import PT1, Totzeit, plot_step, series_connection, simulate_step


def beispiel_totzeit():
    """Beispiel mit scipy.interpolate.pade"""
    strecke = PT1(Kp=3.0, T=1.3)

    # Ohne Totzeit
    t, y = simulate_step(strecke.tf(), t_end=15)
    plot_step(t, y, title="PT1: K=3.0, T=1.3 (ohne Totzeit)", show_input=True)

    # Mit Totzeit
    delay = Totzeit(Tt=2, order=2)
    system = series_connection(strecke, delay)
    t, y = simulate_step(system, t_end=10)
    plot_step(
        t,
        y,
        title="PT1: Kp=3.0, T=1.3 mit Totzeit Tt=2",
        show_input=True,
    )


if __name__ == "__main__":
    beispiel_totzeit()
