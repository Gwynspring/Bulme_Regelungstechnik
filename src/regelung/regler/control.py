from abc import ABC, abstractmethod

from control import TransferFunction


class Controller(ABC):
    """Basis-Klasse für alle Regler"""

    @abstractmethod
    def tf(self) -> TransferFunction:
        pass


class P(Controller):
    def __init__(self, Kp: float):
        self.Kp = Kp
        self.G = TransferFunction([Kp], [1])

    def tf(self) -> TransferFunction:
        return self.G

    def __repr__(self):
        return f"P(Kp={self.Kp})"


class PI(Controller):
    def __init__(self, Kp: float, Ti: float):
        self.Kp = Kp
        self.Ti = Ti
        self.G = TransferFunction([Kp * Ti, Kp], [Ti, 0])

    def tf(self) -> TransferFunction:
        return self.G

    def __repr__(self):
        return f"P(Kp={self.Kp}, Ti={self.Ti})"


class PID(Controller):
    def __init__(self, Kp: float, Ti: float, Td: float):
        self.Kp = Kp
        self.Ti = Ti
        self.Td = Td
        self.G = TransferFunction([Kp * Ti * Td, Kp * Ti, Kp], [Ti, 0])

    def tf(self) -> TransferFunction:
        return self.G

    def __repr__(self):
        return f"P(Kp={self.Kp}, Ti={self.Ti}, Td={self.Td})"
