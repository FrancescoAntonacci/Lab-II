import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 18
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

def ff(x, iter=1000, a=1, omega=2 * np.pi, phi=0, delta=0.3):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += (2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega + phi)
    return a * (f+delta) 


# Analytical square wave
# Pulse train with zero offset
def pulsetrain(x, a=1, omega=2 * np.pi, phi=0, delta=0.3):
    pulse = np.abs(np.mod(x * omega + phi+1, 2 * np.pi)) < (2 * np.pi * delta)
    return a * (pulse)


# Residuals: Difference between square wave and Fourier series
def residuals(x, a=1, iter=1000, omega=2 * np.pi, phi=0,delta=0.3):
    return pulsetrain(x, a=a, omega=omega, phi=phi, delta=delta) - ff(x, iter=iter, a=a, omega=omega, phi=phi, delta=delta)


iterations=(1,5,50,10000)
# Parameters for the square wave and Fourier series
res_im = 100000# Resolution for the x-axis (number of points)
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
    ax_left.set_title(f'Ricostruzione treno di impulsi (N={iter_value})')
    ax_left.grid(True)
    # Plot the residuals (difference between Fourier and analytical wave)
    ax_right.plot(xx, residuals(xx, iter=iter_value))
    ax_right.set_title(f'Residui (N={iter_value})')
    ax_right.grid(True)
# Add shared labels for x and y axes
fig.text(0.5, 0.005, 't  [arb.un.]', ha='center', fontsize=fontsize)  # Shared x-axis label
fig.text(0.00, 0.5, 'x(t)[arb.un.]', va='center', rotation='vertical', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "foupulsetrainwave1e5.png")  # Save the plot as an image
plt.show()  # Display the plot
