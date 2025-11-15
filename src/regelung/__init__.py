"""Regelungstechnik-Bibliothek"""

from regelung.regler import P, PI, PID
from regelung.strecken import PT1, PT2,Totzeit 
from regelung.simulation import (
    closed_loop, 
    simulate_step, 
    simulate_signal,
    simulate_step_scaled,
    plot_step,
    plot_step_with_metrics
)

__version__ = "0.1.0"

__all__ = [
    # Regler
    "P", "PI", "PID",
    # Strecken
    "PT1", "PT2", "Totzeit"
    # Simulation
    "closed_loop", 
    "simulate_step", 
    "simulate_signal",
    "simulate_step_scaled",
    # Plot
    "plot_step", 
    "plot_step_with_metrics"
]
