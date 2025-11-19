from abc import ABC, abstractmethod
from control import TransferFunction

class Controller(ABC):
    """Basis-Klasse für alle Regler"""
    @abstractmethod
    def tf(self) -> TransferFunction:
        pass

class P(Controller):
    def __init__(self, KP: float):
        self.KP = KP
        self._G = TransferFunction([KP], [1])
    
    def tf(self) -> TransferFunction:
        return self._G
    
    def __repr__(self):
        return f"P(KP={self.KP})"

class PI(Controller):
    def __init__(self, KP:float, TI:float):
        self.KP = KP
        self.TI = TI
        self._G = TransferFunction([KP*TI, KP], [TI, 0])

    def tf(self) -> TransferFunction:
        return self._G
    
    def __repr__(self):
        return f"P(KP={self.KP}, TI={self.TI})"

class PID(Controller):
    def __init__(self, KP:float, TI:float, TD: float):
        self.KP = KP
        self.TI = TI
        self.TD = TD
        self._G = TransferFunction([KP*TI*TD, KP*TI, KP], [TI, 0])

    def tf(self) -> TransferFunction:
        return self._G
    
    def __repr__(self):
        return f"P(KP={self.KP}, TI={self.TI}, TD={self.TD})"



