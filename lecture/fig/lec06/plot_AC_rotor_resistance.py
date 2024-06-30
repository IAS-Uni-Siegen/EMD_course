import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import os

# Use LaTeX for labels
rc('text', usetex=True)
rc('font', family='serif')
rc('font', size=18)

# Constants
mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability (H/m)
kappa = 3.7e7  # Conductivity of aluminium (S/m), adjust as needed
h_bar = 0.05  # Bar height (m), adjust as needed
w_bar = 0.01  # Bar width (m), adjust as needed
w_slot = 0.015  # Slot width (m), adjust as needed

# Slip frequency range
f_slip = np.linspace(0.1, 50, 100)  # 1/s

# Skin depth calculation
delta = h_bar * np.sqrt(np.pi * f_slip * mu_0 * kappa  * w_bar / w_slot)

# AC resistance ratio calculation
R_ratio = delta * (np.sinh(2 * delta) + np.sin(2 * delta)) / (np.cosh(2 * delta) - np.cos(2 * delta))

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(f_slip, R_ratio)
plt.xlabel(r'$f_\mathrm{slip}$ in Hz')
plt.ylabel(r'$\frac{R_\mathrm{r}(\omega_\mathrm{slip})}{R_\mathrm{r,DC}}$')
plt.grid(True)
plt.xlim([0, f_slip[-1]])
plt.ylim([1, R_ratio[-1]])
plt.tight_layout(pad=0)

# Save the figure as a PDF in the same folder as the script
current_directory = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(current_directory, 'AC_rotor_resistance.pdf')
plt.savefig(save_path, format='pdf')
plt.show()
