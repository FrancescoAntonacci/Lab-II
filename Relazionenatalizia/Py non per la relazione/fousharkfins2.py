import numpy as np
from matplotlib import pyplot as plt

filepath = r'./'

### Aesthetic Settings
fontsize = 14
num_plots = 4
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
def sharkfin(x, iter=1000, omega=2 * np.pi,ft=1e1):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        phi=dphi_lpf(k*omega,ft)
        G=G_lpf(k*omega,ft)
        f += G*(2 / (k * np.pi)) * np.sin(k * x * omega+phi)
    return f


def ff(x, iter=1000, omega=2 * np.pi, phi=0):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.sin(k * x * omega + phi)
    return f

##################


# Parameters
iterations = (1,5,25,100)  # Logarithmically spaced
res_im = 100000
xx = np.linspace(-1, 1, res_im)
ft=2e0

fig, axes = plt.subplots(len(iterations), 2, sharex=True, figsize=(12, len(iterations) * 2))
axes = axes if len(iterations) > 1 else [axes]  # Ensure compatibility when there's only one iteration

# Iterate through each subplot
for i, (ax_left, ax_right) in enumerate(axes):
    iter_value = int(iterations[i])  # Get the current iteration value
    
    # Plot the reconstructed square wave (Fourier approximation)
    ax_left.plot(xx, ff(xx, iter=iter_value), label=f'N={iter_value}')
    ax_left.set_title(f'Segnale:onda quadra (N={iter_value})')
    ax_left.grid(True)
    # Plot the residuals (difference between Fourier and analytical wave)
    ax_right.plot(xx, sharkfin(xx, iter=iter_value))
    ax_right.set_title(f'Segnale attraverso il filtro (N={iter_value})')
    ax_right.grid(True)
# Add shared labels for x and y axes
fig.supxlabel('t  [arb.un.]', fontsize=fontsize)  # Shared x-axis label
fig.supylabel('x(t)[arb.un.]', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "fousharkfins.png")  # Save the plot as an image
plt.show()  # Display the plot