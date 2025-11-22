import math

from control import TransferFunction


class PT1:
    """
    PT1-Regelstrecke: G(s) = Kp / (T s + 1)

    Args:
        Kp (float): Verstärkung
        T (float): Zeitkonstante

    Returns:
        PT1-Übertragungsfunktion
    """

    def __init__(self, Kp: float, T: float):
        self.Kp = Kp
        self.T = T
        self.G = TransferFunction([Kp], [T, 1])

    def tf(self):
        return self.G


class PT2:
    """
    PT2-Regelstrecke:

    Allgemeine Form:
        G(s) = Kp / ((T1 s + 1)(T2 s + 1))

    Standardform:
        G(s) = Kp / (T² s² + 2 D T s + 1)

    Args:
        Kp (float): Verstärkung
        T1 (float): Zeitkonstante 1
        T2 (float): Zeitkonstante 2

    Returns:
        PT2-Übertragungsfunktion
    """

    def __init__(self, Kp: float, T1: float, T2: float):
        self.Kp = Kp
        self.T1 = T1
        self.T2 = T2
        self.G = TransferFunction([Kp], [T1 * T2, T1 + T2, 1])

    @classmethod
    def from_damping(cls, Kp: float, D: float, T: float):
        """
        PT2-Strecke aus Dämpfung D und Zeitkonstante T.

        Standardform:
            G(s) = Kp / (T² s² + 2 D T s + 1)

        Args:
            Kp (float): Verstärkung
            D (float): Dämpfungsbeiwert
            T (float): Zeitkonstante

        Returns:
            PT2-Objekt in der Standardform
        """
        a2 = T * T
        a1 = 2 * D * T
        a0 = 1

        G = TransferFunction([Kp], [a2, a1, a0])

        obj = cls.__new__(cls)
        obj.Kp = Kp
        obj.T1 = None
        obj.T2 = None
        obj.G = G
        return obj

    def tf(self):
        return self.G

    @staticmethod
    def identify_from_step(h1: float, h_inf: float, t1: float):
        """
        Berechnet Dämpfung D und Zeitkonstante T aus Messwerten einer Sprungantwort.

        Args:
            h1 (float): Erster Peak der Sprungantwort
            h_inf (float): Endwert der Sprungantwort
            t1 (float): Zeit des ersten Peaks

        Returns:
            (D, T): Tupel aus Dämpfung und Zeitkonstante

        Formeln:
            D = - ln((h1/h_inf) - 1) / sqrt(pi² + (ln((h1/h_inf) - 1))²)
            T = t1 * sqrt(1 - D²) / pi
        """

        x = (h1 / h_inf) - 1
        ln_term = math.log(x)

        D = -ln_term / math.sqrt(math.pi**2 + ln_term**2)
        T = t1 * math.sqrt(1 - D**2) / math.pi

        return D, T
