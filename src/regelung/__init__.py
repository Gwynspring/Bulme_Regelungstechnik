"""Regelungstechnik-Bibliothek"""

from regelung.regler import PI, PID, P
from regelung.simulation import (
    closed_loop,
    plot_signal,
    plot_step,
    plot_step_with_metrics,
    series_connection,
    simulate_signal,
    simulate_step,
    simulate_step_scaled,
)
from regelung.strecken import DT1, IT1, PT1, PT2, D, I, Totzeit

__version__ = "0.1.0"

__all__ = [
    # Regler
    "P",
    "PI",
    "PID",
    # Strecken
    "PT1",
    "PT2",
    "Totzeit",
    "D",
    "DT1",
    "I",
    "IT1",
    # Simulation
    "closed_loop",
    "simulate_step",
    "simulate_signal",
    "simulate_step_scaled",
    "series_connection",
    # Plot
    "plot_step",
    "plot_step_with_metrics",
    "plot_signal",
]
