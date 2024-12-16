import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 14
num_plots=int(4)
params = {
    'figure.figsize': (6*1.618,6),  # Figure size
    'axes.labelsize': fontsize, # Axis label size
    'axes.titlesize': fontsize, # Title size
    'xtick.labelsize': fontsize, # X-axis tick label size
    'ytick.labelsize': fontsize, # Y-axis tick label size
    'legend.fontsize': fontsize, # Legend font size
}
plt.rcParams.update(params)

# Function for the Fourier series

def ff(x, iter=1000):
    """
    Fourier sine series for a square wave.

    Parameters:
    ----------
    x: (float) Value at which the function is evaluated
    iter: (int) Number of iterations

    Returns:
    -------
    f: (float) Value of the function at the given point
    """
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += ((2 / (k * np.pi))**2) * np.cos(k * x * np.pi)
    return f

# Parameters
iter = np.logspace(1, num_plots, num_plots, base=10)  # Logarithmically spaced
res_im = 500
xx = np.linspace(-3, 3, res_im)

# Create layout for subplots
fig, axes = plt.subplots(int(num_plots/2), 2, sharex=True, sharey=True)  # Share axes
axes = axes.flatten()  # Flatten the array for easier iteration

# Iterate through subplots
for i, ax in enumerate(axes):
    iter_value = int(iter[i])
    ax.plot(xx, ff(xx, iter=iter_value), label=f'N={iter_value}')
    ax.grid(True)
    ax.legend(loc='upper right')

# Add shared labels for x and y
fig.text(0.5, 0.02, 'x', ha='center', fontsize=fontsize)  # Slightly lower x-axis label
fig.text(0.02, 0.5, 'f(x)', va='center', rotation='vertical', fontsize=fontsize)  # Slightly left y-axis label

# Optimize layout
# plt.tight_layout(rect=[0.08, 0.05, 0.98, 0.95])  # Adjust spacing to avoid overlap
plt.savefig(filepath + "foutriawave.png")
