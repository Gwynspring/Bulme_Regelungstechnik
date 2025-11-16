"""Regelstrecken-Modelle"""

from regelung.strecken.pt import PT1, PT2
from regelung.strecken.int import I, IT1
from regelung.strecken.totzeit import Totzeit
from regelung.strecken.diff import D, DT1

__all__ = ["PT1", "PT2", "I", "IT1", "Totzeit", "D", "DT1"]
