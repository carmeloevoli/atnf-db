import math
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pyplot as plt
plt.style.use('gryphon.mplstyle')

import numpy as np

from utils import set_axes, savefig, scale_size
from constants import GYR

# REFERENCE:
# https://www.cv.nrao.edu/~sransom/web/Ch6.html

def Pdot_to_Edot(period, period_dot):
    """Calculate spin-down energy loss rate (Edot) from period (Pdot)."""
    I = 1e45 # gr cm^2
    return 4. * math.pi**2. * I * period_dot / period**3

def load_data(filename):
    """Load data from a file and handle potential errors."""
    try:
        P0, P1 = np.loadtxt(filename, usecols=(0, 1), unpack=True)
        mask = P1 > 0
        return P0[mask], P1[mask]
    except Exception as e:
        print(f"Error loading data from {filename}: {e}")
        return None, None

def plot_age_lines(ax, period, age_threshold = 1e-2):
    """Plot lines of constant age on the P-Pdot diagram."""
    ages = np.array([1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1e-0, 1e1, 1e2, 1e3]) * GYR
    labels = [r'1 kyr', '', '', r'1 Myr', '', '', r'1 Gyr', '', '', r'$10^{3}$ Gyr']
    for age, label in zip(ages, labels):
        Pdot = period / (2.0 * age) # Calculate Pdot from period and age
        ax.plot(period, Pdot, '--', color='tab:gray', lw=1, alpha=0.75, zorder=10)
        ax.text(15.0, Pdot[660], label, color='tab:gray', ha='center', va='bottom',
                fontsize=16, rotation=20, zorder=10)
    Pdot = period / (2.0 * age_threshold * GYR)
    ax.plot(period, Pdot, '-', color='tab:gray', lw=2.2, alpha=0.75, zorder=10, label=r'$B = 10^{10}$ G')

def plot_bfield_lines(ax, period, B_threshold = 1e10):
    """Plot lines of constant magnetic field strength on the P-Pdot diagram."""
    bfields = np.array([1e8, 1e9, 1e10, 1e11, 1e12, 1e13])
    labels = [r'$10^{8}$ G', r'$10^{9}$ G', r'$10^{10}$ G', r'$10^{11}$ G', r'$10^{12}$ G', r'$10^{13}$ G']
    B_critical = 3.2e19  # Critical magnetic field strength in Gauss
    for B, label in zip(bfields, labels):
        Pdot = (B / B_critical)**2 / period
        ax.plot(period, Pdot, '--', color='tab:gray', lw=1, alpha=0.75, zorder=10)
        ax.text(2e-3, Pdot[70], label, color='tab:gray', ha='center', va='bottom',
                fontsize=16, rotation=-20, zorder=10)
    Pdot = (B_threshold / B_critical)**2 / period
    ax.plot(period, Pdot, '-', color='tab:gray', lw=2.2, alpha=0.75, zorder=10, label=r'$B = 10^{10}$ G')

def plot_ppdot(filename, output_file='ATNF_PPDOT.pdf', cmap='jet'):
    """Main function to plot the P-Pdot diagram using data from the ATNF pulsar database."""
    fig, ax = plt.subplots(figsize=(11.5, 8.5))
    set_axes(ax, xlabel='Period [s]', ylabel='Period derivative', xlim=[1e-3, 40], ylim=[1e-22, 1e-9])

    # Load data from file
    P0, P1 = load_data(filename)
    EDOT = np.log10(Pdot_to_Edot(P0, P1))

    # Scale the size of dots based on EDOT values
    #scaled_sizes = scale_size(EDOT, 29, 38)

    # Create scatter plot with color based on EDOT
    scatter = ax.scatter(P0, P1, s=30, c=EDOT, cmap=cmap, vmin=29, vmax=38,
                          edgecolors='none', alpha=0.7, marker='o', zorder=5)

    # Add a colorbar to indicate log EDOT values
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label(r'log $\dot E$ [erg s$^{-1}$]')

    # Define period range for plotting lines
    period = np.logspace(-3, 2, 1000)

    # Plot lines of constant age
    plot_age_lines(ax, period)

    # Plot lines of constant magnetic field strength
    plot_bfield_lines(ax, period)

    # Save the figure as a PDF
    savefig(fig, output_file)

if __name__ == "__main__":
    plot_ppdot('atnf.txt')