from control import feedback, step_response, forced_response, series
import numpy as np

def closed_loop(regler, strecke):
    """Erstellt geschlossenen Regelkreis"""
    return feedback(series(regler.tf(), strecke.tf()), 1)

def simulate_step(system, t_end: float = 10.0):
    """Simuliert Sprungantwort mit optionaler Zeitdauer"""
    return step_response(system, T=t_end)

def simulate_signal(system, t, u):
    """Simuliert Antwort auf beliebiges Eingangssignal"""
    return forced_response(system, t, u)

def get_metrics(t, y) -> dict:
    """Berechnet Regelgütekriterien"""
    steady_state = y[-1]
    overshoot = (np.max(y) - steady_state) / steady_state * 100
    settling_time = t[np.where(np.abs(y - steady_state) < 0.02 * steady_state)[0][0]]
    
    return {
        'overshoot': overshoot,
        'settling_time': settling_time,
        'steady_state': steady_state
    }
