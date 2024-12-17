import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

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
#################

def calculate_derivative(x, y):
    return np.gradient(y, x)

# Creare la funzione di errore
def assign_error(x, y):
    error = np.zeros_like(y)

    # Calcolare la derivata per identificare i cambiamenti rapidi (punto verticale)
    dy = calculate_derivative(x, y)

    # Punti orizzontali (dove la derivata è bassa)
    horizontal_indices = np.abs(dy) < 0.1
    error[horizontal_indices] = 1  # Errore di 1 ai punti orizzontali

    # Punti verticali (dove la derivata è alta)
    vertical_indices = np.abs(dy) > 0.1
    error[vertical_indices] = 1e4  # Errore di 1e5 ai punti verticali

    return error


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
def sharkfin(x, omega=2 * np.pi,ft=1e1,a=1,c=0, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        dphi=dphi_lpf(k*omega,ft)
        G=G_lpf(k*omega,ft)
        f += G*(2 / (k * np.pi)) * np.sin(k * x * omega+dphi)
    return a*(f- np.mean(f))+c


def ff(x, omega=2 * np.pi, phi=0,a=1,c=0, iter=1000):
    iter += 1
    f = 0
    x=x+phi

    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.sin(k * x * omega)
    return a*f+c

##################

t1,v1=np.loadtxt(filepath+"data/quadra1.txt",unpack=True)
xx=np.linspace(max(t1),min(t1),10000)

s_v1 = assign_error(t1, v1)

p0=(2*np.pi/2.1e5,0.5,3000,2000)
popt11,pcov11=curve_fit(ff,t1,v1,p0=p0,sigma=s_v1,absolute_sigma=False)
popt12,pcov12=curve_fit(ff,t1,v1,p0=p0,absolute_sigma=False)


plt.figure()
plt.errorbar(t1,v1,fmt='.',label="Dati sperimentali")
plt.plot(xx,ff(xx,*popt11),label="Fit trascurando le misure sui transienti")
plt.plot(xx,ff(xx,*popt12),label="Fit considerando le misure sui transienti")
plt.legend()
plt.savefig(filepath+"bestfit_squarewave.png")
plt.show()