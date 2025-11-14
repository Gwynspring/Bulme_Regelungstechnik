from control import feedback, step_response, forced_response, series
import numpy as np

def closed_loop(regler, strecke):
    """Erstellt geschlossenen Regelkreis"""
    return feedback(series(regler.tf(), strecke.tf()), 1)

def simulate_step(system, t_end=10.0):
    """
    Simuliert Sprungantwort mit optionaler Zeitdauer.
    
    Args:
        system: Transfer-Funktion oder Regelkreis
        t_end: Simulationsende in Sekunden (default: 10.0)
        
    Returns:
        t, y: Zeit- und Ausgangsvektoren
    """
    return step_response(system, T=t_end)

def simulate_signal(system, t, u):
    """
    Simuliert Antwort auf beliebiges Eingangssignal.
    
    Args:
        system: Transfer-Funktion oder Regelkreis
        t: Zeitvektor (z.B. np.linspace(0, 10, 1000))
        u: Eingangssignal (gleiche Länge wie t)
        
    Returns:
        t, y: Zeit- und Ausgangsvektoren
        
    Beispiel:
        >>> import numpy as np
        >>> from regelung import PT1, simulate_signal, plot_step
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> t = np.linspace(0, 10, 1000)
        >>> u = np.ones_like(t) * 2.5  # Sprung mit Amplitude 2.5
        >>> t_out, y = simulate_signal(strecke.tf(), t, u)
        >>> plot_step(t_out, y, show_input=True, u_amplitude=2.5)
    """
    # Verwende forced_response aus python-control
    t_out, y = forced_response(system, T=t, U=u)
    
    return t_out, y

def simulate_step_scaled(system, amplitude=1.0, t_end=10.0):
    """
    Simuliert Sprungantwort mit beliebiger Amplitude.
    
    Args:
        system: Transfer-Funktion oder Regelkreis
        amplitude: Amplitude des Sprungs (default: 1.0)
        t_end: Simulationsdauer in Sekunden (default: 10.0)
        
    Returns:
        t, y: Zeit- und Ausgangsvektoren
        
    Beispiel:
        >>> from regelung import PT1, simulate_step_scaled, plot_step
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> t, y = simulate_step_scaled(strecke.tf(), amplitude=2.5)
        >>> plot_step(t, y, show_input=True, u_amplitude=2.5)
    """
    # Normale Sprungantwort (Amplitude=1)
    t, y = step_response(system, T=t_end)
    
    # Skaliere Ausgang mit Amplitude (lineares System!)
    y_scaled = y * amplitude
    
    return t, y_scaled
