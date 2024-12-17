import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 14
num_plots = 6
params = {
    'figure.figsize': (6 * 1.618, 6),  # Figure size
    'axes.labelsize': fontsize,        # Axis label size
    'axes.titlesize': fontsize,        # Title size
    'xtick.labelsize': fontsize,       # X-axis tick label size
    'ytick.labelsize': fontsize,       # Y-axis tick label size
    'legend.fontsize': fontsize,       # Legend font size
}
plt.rcParams.update(params)

# Fourier sine series for a square wave
def ff(x, iter=1000,a=1, omega=2 * np.pi, phi=0):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += ((2 / (k * np.pi))**2) * np.cos(k * x * omega + phi)
    return a*f

# Analytical square wave
def triangwave(x, a, omega=2 * np.pi, phi=0):
    return a * (1-(2/np.pi)*np.arccos(np.cos(x * omega + phi)))

# Residuals: Difference between square wave and Fourier series
def residuals(x, a, iter, omega=2 * np.pi, phi=0):
    return triangwave(x, a, omega, phi) - ff(x, iter, omega, phi)

# Parameters
iter = np.logspace(1, num_plots, num_plots, base=10)  # Logarithmically spaced
res_im = 10000
xx = np.linspace(-1, 1, res_im)

########## Create layout for subplots
fig, axes = plt.subplots(int(num_plots / 2), 2, sharex=True)  # Share axes
axes = axes.flatten()  # Flatten the array for easier iteration

# Iterate through subplots
for i, ax in enumerate(axes):
    if i % 2 == 0:
        iter_value = int(iter[i])
        iteration = int(1 + np.floor(iter_value / 2))  # Kind of wave we are working on
        ax.plot(xx, ff(xx, iter=iteration), label=f'N={iter_value}')
        ax.grid(True)
        ax.legend(loc='upper right')
    if i % 2 == 1:
        iter_value = int(iter[i])
        iteration = int(iter_value / 10)  # Kind of wave we are working on
        ax.plot(xx, residuals(xx, a=0.5, iter=iteration), label=f'N={iteration}')
        ax.grid(True)
        ax.legend(loc='upper right')

# Add shared labels for x and y
fig.text(0.5, 0.02, 'x', ha='center', fontsize=fontsize)  # Slightly lower x-axis label
fig.text(0.02, 0.5, 'f(x)', va='center', rotation='vertical', fontsize=fontsize)  # Slightly left y-axis label
plt.savefig(filepath + "foutriawave.png")  # Save the plot


plt.show()
