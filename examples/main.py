from regelung import P, PI, PID, PT1, PT2
from regelung import closed_loop, simulate_step
from regelung import plot_step, plot_step_with_metrics

def beispiel_pt1_mit_p_regler():
    """Beispiel: PT1-Strecke mit P-Regler"""
    strecke = PT1(K=2.0, T=1.0)
    regler = P(Kp=1.5)
    
    system = closed_loop(regler, strecke)
    t, y = simulate_step(system)
    
    plot_step(t, y, 
             title="PT1 mit P-Regler")

def beispiel_pt2_mit_pid():
    """Beispiel: PT2-Strecke mit PID-Regler"""
    strecke = PT2(K=1.0, T1=2.0, T2=0.5)
    regler = PID(Kp=2.0, Ti=1.5, Td=0.3)
    
    system = closed_loop(regler, strecke)
    t, y = simulate_step(system)
    
    plot_step(t, y, 
             title="PT2 mit PID-Regler")

def beispiel_pt1_strecke():
    """Beispiel: PT1-Strecke ohne Regler (offener Kreis)"""
    strecke = PT1(K=1.0, T=2.0)
    
    # Direkt die Strecke simulieren (kein closed_loop!)
    t, y = simulate_step(strecke.tf())
    
    plot_step(t, y, 
             title="PT1-Strecke (offener Kreis)")

def beispiel_pt2_strecke():
    """Beispiel: PT2-Strecke ohne Regler"""
    strecke = PT2(K=1.0, T1=2.0, T2=0.5)
    
    t, y = simulate_step(strecke.tf())
    
    plot_step(t, y, 
             title="PT2-Strecke (offener Kreis)")

# Einfacher Plot
def beispiel_einfach():
    strecke = PT1(K=2.0, T=1.0)
    t, y = simulate_step(strecke.tf())
    plot_step(t, y, title="PT1-Strecke")

# Mit Metriken
def beispiel_mit_metriken():
    strecke = PT2(K=1.0, T1=2.0, T2=0.5)
    regler = PID(Kp=2.0, Ti=1.5, Td=0.3)
    system = closed_loop(regler, strecke)
    t, y = simulate_step(system)
    plot_step_with_metrics(t, y, 
                          title="PT2 mit PID-Regler")

if __name__ == "__main__":
    beispiel_einfach()
    beispiel_pt1_strecke()
    beispiel_mit_metriken()
