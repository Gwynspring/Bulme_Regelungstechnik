from control import TransferFunction, pade


class Totzeit:
    """
    Totzeit-Approximation mit Padé-Approximation.

    Eine ideale Totzeit G(s) = e^(-Tt·s) wird durch eine rationale
    Funktion approximiert.

    Args:
        Tt: Totzeit in Sekunden
        order: Ordnung der Padé-Approximation (default: 2)

    Beispiel:
        >>> from regelung import Totzeit, simulate_signal
        >>> import numpy as np
        >>>
        >>> totzeit = Totzeit(Tt=1.5, order=3)
        >>> t = np.linspace(0, 10, 1000)
        >>> u = np.ones_like(t)
        >>> t_out, y = simulate_signal(totzeit.tf(), t, u)
    """

    def __init__(self, Tt: float, order: int = 2):
        self.Tt = Tt
        self.order = order

        # Padé-Approximation von python-control
        num, den = pade(Tt, order)

        self.G = TransferFunction(num, den)

    def tf(self):
        """Gibt die Übertragungsfunktion zurück."""
        return self.G

    def __repr__(self):
        return f"Totzeit(Tt={self.Tt}, order={self.order})"
