from regelung import (
    PT1, 
    simulate_signal, 
    simulate_step_scaled,
    plot_step,
)
import numpy as np

def beispiel_simulate_signal():
    """Beispiel mit simulate_signal - volle Kontrolle"""
    strecke = PT1(K=2.0, T=1.0)
    
    # Zeitvektor
    t = np.linspace(0, 10, 1000)
    
    # Verschiedene Eingangssignale
    
    # 1. Sprung mit Amplitude 2.5
    u_sprung = np.ones_like(t) * 2.5
    t1, y1 = simulate_signal(strecke.tf(), t, u_sprung)
    plot_step(t1, y1, title="Sprung: u=2.5", 
              show_input=True, u_amplitude=2.5)
    
    # 2. Rampe
    u_rampe = t * 0.5  # Steigung 0.5
    t2, y2 = simulate_signal(strecke.tf(), t, u_rampe)
    
    # 3. Sinus
    u_sinus = np.sin(2 * np.pi * 0.2 * t)  # 0.2 Hz
    t3, y3 = simulate_signal(strecke.tf(), t, u_sinus)

def beispiel_simulate_step_scaled():
    """Beispiel mit simulate_step_scaled - einfacher für Sprünge"""
    strecke = PT1(K=2.0, T=1.0)
    
    for amplitude in [0.5, 1.0, 2.0, 3.0]:
        t, y = simulate_step_scaled(strecke.tf(), amplitude=amplitude)
        plot_step(t, y, 
                  title=f"PT1: Sprung u={amplitude}",
                  show_input=True,
                  u_amplitude=amplitude,
                  save=f"report/figures/sprung_{amplitude}.png")
        print(f"Amplitude {amplitude}: Endwert = {y[-1]:.3f}")

if __name__ == "__main__":
    beispiel_simulate_signal()
    beispiel_simulate_step_scaled()

