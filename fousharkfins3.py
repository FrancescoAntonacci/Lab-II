import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 18
num_plots = 2
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
# Logarithmically spaced
res_im = 100000
xx = np.linspace(-1, 1, res_im)
ft=(1e-3,1e-2,1e-1,1e0,1e1,1e2)


fig, axes = plt.subplots(int(len(ft)/2), 2, sharex=True, figsize=(12, len(ft)))
axes=axes.flatten()
# Ciclo per creare i plot
for i, ax in enumerate(axes):
    ft_iteration=ft[i]
    ax.plot(xx, sharkfin(xx,ft=ft_iteration ))
    ax.set_title(f'$ft={ft_iteration}$[arb.un.]')
    ax.grid(True)

# Add shared labels for x and y axes
fig.text(0.5, 0.005, 't  [arb.un.]', ha='center', fontsize=fontsize)  # Shared x-axis label
fig.text(0.00, 0.5, 'x(t)[arb.un.]', va='center', rotation='vertical', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "fousharkfinsfts1.png")  # Save the plot as an image
plt.show()  # Display the plot