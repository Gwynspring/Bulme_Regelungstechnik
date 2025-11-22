"""
Tests für Simulation und Regelkreis

Copyright (c) 2025 Gwynspring
Licensed under MIT License
"""

import numpy as np
import pytest

from regelung import PI, PT1, P, closed_loop, simulate_signal, simulate_step


class TestClosedLoop:
    """Tests für geschlossene Regelkreise"""

    def test_closed_loop_creation(self):
        """Test: Regelkreis erstellen"""
        regler = P(Kp=1.0)
        strecke = PT1(Kp=1.0, T=1.0)
        system = closed_loop(regler, strecke)

        assert system is not None

    def test_closed_loop_stability(self):
        """Test: Stabiler Regelkreis"""
        regler = P(Kp=0.5)
        strecke = PT1(Kp=1.0, T=1.0)
        system = closed_loop(regler, strecke)

        # Alle Pole sollten negative Realteile haben
        poles = system.poles()
        assert all(np.real(p) < 0 for p in poles)

    def test_closed_loop_dc_gain(self):
        """Test: Regelkreis DC-Verstärkung"""
        regler = P(Kp=1.0)
        strecke = PT1(Kp=1.0, T=1.0)
        system = closed_loop(regler, strecke)

        # Mit P-Regler: stationäre Abweichung
        dc_gain = system.dcgain()
        assert 0 < dc_gain <= 1.0


class TestSimulateStep:
    """Tests für Sprungantwort-Simulation"""

    def test_simulate_step_pt1(self):
        """Test: PT1 Sprungantwort"""
        strecke = PT1(Kp=1.0, T=1.0)
        t, y = simulate_step(strecke.tf())

        # Grundlegende Checks
        assert len(t) > 0
        assert len(y) > 0
        assert len(t) == len(y)
        assert t[0] == 0.0
        assert y[0] >= 0.0  # Startwert

    def test_simulate_step_reaches_steady_state(self):
        """Test: System erreicht stationären Wert"""
        strecke = PT1(Kp=2.0, T=1.0)
        t, y = simulate_step(strecke.tf(), t_end=20.0)

        # Endwert sollte nahe K sein (für PT1 mit Sprung)
        assert np.isclose(y[-1], 2.0, rtol=0.05)

    def test_simulate_step_custom_time(self):
        """Test: Benutzerdefinierte Simulationszeit"""
        strecke = PT1(Kp=1.0, T=1.0)
        t, y = simulate_step(strecke.tf(), t_end=5.0)

        assert t[-1] <= 5.0

    def test_simulate_step_integrator(self):
        """Test: Integrator-Sprungantwort (Rampe)"""
        from regelung import I
        strecke = I(Ki=1.0)
        t, y = simulate_step(strecke.tf(), t_end=5.0)

        # Integrator sollte linear ansteigen
        assert y[-1] > y[0]
        # Grobe Linearitätsprüfung
        assert y[-1] > 0.9 * t[-1]  # Sollte etwa linear sein


class TestSimulateSignal:
    """Tests für beliebige Signal-Simulation"""

    def test_simulate_signal_custom(self):
        """Test: Simulation mit benutzerdefiniertem Signal"""
        strecke = PT1(Kp=1.0, T=1.0)
        t = np.linspace(0, 5, 100)
        u = np.sin(t)  # Sinus-Signal

        t_out, y = simulate_signal(strecke.tf(), t, u)

        assert len(t_out) > 0
        assert len(y) > 0

    def test_simulate_signal_constant(self):
        """Test: Konstantes Eingangssignal"""
        strecke = PT1(Kp=2.0, T=1.0)
        t = np.linspace(0, 10, 100)
        u = np.ones_like(t) * 3.0  # Konstant 3.0

        t_out, y = simulate_signal(strecke.tf(), t, u)

        # Endwert sollte K*u = 2*3 = 6 sein
        assert np.isclose(y[-1], 6.0, rtol=0.1)


class TestControlLoop:
    """Integrationstests für komplette Regelkreise"""

    def test_p_controller_steady_state_error(self):
        """Test: P-Regler hat stationäre Regelabweichung"""
        regler = P(Kp=2.0)
        strecke = PT1(Kp=1.0, T=1.0)
        system = closed_loop(regler, strecke)

        t, y = simulate_step(system, t_end=20.0)

        # Mit P-Regler: y_inf < 1 (stationäre Abweichung)
        assert y[-1] < 1.0
        assert y[-1] > 0.5  # Aber sollte nah dran sein

    def test_pi_controller_no_steady_state_error(self):
        """Test: PI-Regler eliminiert stationäre Regelabweichung"""
        regler = PI(Kp=2.0, Ti=1.0)
        strecke = PT1(Kp=1.0, T=1.0)
        system = closed_loop(regler, strecke)

        t, y = simulate_step(system, t_end=30.0)

        # PI-Regler sollte y_inf = 1 erreichen
        assert np.isclose(y[-1], 1.0, rtol=0.01)

    def test_high_gain_oscillation(self):
        """Test: Hohe Verstärkung kann Schwingungen verursachen"""
        regler = P(Kp=10.0)
        strecke = PT1(Kp=1.0, T=1.0)
        system = closed_loop(regler, strecke)

        t, y = simulate_step(system, t_end=10.0)

        # System sollte immer noch stabil sein
        poles = system.poles()
        assert all(np.real(p) < 0 for p in poles)


class TestEdgeCases:
    """Grenzfälle und Fehlerbehandlung"""

    def test_zero_time_array(self):
        """Test: Leere Zeitarray"""
        strecke = PT1(Kp=1.0, T=1.0)
        t = np.array([])
        u = np.array([])

        # Sollte Fehler werfen oder leere Arrays zurückgeben
        with pytest.raises((ValueError, IndexError)):
            simulate_signal(strecke.tf(), t, u)

    def test_mismatched_arrays(self):
        """Test: t und u haben unterschiedliche Längen"""
        strecke = PT1(Kp=1.0, T=1.0)
        t = np.linspace(0, 5, 100)
        u = np.ones(50)  # Falsche Länge

        with pytest.raises((ValueError, AssertionError)):
            simulate_signal(strecke.tf(), t, u)
