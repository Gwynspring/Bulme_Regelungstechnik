from control import TransferFunction

class D:
    """
    D-Strecke : G(s) = KD * s
    """
    def __init__(self, KD: float):
        self.KD = KD
        self.G = TransferFunction([KD, 0], [1])

    def tf(self):
        return self.G

class DT1:
    """
    DT1-Strecke : G(s) = (KD * s) / (1 + T1 * s)
    """
    def __init__(self, KD: float, T1: float):
        self.KD = KD
        self.T1 = T1
        self.G = TransferFunction([KD, 0], [T1, 1])

    def tf(self):
        return self.G

