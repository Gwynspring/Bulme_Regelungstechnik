from control import TransferFunction

class PT1:
    """
    PT1-Regelstrecke: G(s) = K / (T s + 1)
    """
    def __init__(self, K: float, T: float):
        self.K = K
        self.T = T
        self.G = TransferFunction([K], [T, 1])

    def tf(self):
        return self.G

class PT2:
    """
    PT2-Regelstrecke: G(s) = K / ((T1 s + 1)(T2 s + 1))
    """
    def __init__(self, K: float, T1: float, T2: float):
        self.K = K
        self.T1 = T1
        self.T2 = T2
        self.G = TransferFunction(
            [K],
            [T1*T2, T1 + T2, 1]
        )

    def tf(self):
        return self.G

class I:
    """
    I-Regelstrecke (Integrator): G(s) = KI / s = 1 / (TI·s)
    
    Übertragungsfunktion: 
    - Mit KI: G(s) = KI / s
    - Mit TI: G(s) = 1 / (TI·s)
    
    Zusammenhang: KI = 1/TI
    """
    
    def __init__(self, KI: float):
        """
        Erstellt I-Strecke mit Integrierverstärkung.
        
        Args:
            KI: Integrierverstärkung
        """
        self.KI = KI
        self.TI = 1.0 / KI
        self.G = TransferFunction([self.KI], [1, 0])
    
    @classmethod
    def from_TI(cls, TI: float):
        """
        Erstellt I-Strecke aus Integrierzeitkonstante.
        
        Args:
            TI: Integrierzeitkonstante
            
        Returns:
            I-Strecke mit KI = 1/TI
            
        Beispiel:
            >>> strecke = I.from_TI(0.5)  # Ergibt KI=2.0
        """
        KI = 1.0 / TI
        return cls(KI)
    
    def tf(self):
        return self.G
    
    def __repr__(self):
        return f"I(KI={self.KI:.3f}, TI={self.TI:.3f})"

from control import TransferFunction

class IT1:
    """
    IT1-Regelstrecke: G(s) = KI / (s·(T1·s + 1))
    
    Kombination aus Integrator und PT1-Glied.
    
    Übertragungsfunktion:
    - G(s) = KI / (s·(T1·s + 1))
    
    Zusammenhang: KI = 1/TI
    """
    
    def __init__(self, T1: float, KI: float):
        """
        Erstellt IT1-Strecke mit Integrierverstärkung.
        
        Args:
            T1: Zeitkonstante des PT1-Glieds
            KI: Integrierverstärkung
            
        Beispiel:
            >>> strecke = IT1(T1=2.0, KI=1.5)
        """
        self.T1 = T1
        self.KI = KI
        self.TI = 1.0 / KI
        self.G = TransferFunction([self.KI], [T1, 1, 0])
    
    @classmethod
    def from_TI(cls, T1: float, TI: float):
        """
        Erstellt IT1-Strecke aus Integrierzeitkonstante.
        
        Args:
            T1: Zeitkonstante des PT1-Glieds
            TI: Integrierzeitkonstante
            
        Returns:
            IT1-Strecke mit KI = 1/TI
            
        Beispiel:
            >>> strecke = IT1.from_TI(T1=2.0, TI=0.67)
        """
        KI = 1.0 / TI
        return cls(T1=T1, KI=KI)
    
    def tf(self):
        return self.G
    
    def __repr__(self):
        return f"IT1(T1={self.T1:.3f}, KI={self.KI:.3f}, TI={self.TI:.3f})"


