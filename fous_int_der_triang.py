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

# Fourier sine series for a square wave
def ff(x,a, omega, phi,c,ft, iter=1000):
    iter += 1
    f = 0
    x=phi+x
    for k in range(1, iter, 2):
        f += G_lpf(k*omega,ft)*((2 / (k * np.pi))**2) * np.cos(k * x * omega + dphi_lpf(k*omega,ft) )
    f=f-np.mean(f)
    return a*f+c

def fd(x,a, omega, phi,c,ft, iter=1000):
    iter += 1
    f = 0
    x=phi+x
    for k in range(1, iter, 2):
        f += G_hpf(k*omega,ft)*((2 / (k * np.pi))**2) * np.cos(k * x * omega + dphi_hpf(k*omega,ft) )
    f=f-np.mean(f)
    return a*f+c

def ft(x,a=1, omega=2 * np.pi, phi=0, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += ((2 / (k * np.pi))**2) * np.cos(k * x * omega + phi)
    return a*f


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



# Analytical square wave
def triangwave(x, a, omega=2 * np.pi, phi=0):
    return a * (1-(2/np.pi)*np.arccos(np.cos(x * omega + phi)))


# Parameters
iter = np.logspace(1, num_plots, num_plots, base=10)  # Logarithmically spaced
res_im = 10000
xx = np.linspace(-1, 1, res_im)

plt.figure()
plt.plot(xx,1000*ff(xx,1,2*np.pi,0,0,1e-3),label="Segnale integrato x1000")
plt.plot(xx,1000*fd(xx,1,2*np.pi,0,0,1e3),label="Segnale derivato x1000")
plt.plot(xx,ft(xx,1,2*np.pi,0,1000),label="Segnale")
plt.grid()
plt.legend(loc='lower right', ncol=1)
plt.savefig(filepath+"integ_der_trinag.png")
plt.show()
