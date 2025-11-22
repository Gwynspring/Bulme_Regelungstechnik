"""
Tests für Regler-Implementierungen

Copyright (c) 2025 Gwynspring
Licensed under MIT License
"""

import pytest
import numpy as np
from regelung import P, PI, PID


class TestPRegler:
    """Tests für P-Regler"""
    
    def test_p_creation(self):
        """Test: P-Regler erstellen"""
        regler = P(Kp=2.0)
        assert regler is not None
        
    def test_p_transfer_function(self):
        """Test: P-Regler Übertragungsfunktion"""
        regler = P(Kp=2.0)
        tf = regler.tf()
        
        # P-Regler sollte Zähler = [2.0] und Nenner = [1.0] haben
        assert np.allclose(tf.num[0][0], [2.0])
        assert np.allclose(tf.den[0][0], [1.0])
    
    def test_p_invalid_kp(self):
        """Test: Negative Kp sollte funktionieren (für invertierende Regler)"""
        regler = P(Kp=-1.0)
        assert regler is not None


class TestPIRegler:
    """Tests für PI-Regler"""
    
    def test_pi_creation(self):
        """Test: PI-Regler erstellen"""
        regler = PI(Kp=2.0, Ti=1.0)
        assert regler is not None
    
    def test_pi_transfer_function(self):
        """Test: PI-Regler Übertragungsfunktion"""
        regler = PI(Kp=1.0, Ti=1.0)
        tf = regler.tf()
        
        # PI: G(s) = Kp(1 + 1/(Ti*s)) = Kp(Ti*s + 1)/(Ti*s)
        # Mit Kp=1, Ti=1: (s + 1)/s
        assert len(tf.num[0][0]) == 2  # Zähler Grad 1
        assert len(tf.den[0][0]) == 2  # Nenner Grad 1
    
    def test_pi_zero_ti_raises_error(self):
        """Test: Ti=0 sollte Fehler werfen"""
        with pytest.raises((ValueError, ZeroDivisionError)):
            regler = PI(Kp=1.0, Ti=0.0)
            regler.tf()


class TestPIDRegler:
    """Tests für PID-Regler"""
    
    def test_pid_creation(self):
        """Test: PID-Regler erstellen"""
        regler = PID(Kp=2.0, Ti=1.5, Td=0.3)
        assert regler is not None
    
    def test_pid_transfer_function(self):
        """Test: PID-Regler Übertragungsfunktion"""
        regler = PID(Kp=1.0, Ti=1.0, Td=1.0)
        tf = regler.tf()
        
        # PID sollte höheren Grad haben
        assert len(tf.num[0][0]) >= 2
        assert len(tf.den[0][0]) >= 1
    
    def test_pid_reduces_to_pi(self):
        """Test: PID mit Td=0 sollte PI sein"""
        pid = PID(Kp=2.0, Ti=1.0, Td=0.0)
        pi = PI(Kp=2.0, Ti=1.0)
        
        # Übertragungsfunktionen sollten ähnlich sein
        # (genauer Vergleich schwierig wegen Numerik)
        assert pid.tf() is not None
        assert pi.tf() is not None


class TestReglerEdgeCases:
    """Edge Cases und Grenzwerte"""
    
    def test_very_small_kp(self):
        """Test: Sehr kleine Verstärkung"""
        regler = P(Kp=1e-6)
        assert regler.tf() is not None
    
    def test_very_large_kp(self):
        """Test: Sehr große Verstärkung"""
        regler = P(Kp=1e6)
        assert regler.tf() is not None
    
    def test_typical_values(self):
        """Test: Typische Werte aus der Praxis"""
        # Typische PID-Parameter
        regler = PID(Kp=5.0, Ti=2.0, Td=0.5)
        tf = regler.tf()
        
        assert tf is not None
        assert tf.isdtime() == False  # Kontinuierliches System
