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


