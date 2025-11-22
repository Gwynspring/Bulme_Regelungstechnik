from regelung import (
    PT1,
    PT2,
    plot_step,
    simulate_step,
)
from regelung.simulation.plot import plot_step_with_metrics
from regelung.strecken.int import I


def beispiel_simulate_pt1():
    """Beispiel für eine PT1 Strecke"""
    strecke = PT1(Kp=3.0, T=1.3)  # T sollte nicht 0.0 sein!

    t, y = simulate_step(strecke.tf())

    plot_step(
        t,
        y,
        title="PT1 Strecke mit K=3.0, T=1.3",
        show_input=True,
        u_amplitude=1,
        show=True,
    )


def beispiel_simulate_pt2():
    """Beispiel für eine PT2 Strecke"""
    strecke = PT2(Kp=2, T1=1, T2=1.5)

    t, y = simulate_step(strecke.tf())

    plot_step_with_metrics(t, y, title="PT2 Strecke mit K=2, T1=1 und T2=1.5")


def beispiel_simulate_I_strecke():
    """Beispiel für eine I Strecke"""
    strecke = I.from_Ti(Ti=5)

    t, y = simulate_step(strecke.tf())

    plot_step(t, y, title="I Strecke mit Ti=2", show_input=True)


if __name__ == "__main__":
    beispiel_simulate_pt1()
    beispiel_simulate_pt2()
    beispiel_simulate_I_strecke()
