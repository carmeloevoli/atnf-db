import math
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('gryphon.mplstyle')

import numpy as np

from utils import Pdot_from_B, calculate_ages, compute_Edot, set_axes, savefig, load_data
from constants import MYR

def plot_galactic_plane(output_file='msp_galactic_plane.pdf', cmap='jet'):
    """Plot the distance of pulsars in the XY plane with color coded by age."""
    fig, ax = plt.subplots(figsize=(12.0, 8.5))
    set_axes(ax, xlabel='x [kpc]', ylabel='y [kpc]', xscale='linear', yscale='linear', xlim=[-15, 15], ylim=[-15, 15])

    # Load data from file
    P0, P1, DIST, XX, YY = load_data('atnf.txt')

    # Calculate log10 of age in Myr
    log_age = calculate_ages(P0, P1)

    # Select objects below a maximum period derivative (for B = 1e10)
    B_threshold = 1e10
    pdot_max = Pdot_from_B(P0, B_threshold)

    # Select objects below the maximum period derivative
    selected = P1 < pdot_max
    P0 = P0[selected]
    P1 = P1[selected]
    DIST = DIST[selected]
    XX = XX[selected]
    YY = YY[selected]
    log_age = log_age[selected]

    print(f"Age (log10) range: {min(log_age)}, {max(log_age)}")

    # Create scatter plot
    scatter = ax.scatter(XX, YY, c=log_age, cmap=cmap, vmin=1, vmax=5, s=20, edgecolors='none', alpha=0.7, marker='o')

    # Count objects with DIST < 5
    HALO_SIZE = 5.0
    mask = DIST < HALO_SIZE
    count = np.sum(mask)
    print(f"Number of objects with DIST < 5 kpc: {count}")
    EDOT = compute_Edot(P0, P1)

    ax.text(6, 12, fr'N($D < 5$ kpc) = {count}', fontsize=24, ha='center', va='center')
    # Compute mean EDOT and format as scientific notation with 10^exp
    mean_edot = np.mean(EDOT[mask])
    print(f"EDOT mean: {mean_edot:.3e}")
    ax.text(6, 9, fr'$\langle \dot E \rangle =$ {mean_edot:.1e} erg/s',
        fontsize=24, ha='center', va='center'
    )
    mean_P0 = np.mean(P0[mask])
    print(f"P0 mean: {mean_P0:.3f}")
    ax.text(6, 6, fr'$\langle P_0 \rangle$ = {mean_P0 / 1e-3:.0f} msec',
        fontsize=24, ha='center', va='center'
    )

    # Add colorbar for the age scale
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label(r'log age [Myr]')

    # Plot some guide lines and a circular boundary
    ax.hlines(0, -15, 15, lw=1, ls='--', color='tab:gray')
    ax.vlines(-8, -15, 15, lw=1, ls='--', color='tab:gray')

    # Draw a circle centered in -8,0 and with radius 5
    circle = plt.Circle((-8, 0), 5, color='tab:gray', fill=False, lw=1, ls='--')
    ax.add_artist(circle)

    #for i in range(len(XX)):
    #    print(f'{P0[i]}, {P1[i]}, {DIST[i]}, {XX[i]}, {YY[i]}, {LOGAGE[i]:.1f}')

    # Save the figure
    savefig(fig, output_file)

if __name__ == "__main__":
    plot_galactic_plane()
