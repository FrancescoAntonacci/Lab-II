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

# Fourier sine series for a train pulse wave
def ff(x, a=1, omega=2 * np.pi, delta=0.3, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += (2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega)
    return a * f 

def fi(x, a=1, omega=2 * np.pi, delta=0.3,ft=1e-3, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += G_lpf(k*omega,ft)*(2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega+dphi_lpf(k*omega,ft))
    return a * f 

def fd(x, a=1, omega=2 * np.pi, delta=0.3,ft=1e1, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += G_hpf(k*omega,ft)*(2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega+dphi_hpf(k*omega,ft))
    return a * f 

def fpb(x, a=1, omega=2 * np.pi, delta=0.3,ft1=1e1,ft2=1e-3, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += G_lpf(k*omega,ft2)*G_hpf(k*omega,ft1)*(2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega+dphi_hpf(k*omega,ft1)+dphi_lpf(k*omega,ft2))
    return a * f 



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





res_im = 100000
xx = np.linspace(-1, 1, res_im)
ft=([1e-3,1e-3],[1e-2,1e-2],[1e-1,1e-1],[1e-0,1e-0],[1e1,1e1],[1e2,1e2])


fig, axes = plt.subplots(int(len(ft)/2), 2, sharex=True, figsize=(12, len(ft)))
axes=axes.flatten()
# Ciclo per creare i plot
for i, ax in enumerate(axes):
    ft_iteration=ft[i]
    ax.plot(xx, fpb(xx,ft1=ft_iteration[0],ft2=ft_iteration[1] ))
    ax.set_title(f'$ft1,ft2={ft_iteration}$[arb.un.]')
    ax.grid(True)

# Add shared labels for x and y axes
fig.text(0.5, 0.005, 't  [arb.un.]', ha='center', fontsize=fontsize)  # Shared x-axis label
fig.text(0.00, 0.5, 'x(t)[arb.un.]', va='center', rotation='vertical', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "band_train.png")  # Save the plot as an image
plt.show()  # Display the plot
