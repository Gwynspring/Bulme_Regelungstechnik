"""
Simulationsfunktionen für Regelkreise.
"""

from control import feedback, step_response, forced_response, series
import numpy as np


def closed_loop(regler, strecke):
    """
    Erstellt geschlossenen Regelkreis.
    
    Args:
        regler: Regler-Objekt mit .tf() Methode
        strecke: Strecken-Objekt mit .tf() Methode
        
    Returns:
        Transfer-Funktion des geschlossenen Regelkreises
    """
    return feedback(series(regler.tf(), strecke.tf()), 1)


def simulate_step(system, t_end=10.0):
    """
    Simuliert Sprungantwort mit einer Amplitude von 1 und optionaler Zeitdauer.
    
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
        >>> from regelung import PT1, simulate_signal
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> t = np.linspace(0, 10, 1000)
        >>> u = np.ones_like(t) * 2.5  # Sprung mit Amplitude 2.5
        >>> t_out, y = simulate_signal(strecke.tf(), t, u)
    """
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
        >>> from regelung import PT1, simulate_step_scaled
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> t, y = simulate_step_scaled(strecke.tf(), amplitude=2.5)
    """
    t, y = step_response(system, T=t_end)
    y_scaled = y * amplitude
    return t, y_scaled


def series_connection(*systems):
    """
    Verschaltet mehrere Systeme in Serie (Reihenschaltung).
    
    Args:
        *systems: Variable Anzahl von Transfer-Funktionen oder Objekten mit .tf()
        
    Returns:
        Transfer-Funktion des Gesamt-Systems
        
    Beispiel:
        >>> from regelung import PT1, series_connection
        >>> s1 = PT1(K=2, T=1.0)
        >>> s2 = PT1(K=3, T=0.5)
        >>> system = series_connection(s1, s2)
        >>> # Entspricht K=2×3=6 mit komplexer Dynamik
    """
    tfs = [sys.tf() if hasattr(sys, 'tf') else sys for sys in systems]
    
    result = tfs[0]
    for tf in tfs[1:]:
        result = series(result, tf)
    
    return result
