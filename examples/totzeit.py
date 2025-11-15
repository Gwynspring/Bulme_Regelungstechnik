# examples/totzeit.py
from regelung import PT1, simulate_step, plot_step
from regelung.strecken.totzeit import add_deadtime

def beispiel_totzeit_scipy():
    """Beispiel mit scipy.interpolate.pade"""
    strecke = PT1(K=3.0, T=1.3)
    
    # Ohne Totzeit
    t, y = simulate_step(strecke.tf(), t_end=15)
    plot_step(t, y,
              title="PT1: K=3.0, T=1.3 (ohne Totzeit)", 
              show_input=True, 
              u_amplitude=1)
    
    # Mit Totzeit (scipy wird automatisch verwendet)
    system = add_deadtime(strecke.tf(), Tt=5.0, order=2)
    t, y = simulate_step(system, t_end=10)
    plot_step(t, y,
              title="PT1: K=3.0, T=1.3 mit Totzeit Tt=5", 
              show_input=True, 
              u_amplitude=1)

if __name__ == "__main__":
    beispiel_totzeit_scipy()
