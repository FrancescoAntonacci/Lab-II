import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'


s_v=10 #Basto su esperienze precedenti

### Aesthetic Settings
fontsize = 20
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
    error[horizontal_indices] = s_v # Errore di 1 ai punti orizzontali

    # Punti verticali (dove la derivata è alta)
    vertical_indices = np.abs(dy) > 0.1
    error[vertical_indices] = 1e3  # Errore di 1e5 ai punti verticali

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

def residuals(yy,xx,pars):
    return yy-ff(xx, *pars)
##################
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

s_v1=np.full_like(v1, s_v)
s_v1 = assign_error(t1, v1)

p0=(2*np.pi/2.1e5,0.5,3000,2000)
popt11,pcov11=curve_fit(ff,t1,v1,p0=p0,sigma=s_v1,absolute_sigma=True)
res11=residuals(v1,t1,popt11)/s_v1
k11=sum((res11/s_v1)**2)/(len(v1)-len(popt11))


s_v1=np.full_like(v1, s_v)

popt12,pcov12=curve_fit(ff,t1,v1,p0=p0,sigma=s_v1,absolute_sigma=False)
res12=residuals(v1,t1,popt12)/s_v1
k12=sum((res12/s_v1)**2)/(len(v1)-len(popt12))

fig, axs = plt.subplots(2, 2, figsize=(16,8), gridspec_kw={'height_ratios': [2, 1]})

# Plotting the fits
axs[0, 0].set_title("Best-fit trascurando le misure sui transienti")
axs[0, 0].errorbar(t1, v1, s_v1, fmt='.', label="Dati")
axs[0, 0].plot(xx, ff(xx, *popt11), label="Fit")
axs[0, 0].legend(loc='lower right')
axs[0, 0].set_ylabel("V [arb.un.]")
axs[0, 0].set_xlabel("t [$\mu$s]")

axs[0, 1].set_title("Best-fit considerando le misure sui transienti")
axs[0, 1].errorbar(t1, v1, s_v1, fmt='.', label="Dati")
axs[0, 1].plot(xx, ff(xx, *popt12), label="Fit")
axs[0, 1].legend(loc='lower right')
axs[0, 1].set_ylabel("V [arb.un.]")
axs[0, 1].set_xlabel("t [$\mu$s]")

# Plotting the residuals
axs[1, 0].set_title("Residui trascurando le misure sui transienti")
axs[1, 0].plot(t1, res11, '.')
axs[1, 0].set_ylabel("Residui normalizzati")
axs[1, 0].set_xlabel("t [$\mu$s]")

axs[1, 1].set_title("Residui considerando le misure sui transienti")
axs[1 ,1].plot(t1, res12, '.')
axs[1, 1].set_ylabel("Residui normalizzati")
axs[1, 1].set_xlabel("t [$\mu$s]")

plt.tight_layout()
plt.savefig(filepath + "bestfit_squarewave.png")
plt.show()


print("\n\Trascurando le misure sui transienti")
print("parametri:", popt11)
print("incertezze:", np.sqrt(pcov11.diagonal()))

corr11 = np.copy(pcov11)
for i in range(len(pcov11)):
    for j in range(len(pcov11)):
        corr11[i, j] = pcov11[i,j]/(np.sqrt(pcov11[i, i] * pcov11[j, j]))
print("matrice di correlazione:\n",corr11)
print("x2=",k11)



print("\n\nConsiderando le misure sui transienti")
print("parametri:", popt12)
print("incertezze:", np.sqrt(pcov12.diagonal()))

corr12 = np.copy(pcov12)
for i in range(len(pcov12)):
    for j in range(len(pcov12)):
        corr12[i, j] = pcov12[i,j]/(np.sqrt(pcov12[i, i] * pcov12[j, j]))
print("matrice di correlazione:\n",corr12)
print("x2=",k12)


#print(popt12)
#print(pcov12)
