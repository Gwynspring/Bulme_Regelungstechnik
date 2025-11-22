from control import TransferFunction


class I:
    """
    I-Regelstrecke (Integrator): G(s) = Ki / s = 1 / (Ti·s)

    Übertragungsfunktion:
    - Mit Ki: G(s) = Ki / s
    - Mit Ti: G(s) = 1 / (Ti·s)

    Zusammenhang: Ki = 1/Ti
    """

    def __init__(self, Ki: float):
        """
        Erstellt I-Strecke mit Integrierverstärkung.

        Args:
            Ki: Integrierverstärkung
        """
        self.Ki = Ki
        self.Ti = 1.0 / Ki
        self.G = TransferFunction([self.Ki], [1, 0])

    @classmethod
    def from_Ti(cls, Ti: float):
        """
        Erstellt I-Strecke aus Integrierzeitkonstante.

        Args:
            Ti: Integrierzeitkonstante

        Returns:
            I-Strecke mit Ki = 1/Ti

        Beispiel:
            >>> strecke = I.from_Ti(0.5)  # Ergibt Ki=2.0
        """
        Ki = 1.0 / Ti
        return cls(Ki)

    def tf(self):
        return self.G

    def __repr__(self):
        return f"I(Ki={self.Ki:.3f}, Ti={self.Ti:.3f})"


class IT1:
    """
    IT1-Regelstrecke: G(s) = Ki / (s·(T1·s + 1))

    Kombination aus Integrator und PT1-Glied.

    Übertragungsfunktion:
    - G(s) = Ki / (s·(T1·s + 1))

    Zusammenhang: Ki = 1/Ti
    """

    def __init__(self, T1: float, Ki: float):
        """
        Erstellt IT1-Strecke mit Integrierverstärkung.

        Args:
            T1: Zeitkonstante des PT1-Glieds
            Ki: Integrierverstärkung

        Beispiel:
            >>> strecke = IT1(T1=2.0, Ki=1.5)
        """
        self.T1 = T1
        self.Ki = Ki
        self.Ti = 1.0 / Ki
        self.G = TransferFunction([self.Ki], [T1, 1, 0])

    @classmethod
    def from_Ti(cls, T1: float, Ti: float):
        """
        Erstellt IT1-Strecke aus Integrierzeitkonstante.

        Args:
            T1: Zeitkonstante des PT1-Glieds
            Ti: Integrierzeitkonstante

        Returns:
            IT1-Strecke mit Ki = 1/Ti

        Beispiel:
            >>> strecke = IT1.from_Ti(T1=2.0, Ti=0.67)
        """
        Ki = 1.0 / Ti
        return cls(T1=T1, Ki=Ki)

    def tf(self):
        return self.G

    def __repr__(self):
        return f"IT1(T1={self.T1:.3f}, Ki={self.Ki:.3f}, Ti={self.Ti:.3f})"
