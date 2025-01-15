import numpy as np
from matplotlib import pyplot as plt

# Filepath for saving the output image
filepath = r'./'

### Aesthetic settings for the plots
fontsize = 18
params = {
    'figure.figsize': (4 * 1.618, 4),  # Figure size in inches (width x height)
    'axes.labelsize': fontsize,        # Font size for axis labels
    'axes.titlesize': fontsize,        # Font size for titles
    'xtick.labelsize': fontsize,       # Font size for x-axis ticks
    'ytick.labelsize': fontsize,       # Font size for y-axis ticks
    'legend.fontsize': fontsize,       # Font size for legends
}
plt.rcParams.update(params)  # Apply these settings globally to matplotlib

# Fourier sine series for a square wave
def ff(x, iter=1000, omega=2 * np.pi, phi=0):
    """
    Compute the Fourier series approximation of a square wave.

    Args:
        x: Array of points to evaluate.
        iter: Number of iterations (number of terms in the series).
        omega: Angular frequency of the wave.
        phi: Phase shift.

    Returns:
        Approximated square wave using Fourier series.
    """
    iter += 1  # Add 1 to include all odd terms
    f = 0
    for k in range(1, iter, 2):  # Only odd terms in the series
        f += (2 / (k * np.pi)) * np.sin(k * x * omega + phi)
    return f

# Analytical representation of a square wave
def squarewave(x, a, omega=2 * np.pi, phi=0):
    """
    Generate an analytical square wave.

    Args:
        x: Array of points to evaluate.
        a: Amplitude of the wave.
        omega: Angular frequency of the wave.
        phi: Phase shift.

    Returns:
        Analytical square wave values.
    """
    return a * np.sign(np.sin(x * omega + phi))

# Residuals: Difference between analytical and Fourier series square waves
def residuals(x, a, iter, omega=2 * np.pi, phi=0):
    """
    Compute the residuals (error) between the analytical square wave 
    and its Fourier series approximation.

    Args:
        x: Array of points to evaluate.
        a: Amplitude of the wave.
        iter: Number of iterations for the Fourier series.
        omega: Angular frequency of the wave.
        phi: Phase shift.

    Returns:
        Residuals as the difference between the analytical wave and Fourier approximation.
    """
    return squarewave(x, a, omega, phi) - ff(x, iter, omega, phi)

iterations=(1,5,50,10000)
# Parameters for the square wave and Fourier series
res_im = 100000 # Resolution for the x-axis (number of points)
xx = np.linspace(-1, 1, res_im)  # Generate x values between -1 and 1
num_plots = len(iterations) * 2  # Each iteration generates two plots (wave and residuals)

# Create a grid layout for subplots
fig, axes = plt.subplots(len(iterations), 2, sharex=True, figsize=(12, len(iterations) * 2))
axes = axes if len(iterations) > 1 else [axes]  # Ensure compatibility when there's only one iteration

# Iterate through each subplot
for i, (ax_left, ax_right) in enumerate(axes):
    iter_value = iterations[i]  # Get the current iteration value
    
    # Plot the reconstructed square wave (Fourier approximation)
    ax_left.plot(xx, ff(xx, iter=iter_value), label=f'N={iter_value}')
    ax_left.set_title(f'Ricostruzione onda quadra (N={iter_value})')
    ax_left.grid(True)
    # Plot the residuals (difference between Fourier and analytical wave)
    ax_right.plot(xx, residuals(xx, a=0.5, iter=iter_value))
    ax_right.set_title(f'Residui (N={iter_value})')
    ax_right.grid(True)
# Add shared labels for x and y axes
fig.supxlabel('t  [arb.un.]', fontsize=fontsize)  # Shared x-axis label
fig.supylabel('x(t)[arb.un.]', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "fousquarewave1e5.png")  # Save the plot as an image
plt.show()  # Display the plot
