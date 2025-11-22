import numpy as np

from regelung import (
    PT1,
    plot_step,
    simulate_signal,
    simulate_step,
    plot_signal
)

def beispiel_simulate_signal():
    """Beispiel mit simulate_signal - volle Kontrolle"""
    strecke = PT1(Kp=2.0, T=3.0)

    t = np.linspace(0, 20, 1000)

    # 1. Sprung mit Amplitude 2.5
    t_1, y_1 = simulate_step(strecke.tf(), t_end=20)
    plot_step(
        t_1,
        y_1,
        title=f"Sprungantwort einer PT1 Strecke mit Kp={strecke.Kp} und T={strecke.T} ",
        show=True,
        show_input=True,
    )

    # 2. Sinunseingang
    u_sinus = np.sin(2 * np.pi * 0.2 * t)  # 0.2 Hz
    t_2, y_2 = simulate_signal(strecke.tf(), t=t, u=u_sinus)
    plot_signal(
        t_2,
        y_2,
        title="Antwort einer PT1 Strecke auf einen sinusförmigen Eingang",
        show=True,
        show_input=True,
        u=u_sinus,
    )

    # 3. Rampe
    u_rampe = t * 0.5  # Steigung 0.5
    t_3, y_3 = simulate_signal(strecke.tf(), t, u_rampe)
    plot_signal(
        t_3,
        y_3,
        title="Antwort einer PT1 Strecke auf einen rampenförmigen Eingang",
        show=True,
        show_input=True,
        u=u_rampe,
    )


if __name__ == "__main__":
    beispiel_simulate_signal()
