"""
Tests für Strecken-Implementierungen

Copyright (c) 2025 Gwynspring
Licensed under MIT License
"""

import numpy as np

from regelung import IT1, PT1, PT2, I


class TestPT1:
    """Tests für PT1-Strecke"""

    def test_pt1_creation(self):
        """Test: PT1-Strecke erstellen"""
        strecke = PT1(Kp=2.0, T=1.0)
        assert strecke is not None

    def test_pt1_transfer_function(self):
        """Test: PT1 Übertragungsfunktion"""
        strecke = PT1(Kp=2.0, T=1.0)
        tf = strecke.tf()

        # PT1: G(s) = K/(T*s + 1) = 2/(s + 1)
        assert len(tf.num[0][0]) == 1  # Konstante im Zähler
        assert len(tf.den[0][0]) == 2  # Nenner Grad 1

    def test_pt1_dc_gain(self):
        """Test: PT1 Gleichverstärkung (DC-Gain)"""
        K = 3.0
        strecke = PT1(Kp=K, T=1.0)
        tf = strecke.tf()

        # Bei s=0 sollte G(0) = K sein
        dc_gain = tf.dcgain()
        assert np.isclose(dc_gain, K, rtol=1e-5)


class TestPT2:
    """Tests für PT2-Strecke"""

    def test_pt2_creation(self):
        """Test: PT2-Strecke erstellen"""
        strecke = PT2(Kp=1.0, T1=2.0, T2=0.5)
        assert strecke is not None

    def test_pt2_transfer_function(self):
        """Test: PT2 Übertragungsfunktion"""
        strecke = PT2(Kp=1.0, T1=1.0, T2=1.0)
        tf = strecke.tf()

        # PT2: G(s) = K/((T1*s+1)(T2*s+1))
        assert len(tf.num[0][0]) == 1  # Konstante im Zähler
        assert len(tf.den[0][0]) == 3  # Nenner Grad 2

    def test_pt2_dc_gain(self):
        """Test: PT2 Gleichverstärkung"""
        K = 5.0
        strecke = PT2(Kp=K, T1=1.0, T2=2.0)
        tf = strecke.tf()

        dc_gain = tf.dcgain()
        assert np.isclose(dc_gain, K, rtol=1e-5)


class TestIntegrator:
    """Tests für I-Strecke (Integrator)"""

    def test_i_creation(self):
        """Test: I-Strecke erstellen"""
        strecke = I(Ki=1.0)
        assert strecke is not None

    def test_i_transfer_function(self):
        """Test: I Übertragungsfunktion"""
        strecke = I(Ki=2.0)
        tf = strecke.tf()

        # I: G(s) = K/s
        assert len(tf.num[0][0]) == 1  # Konstante im Zähler
        assert len(tf.den[0][0]) == 2  # [1, 0] im Nenner

        # Pol bei s=0
        poles = tf.poles()
        assert np.isclose(poles[0], 0.0, atol=1e-10)


class TestIT1:
    """Tests für IT1-Strecke"""

    def test_it1_creation(self):
        """Test: IT1-Strecke erstellen"""
        strecke = IT1(Ki=1.0, T1=1.0)
        assert strecke is not None

    def test_it1_transfer_function(self):
        """Test: IT1 Übertragungsfunktion"""
        strecke = IT1(Ki=1.0, T1=1.0)
        tf = strecke.tf()

        # IT1: G(s) = K/(s(T*s+1))
        assert len(tf.num[0][0]) == 1  # Konstante im Zähler
        assert len(tf.den[0][0]) == 3  # Nenner Grad 2

        # Ein Pol bei s=0
        poles = tf.poles()
        assert any(np.isclose(p, 0.0, atol=1e-10) for p in poles)


class TestStreckenEdgeCases:
    """Edge Cases für Strecken"""

    def test_negative_gain(self):
        """Test: Negative Verstärkung (invertierende Strecke)"""
        strecke = PT1(Kp=-1.0, T=1.0)
        tf = strecke.tf()
        assert tf.dcgain() < 0

    def test_very_fast_system(self):
        """Test: Sehr schnelles System (kleine T)"""
        strecke = PT1(Kp=1.0, T=0.001)
        assert strecke.tf() is not None

    def test_very_slow_system(self):
        """Test: Sehr langsames System (große T)"""
        strecke = PT1(Kp=1.0, T=1000.0)
        assert strecke.tf() is not None
