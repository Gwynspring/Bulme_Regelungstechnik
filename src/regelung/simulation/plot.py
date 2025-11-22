"""
Visualisierungsfunktionen für Regelkreise.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_step(
    t,
    y,
    title="Sprungantwort",
    save=None,
    show=True,
    xlabel="Zeit [s]",
    ylabel="y(t)",
    figsize=(10, 6),
    show_input=False,
    u_amplitude=1.0,
    u_signal=None,
):
    """
    Plottet Sprungantwort oder beliebige Signale.

    Args:
        t: Zeitvektor
        y: Ausgangssignal
        title: Titel des Plots
        save: Pfad zum Speichern (optional)
        show: Plot anzeigen (True/False)
        xlabel: Label der x-Achse
        ylabel: Label der y-Achse
        figsize: Größe der Figure (width, height)
        show_input: Zeige Eingangssignal (default: False)
        u_amplitude: Amplitude des Sprungs (default: 1.0)
        u_signal: Beliebiges Eingangssignal (überschreibt u_amplitude)

    Beispiel:
        >>> from regelung import PT1, simulate_step, plot_step
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> t, y = simulate_step(strecke.tf())
        >>> plot_step(t, y, show_input=True, u_amplitude=1.0)
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Eingangssignal (optional)
    if show_input:
        if u_signal is not None:
            # Beliebiges Signal plotten
            ax.plot(t, u_signal, "r--", linewidth=2, alpha=0.7, label="Eingang u(t)")
        else:
            # Standard-Sprung
            u = np.ones_like(t) * u_amplitude
            u[t < 0] = 0
            ax.plot(
                t,
                u,
                "r--",
                linewidth=2,
                alpha=0.7,
                label=f"Eingang u(t) = {u_amplitude}",
            )

    # Ausgangssignal
    ax.plot(t, y, linewidth=2.5, color="#2E86AB", label="Ausgang y(t)")

    # Endwert-Linie
    steady_state = y[-1]
    ax.axhline(
        y=steady_state,
        color="olive",
        linestyle="--",
        linewidth=1,
        alpha=0.7,
        label=f"Endwert: {steady_state:.3f}",
    )

    # Vertikale Linie bei t=0
    ax.axvline(x=0, color="gray", linestyle=":", linewidth=1, alpha=0.5)

    # Styling
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(loc="best", fontsize=10)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=300, bbox_inches="tight")
        print(f"✓ Plot gespeichert: {save}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_step_with_metrics(
    t, y, title="Sprungantwort mit Metriken", save=None, show=True
):
    """
    Plottet Sprungantwort mit Regelgütekriterien.

    Args:
        t: Zeitvektor
        y: Ausgangssignal
        title: Titel des Plots
        save: Pfad zum Speichern (optional)
        show: Plot anzeigen (True/False)

    Zeigt automatisch:
        - Endwert (stationärer Wert)
        - Überschwingen in %
        - Ausregelzeit (2%-Kriterium)
        - Anstiegszeit (10%-90%)

    Beispiel:
        >>> from regelung import PT2, PID, closed_loop, simulate_step
        >>> from regelung import plot_step_with_metrics
        >>> strecke = PT2(K=1.0, T1=2.0, T2=0.5)
        >>> regler = PID(Kp=2.0, Ti=1.5, Td=0.3)
        >>> system = closed_loop(regler, strecke)
        >>> t, y = simulate_step(system)
        >>> plot_step_with_metrics(t, y, title="PT2 mit PID-Regler")
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Hauptplot
    ax.plot(t, y, linewidth=2.5, color="#2E86AB", label="y(t)")

    # Metriken berechnen
    steady_state = y[-1]
    max_value = np.max(y)
    overshoot_abs = max_value - steady_state
    overshoot_pct = (overshoot_abs / steady_state * 100) if steady_state != 0 else 0

    # 2% Band für Ausregelzeit
    tolerance = 0.02 * abs(steady_state)
    settled_idx = np.where(np.abs(y - steady_state) <= tolerance)[0]
    settling_time = t[settled_idx[0]] if len(settled_idx) > 0 else t[-1]

    # Anstiegszeit (10% bis 90%)
    y_10 = 0.1 * steady_state
    y_90 = 0.9 * steady_state

    try:
        idx_10 = np.where(y >= y_10)[0][0] if np.any(y >= y_10) else 0
        idx_90 = np.where(y >= y_90)[0][0] if np.any(y >= y_90) else len(y) - 1
        rise_time = t[idx_90] - t[idx_10]
    except IndexError:
        rise_time = 0

    # Markierungen im Plot
    # Endwert
    ax.axhline(
        y=steady_state,
        color="red",
        linestyle="--",
        linewidth=1.5,
        alpha=0.7,
        label=f"Endwert: {steady_state:.3f}",
    )

    # 2% Band
    if steady_state > 0:
        ax.axhline(
            y=steady_state * 1.02, color="orange", linestyle=":", linewidth=1, alpha=0.5
        )
        ax.axhline(
            y=steady_state * 0.98,
            color="orange",
            linestyle=":",
            linewidth=1,
            alpha=0.5,
            label="±2% Band",
        )

    # Ausregelzeit
    if settling_time < t[-1]:
        ax.axvline(
            x=settling_time,
            color="green",
            linestyle="--",
            linewidth=1.5,
            alpha=0.7,
            label=f"Ausregelzeit: {settling_time:.2f}s",
        )

    # Überschwingen markieren
    if overshoot_abs > tolerance:  # Nur wenn signifikant
        max_idx = np.argmax(y)
        ax.plot(t[max_idx], y[max_idx], "ro", markersize=8, zorder=5)
        ax.annotate(
            f"Überschwingen: {overshoot_pct:.1f}%",
            xy=(t[max_idx], y[max_idx]),
            xytext=(10, 10),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.7),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0"),
            fontsize=9,
        )

    # Textbox mit allen Metriken
    metrics_text = (
        f"Regelgütekriterien:\n"
        f"━━━━━━━━━━━━━━━━━\n"
        f"Endwert:        {steady_state:.4f}\n"
        f"Maximum:        {max_value:.4f}\n"
        f"Überschwingen:  {overshoot_pct:.2f}%\n"
        f"Ausregelzeit:   {settling_time:.3f}s\n"
        f"Anstiegszeit:   {rise_time:.3f}s"
    )

    ax.text(
        0.02,
        0.98,
        metrics_text,
        transform=ax.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.85),
        fontsize=10,
        fontfamily="monospace",
    )

    # Styling
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    ax.set_xlabel("Zeit [s]", fontsize=12)
    ax.set_ylabel("y(t)", fontsize=12)
    ax.legend(loc="right", fontsize=10)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=300, bbox_inches="tight")
        print(f"✓ Plot gespeichert: {save}")

    if show:
        plt.show()
    else:
        plt.close()


def plot_signal(
    t,
    y,
    u=None,
    title="Signalverlauf",
    save=None,
    show=True,
    xlabel="Zeit [s]",
    ylabel="Signal",
    figsize=(12, 6),
):
    """
    Plottet beliebige Ein- und Ausgangssignale (Sinus, Rampe, etc.).

    Args:
        t: Zeitvektor
        y: Ausgangssignal
        u: Eingangssignal (optional, gleiche Länge wie t)
        title: Titel des Plots
        save: Pfad zum Speichern (optional)
        show: Plot anzeigen (True/False)
        xlabel: Label der x-Achse
        ylabel: Label der y-Achse
        figsize: Größe der Figure (width, height)

    Beispiel:
        >>> import numpy as np
        >>> from regelung import PT1, simulate_signal, plot_signal
        >>> strecke = PT1(K=2.0, T=1.0)
        >>> t = np.linspace(0, 10, 1000)
        >>> u = 5 * np.sin(2 * np.pi * 0.5 * t)  # 0.5 Hz Sinus
        >>> t_out, y = simulate_signal(strecke.tf(), t, u)
        >>> plot_signal(t_out, y, u=u, title="PT1 mit Sinus-Anregung")
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Eingangssignal (optional)
    if u is not None:
        ax.plot(t, u, "r--", linewidth=2, alpha=0.7, label="Eingang u(t)")

    # Ausgangssignal
    ax.plot(t, y, "b-", linewidth=2.5, label="Ausgang y(t)")

    # Styling
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.axhline(y=0, color="k", linewidth=0.5, alpha=0.5)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(loc="best", fontsize=11)

    plt.tight_layout()

    if save:
        plt.savefig(save, dpi=300, bbox_inches="tight")
        print(f"✓ Plot gespeichert: {save}")

    if show:
        plt.show()
    else:
        plt.close()


def get_step_metrics(t, y):
    """
    Berechnet Regelgütekriterien aus Sprungantwort.

    Args:
        t: Zeitvektor
        y: Ausgangssignal

    Returns:
        dict mit Metriken:
            - steady_state: Stationärer Endwert
            - t_max: Zeit beim Maximum
            - y_max: Maximaler Wert
            - overshoot_pct: Überschwingen in %
            - overshoot_abs: Absolutes Überschwingen
            - rise_time: Anstiegszeit (10%-90%)
            - settling_time: Ausregelzeit (2%-Kriterium)

    Beispiel:
        >>> from regelung import PT2, simulate_step, get_step_metrics
        >>> strecke = PT2(K=1.0, T1=2.0, T2=0.5)
        >>> t, y = simulate_step(strecke.tf())
        >>> metrics = get_step_metrics(t, y)
        >>> print(f"Überschwingen: {metrics['overshoot_pct']:.2f}%")
    """
    steady_state = y[-1]

    # Maximum
    max_idx = np.argmax(y)
    t_max = t[max_idx]
    y_max = y[max_idx]

    # Überschwingen
    overshoot_abs = y_max - steady_state
    overshoot_pct = (overshoot_abs / steady_state) * 100 if steady_state != 0 else 0

    # Anstiegszeit (10% bis 90%)
    y_10 = 0.1 * steady_state
    y_90 = 0.9 * steady_state

    try:
        idx_10 = np.where(y >= y_10)[0][0] if np.any(y >= y_10) else 0
        idx_90 = np.where(y >= y_90)[0][0] if np.any(y >= y_90) else len(y) - 1
        rise_time = t[idx_90] - t[idx_10]
    except IndexError:
        rise_time = 0

    # Ausregelzeit (2%-Kriterium)
    tolerance = 0.02 * abs(steady_state)
    settled_idx = np.where(np.abs(y - steady_state) <= tolerance)[0]
    settling_time = t[settled_idx[0]] if len(settled_idx) > 0 else t[-1]

    return {
        "steady_state": steady_state,
        "t_max": t_max,
        "y_max": y_max,
        "overshoot_pct": overshoot_pct,
        "overshoot_abs": overshoot_abs,
        "rise_time": rise_time,
        "settling_time": settling_time,
    }
