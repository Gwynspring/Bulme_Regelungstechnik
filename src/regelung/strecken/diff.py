from control import TransferFunction


class D:
    """
    D-Strecke : G(s) = Kd * s
    """

    def __init__(self, Kd: float):
        self.Kd = Kd
        self.G = TransferFunction([Kd, 0], [1])

    def tf(self):
        return self.G


class DT1:
    """
    DT1-Strecke : G(s) = (Kd * s) / (1 + T1 * s)
    """

    def __init__(self, Kd: float, T1: float):
        self.Kd = Kd
        self.T1 = T1
        self.G = TransferFunction([Kd, 0], [T1, 1])

    def tf(self):
        return self.G
