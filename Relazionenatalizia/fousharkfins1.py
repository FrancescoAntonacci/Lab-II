import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 18
num_plots = 8
params = {
    'figure.figsize': (6 * 1.618, 6),  # Figure size
    'axes.labelsize': fontsize,        # Axis label size
    'axes.titlesize': fontsize,        # Title size
    'xtick.labelsize': fontsize,       # X-axis tick label size
    'ytick.labelsize': fontsize,       # Y-axis tick label size
    'legend.fontsize': fontsize,       # Legend font size
}
plt.rcParams.update(params)



##################
def G_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(f/ft)**2)
def dphi_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(-f/ft)

def G_hpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(ft/f)**2)
def dphi_hpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(ft/f)

##################
import numpy as np

import numpy as np

def sharkfin(x, a=1, omega=2 * np.pi, ft=1e1):
    """
    Generates a periodic 'sharkfin' waveform without a phase shift.

    Parameters:
        x (float or ndarray): Input time or position variable.
        a (float): Amplitude scaling factor (default: 1).
        omega (float): Angular frequency in radians (default: 2 * pi).
        ft (float): Frequency parameter, related to the time constant (default: 10 Hz).

    Returns:
        float or ndarray: Output periodic 'sharkfin' waveform value(s).
    """
    period = 2 * np.pi / omega  # Calculate the period from omega
    x_mod = x % period  # Wrap x to create periodicity

    tau = 1 / (2 * np.pi * ft)  # Time constant derived from ft
    
    # Exponential terms
    exp_decay = np.exp(-x_mod / tau)
    exp_shifted_decay = np.exp(-(x_mod - 0.5 * period) / tau)
    
    # Positive and negative sine components
    pos_sine = np.maximum(np.sign(np.sin(omega * x_mod)), 0)
    neg_sine = np.minimum(np.sign(np.sin(omega * x_mod)), 0)
    
    # Compute the waveform
    term1 = (a * (1 - exp_decay) - a / 2) * pos_sine
    term2 = -(a * (exp_shifted_decay - 1) + a / 2) * neg_sine
    
    # Combine terms
    return term1 + term2




def ff(x, iter=1000, omega=2 * np.pi, phi=0,ft=1e1):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        phi=dphi_lpf(k*omega,ft)
        G=G_lpf(k*omega,ft)
        f += G*(2 / (k * np.pi)) * np.sin(k * x * omega+phi)
    return f

def residuals(x, a=1, iter=1000, omega=2 * np.pi, phi=0):
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
    return sharkfin(x) - ff(x,iter=iter)##################

iterations=(1,5,50,1000)
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
fig.text(0.5, 0.005, 't  [arb.un.]', ha='center', fontsize=fontsize)  # Shared x-axis label
fig.text(0.00, 0.5, 'x(t)[arb.un.]', va='center', rotation='vertical', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "fousharkfins1e2.png")  # Save the plot as an image
plt.show()  # Display the plot