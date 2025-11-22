"""Regelstrecken-Modelle"""

from regelung.strecken.diff import DT1, D
from regelung.strecken.int import IT1, I
from regelung.strecken.pt import PT1, PT2
from regelung.strecken.totzeit import Totzeit

__all__ = ["PT1", "PT2", "I", "IT1", "Totzeit", "D", "DT1"]
