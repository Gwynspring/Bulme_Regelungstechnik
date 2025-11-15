# src/regelung/strecken/totzeit.py
from control import TransferFunction, series
import numpy as np

def add_deadtime(system_tf, Tt: float, order: int = 2):
    """
    Fügt Totzeit zu einem System hinzu.
    
    Verwendet Padé-Approximation für e^(-Tt·s).
    
    Args:
        system_tf: Transfer-Funktion des Systems
        Tt: Totzeit in Sekunden
        order: Ordnung der Padé-Approximation (1, 2, oder 3)
        
    Returns:
        Transfer-Funktion mit Totzeit: G(s) · e^(-Tt·s)
        
    Beispiel:
        >>> from regelung import PT1
        >>> from regelung.strecken.totzeit import add_deadtime
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> system = add_deadtime(strecke.tf(), Tt=0.5, order=2)
    """
    if Tt <= 0:
        return system_tf
    
    # Padé-Approximation nach Standard-Formeln
    # Quelle: Åström & Hägglund, "PID Controllers", 2nd ed.
    if order == 1:
        # (1 - Tt/2·s) / (1 + Tt/2·s)
        num = np.array([-Tt/2, 1])
        den = np.array([Tt/2, 1])
        
    elif order == 2:
        # (1 - Tt/2·s + Tt²/12·s²) / (1 + Tt/2·s + Tt²/12·s²)
        num = np.array([Tt**2/12, -Tt/2, 1])
        den = np.array([Tt**2/12, Tt/2, 1])
        
    elif order == 3:
        # (1 - Tt/2·s + Tt²/12·s² - Tt³/120·s³) / (1 + Tt/2·s + Tt²/12·s² + Tt³/120·s³)
        num = np.array([-Tt**3/120, Tt**2/12, -Tt/2, 1])
        den = np.array([Tt**3/120, Tt**2/12, Tt/2, 1])
        
    else:
        raise ValueError("order muss 1, 2 oder 3 sein!")
    
    # Erstelle Totzeit-Transferfunktion
    G_totzeit = TransferFunction(num, den)
    
    # Kombiniere System mit Totzeit
    return series(system_tf, G_totzeit)


class Totzeit:
    """
    Reines Totzeit-Glied: G(s) = e^(-Tt·s)
    
    Implementiert mit Padé-Approximation.
    """
    
    def __init__(self, Tt: float, order: int = 2):
        """
        Args:
            Tt: Totzeit in Sekunden
            order: Ordnung der Padé-Approximation (default: 2)
                   1 = erste Ordnung (weniger genau)
                   2 = zweite Ordnung (empfohlen)
                   3 = dritte Ordnung (sehr genau)
        """
        self.Tt = Tt
        self.order = order
        
        # Padé-Approximation
        if order == 1:
            num = np.array([-Tt/2, 1])
            den = np.array([Tt/2, 1])
        elif order == 2:
            num = np.array([Tt**2/12, -Tt/2, 1])
            den = np.array([Tt**2/12, Tt/2, 1])
        elif order == 3:
            num = np.array([-Tt**3/120, Tt**2/12, -Tt/2, 1])
            den = np.array([Tt**3/120, Tt**2/12, Tt/2, 1])
        else:
            raise ValueError("order muss 1, 2 oder 3 sein!")
        
        self.G = TransferFunction(num, den)
    
    def tf(self):
        return self.G
    
    def __repr__(self):
        return f"Totzeit(Tt={self.Tt:.3f}s, order={self.order})"
