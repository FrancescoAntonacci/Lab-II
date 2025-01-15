import numpy as np
from matplotlib import pyplot as plt

filepath = r'./'

### Aesthetic Settings
fontsize = 18
params = {
    'figure.figsize': (6 * 1.618, 6),  # Figure size
    'axes.labelsize': fontsize,        # Axis label size
    'axes.titlesize': fontsize,        # Title size
    'xtick.labelsize': fontsize,       # X-axis tick label size
    'ytick.labelsize': fontsize,       # Y-axis tick label size
    'legend.fontsize': fontsize,       # Legend font size
}
plt.rcParams.update(params)

# Fourier sine series for a triangular wave (leave the original implementation intact)
def ff(x, iter=1000, a=1, omega=2 * np.pi, phi=0):
    iter += 1
    f = 0
    for k in range(1, iter, 2):  # Odd harmonics only
        f += ((2 / (k * np.pi))**2) * np.cos(k * x * omega + phi)
    return a * f

# Analytical triangular wave
def triangwave(x, a=1, omega=2 * np.pi, phi=0):
    return a * 0.5 * (1 - (2 / np.pi) * np.arccos(np.cos(x * omega + phi)))

# Residuals: Difference between analytical triangular wave and Fourier series
def residuals(x, a=1, iter=1000, omega=2 * np.pi, phi=0):
    # Ensure all parameters are correctly passed and consistent
    return triangwave(x, a, omega, phi) - ff(x, iter=iter, a=a, omega=omega, phi=phi)

# Parameters for the triangular wave and Fourier series
iterations = (1, 5, 50, 10000)  # Number of terms in Fourier series
res_im = 100  # Resolution for the x-axis (number of points)
xx = np.linspace(-1, 1, res_im)  # Generate x values between -1 and 1

# Create a grid layout for subplots
fig, axes = plt.subplots(len(iterations), 2, sharex=True, figsize=(12, len(iterations) * 2))
axes = axes if len(iterations) > 1 else [axes]  # Ensure compatibility when there's only one iteration

# Iterate through each subplot
for i, (ax_left, ax_right) in enumerate(axes):
    iter_value = iterations[i]  # Get the current iteration value
    
    # Plot the reconstructed triangular wave (Fourier approximation)
    ax_left.plot(xx, ff(xx, iter=iter_value, a=1))
    ax_left.set_title(f'Ricostruzione onda Triangolare(N={iter_value})')
    ax_left.grid(True)
    
    # Plot the residuals (difference between Fourier and analytical wave)
    ax_right.plot(xx, residuals(xx, iter=iter_value, a=1))
    ax_right.set_title(f'Residui (N={iter_value})')
    ax_right.grid(True)

# Add shared labels for x and y axes
fig.supxlabel('t  [arb.un.]', fontsize=fontsize)  # Shared x-axis label
fig.supylabel('x(t) [arb.un.]', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "foutriawave1e2.png")  # Save the plot as an image
plt.show()  # Display the plot
