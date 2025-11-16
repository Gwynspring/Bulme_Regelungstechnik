import matplotlib.pyplot as plt
import numpy as np 

def plot_step(t, y, title="Sprungantwort", save=None, show=True, 
              xlabel="Zeit [s]", ylabel="y(t)", figsize=(10, 6),
              show_input=False, u_amplitude=1.0):
    """
    Plottet Sprungantwort mit optionalem Eingangssignal.
    
    Args:
        ...
        show_input: Zeige Eingangssignal (default: False)
        u_amplitude: Amplitude des Sprungs (default: 1.0)
    """
    plt.figure(figsize=figsize)
    
    # Eingangssignal (optional)
    if show_input:
        u = np.ones_like(t) * u_amplitude
        u[t < 0] = 0
        plt.plot(t, u, 'r--', linewidth=2, alpha=0.7, label=f'Eingang u(t) = {u_amplitude}')
    
    # Ausgangssignal
    plt.plot(t, y, linewidth=2.5, color='#2E86AB', label='Ausgang y(t)')
    
    steady_state = y[-1]
    plt.axhline(y=steady_state, color='olive', linestyle='--', 
                linewidth=1, alpha=0.7, label=f'Endwert: {steady_state:.3f}')
    
    plt.axvline(x=0, color='gray', linestyle=':', linewidth=1, alpha=0.5)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.legend(loc='best')
    plt.tight_layout()
    
    if save:
        plt.savefig(save, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save}")
    
    if show:
        plt.show()
    else:
        plt.close()

def plot_step_with_metrics(t, y, title="Sprungantwort", save=None):
    """Plottet Sprungantwort mit Regelgütekriterien."""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Hauptplot
    ax.plot(t, y, linewidth=2.5, color='#2E86AB', label='y(t)')
    
    # Metriken berechnen
    steady_state = y[-1]
    overshoot_abs = np.max(y) - steady_state
    overshoot_pct = (overshoot_abs / steady_state * 100) if steady_state != 0 else 0
    
    # 2% Band für Ausregelzeit
    tolerance = 0.02 * abs(steady_state)
    settled_idx = np.where(np.abs(y - steady_state) <= tolerance)[0]
    settling_time = t[settled_idx[0]] if len(settled_idx) > 0 else t[-1]
    
    # Anstiegszeit (10% bis 90%)
    y_10 = 0.1 * steady_state
    y_90 = 0.9 * steady_state
    idx_10 = np.where(y >= y_10)[0][0] if np.any(y >= y_10) else 0
    idx_90 = np.where(y >= y_90)[0][0] if np.any(y >= y_90) else len(y)-1
    rise_time = t[idx_90] - t[idx_10]
    
    # Markierungen
    ax.axhline(y=steady_state, color='red', linestyle='--', 
               linewidth=1.5, alpha=0.7, label=f'Endwert: {steady_state:.3f}')
    
    # 2% Band
    ax.axhline(y=steady_state * 1.02, color='orange', linestyle=':', 
               linewidth=1, alpha=0.5)
    ax.axhline(y=steady_state * 0.98, color='orange', linestyle=':', 
               linewidth=1, alpha=0.5, label='±2% Band')
    
    # Ausregelzeit
    if settling_time < t[-1]:
        ax.axvline(x=settling_time, color='green', linestyle='--', 
                   linewidth=1.5, alpha=0.7, label=f'T_s: {settling_time:.2f}s')
    
    # Überschwingen
    if overshoot_abs > 0:
        max_idx = np.argmax(y)
        ax.plot(t[max_idx], y[max_idx], 'ro', markersize=8)
        ax.annotate(f'Max: {overshoot_pct:.1f}%', 
                    xy=(t[max_idx], y[max_idx]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Textbox mit Metriken
    metrics_text = (
        f"Metriken:\n"
        f"Endwert: {steady_state:.3f}\n"
        f"Überschwingen: {overshoot_pct:.1f}%\n"
        f"Ausregelzeit: {settling_time:.2f}s\n"
        f"Anstiegszeit: {rise_time:.2f}s"
    )

    ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes,
            verticalalignment='top', bbox=dict(boxstyle='round', 
            facecolor='wheat', alpha=0.8), fontsize=10, fontfamily='monospace')
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Zeit [s]", fontsize=12)
    ax.set_ylabel("y(t)", fontsize=12)
    ax.legend(loc='right', fontsize=10)
    
    plt.tight_layout()
    
    if save:
        plt.savefig(save, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save}")
    
    plt.show()

def plot_signal(t, y, u=None, title="Signalverlauf", save=None, show=True,
                xlabel="Zeit [s]", ylabel="Signal", figsize=(12, 6)):
    """
    Plottet beliebige Ein- und Ausgangssignale.
    
    Args:
        t: Zeitvektor
        y: Ausgangssignal
        u: Eingangssignal (optional)
        title: Titel des Plots
        save: Pfad zum Speichern
        show: Plot anzeigen
        xlabel: Label der x-Achse
        ylabel: Label der y-Achse
        figsize: Größe der Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Eingangssignal (optional)
    if u is not None:
        ax.plot(t, u, 'r--', linewidth=2, alpha=0.7, label='Eingang u(t)')
    
    # Ausgangssignal
    ax.plot(t, y, 'b-', linewidth=2.5, label='Ausgang y(t)')
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(loc='best', fontsize=11)
    
    plt.tight_layout()
    
    if save:
        plt.savefig(save, dpi=300, bbox_inches='tight')
        print(f"✓ Plot gespeichert: {save}")
    
    if show:
        plt.show()
    else:
        plt.close()
