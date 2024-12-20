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





# Parameters
iter = np.logspace(1, num_plots, num_plots, base=10)  # Logarithmically spaced
res_im = 10000
xx = np.linspace(-1, 1, res_im)

plt.figure()
plt.plot(xx,ff(xx),label="Segnale")
plt.plot(xx,1e3*fi(xx),label="Segnale integrato x1000")
plt.plot(xx,fd(xx),label="Segnale derivato")
#plt.plot(xx,1e3*fpb(xx),label="Segnale fuori dal passabanda")

plt.grid()
plt.ylim(-1,1)
plt.legend(loc='lower right', ncol=1)
plt.savefig(filepath+"integ_der_train.png")
plt.show()