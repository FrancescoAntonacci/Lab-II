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

    return f - np.mean(f)


def ff(x, iter=1000, omega=2 * np.pi, phi=0):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.sin(k * x * omega + phi)
    return f

##################


# Parameters
iter = np.logspace(1, num_plots, num_plots, base=10)  # Logarithmically spaced
res_im = 100
xx = np.linspace(-1, 1, res_im)
ft=2e0

fig, axes = plt.subplots(int(num_plots / 2), 2, sharex=True)  # Share axes
axes = axes.flatten()  # Flatten the array for easier iteration

# Iterate through subplots
for i, ax in enumerate(axes):
    if i % 2 == 0:
        iter_value = int(iter[i])
        iteration = int(1 + np.floor(iter_value / 2))  # Kind of wave we are working on
        ax.plot(xx, sharkfin(xx, iter=iteration,ft=ft), label=f'N={iter_value}')
        ax.grid(True)
        ax.legend(loc='upper right')
    if i % 2 == 1:
        iter_value = int(iter[i])
        iteration = int(iter_value / 10)  # Kind of wave we are working on
        ax.plot(xx, ff(xx, iter=iteration), label=f'N={iteration}')
        ax.grid(True)
        ax.legend(loc='upper right')

plt.savefig(filepath+"fousharkfins.png")
plt.show()