from control import TransferFunction

class D:
    """
    D-Strecke : G(s) = K * s
    """
    def __init__(self, K: float):
        self.K = K
        self.G = TransferFunction([K, 0], [1])

    def tf(self):
        return self.G

class DT1:
    """
    DT1-Strecke : G(s) = (K * s) / (1 + T1 * s)
    """
    def __init__(self, K: float, T1: float):
        self.K = K
        self.T1 = T1
        self.G = TransferFunction([K, 0], [T1, 1])

    def tf(self):
        return self.G

