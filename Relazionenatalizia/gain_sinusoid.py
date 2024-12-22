import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Filepath for saving the output image
filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic settings for the plots
fontsize = 18
params = {
    'figure.figsize': (4 * 1.618, 4),  # Figure size in inches (width x height)
    'axes.labelsize': fontsize,        # Font size for axis labels
    'axes.titlesize': fontsize,        # Font size for titles
    'xtick.labelsize': fontsize,       # Font size for x-axis ticks
    'ytick.labelsize': fontsize,       # Font size for y-axis ticks
    'legend.fontsize': fontsize,       # Font size for legends
}
plt.rcParams.update(params)  # Apply these settings globally to matplotlib


##################
#Filters
def G_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(f/ft)**2)
def dphi_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(-f/ft)
########## Data from the previous fits
v=np.array([2402,2402,918,101])/2
s_v=np.full_like(v,1)
a=np.mean([1240.2,1240.2,1240.2,1240.2])
s_a=np.std([0.8,0.9,0.8,0.8])
omega=np.array([29.822,300.77,2969.9,29652])
s_omega=np.array([0.003,0.03,0.7,3])
f=omega/(2*np.pi)
s_f=s_omega/(2*np.pi)
G=v/a
s_G=G*np.sqrt((s_v/v)**2+(s_a/a)**2)

p0=[1e3]

popt,pcov=curve_fit(G_lpf,omega,G,p0=p0,sigma=s_G,absolute_sigma=True)

xx=np.logspace(min(np.log10(f))-1,max(np.log10(f)),1000)

plt.figure()
plt.plot(xx,G_lpf(xx,*popt),label='Onda sinusoidale')
plt.errorbar(f,G,yerr=s_G,xerr=s_f,fmt='.',label='Dati')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequenza [Hz]')
plt.ylabel('G')
plt.grid()
plt.legend()
plt.minorticks_on()
plt.tight_layout()
plt.savefig(filepath+'gain_sinusoid.png')
plt.show()