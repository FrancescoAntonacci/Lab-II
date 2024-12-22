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

# Functions
def ff(x,a=1, omega=2 * np.pi*1e1,ft=1e1, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        phi=dphi_lpf(k*omega,ft)
        G=G_lpf(k*omega,ft)
        f += a*G*((2 / (k * np.pi))**2) * np.cos(k * x * omega+phi)
    return f

def vpp(f,a=1,ft=1e1, iter=1000):
    vv=[]
    for freq in f:
        omega=2*np.pi*freq
        xx=np.linspace(-1,1,10000)
        yy=ff(xx,a,omega,ft,iter)
        vv.append(np.max(yy)-np.min(yy))
    return vv



##################
#Filters
def G_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(f/ft)**2)
def dphi_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(-f/ft)
#####Obteined with previous fits
v=np.array([2575,2333,781,83])
s_v=np.full_like(v,1)
a=np.mean([2665,2671,2674,2652])
s_a=np.std([2665,2671,2674,2652])
omega=np.array([29.817,300.784,2969.2,29667])
s_omega=np.array([0.002,0.03,0.08,16])
f=omega/(2*np.pi)
s_f=s_omega/(2*np.pi)
G=v/a
s_G=G*np.sqrt((s_v/v)**2+(s_a/a)**2)

p0=[2000,1e3]

popt,pcov=curve_fit(vpp,f,G,p0=p0,sigma=s_G,absolute_sigma=True)
_, ft = popt

xx=np.logspace(min(np.log10(f)),max(np.log10(f)),1000)

plt.figure()
plt.plot(xx,vpp(xx,*popt),label='Best-fit onda triangolare')
plt.plot(xx,G_lpf(2*np.pi*xx,ft=ft),label='Onda sinusoidale')
plt.errorbar(f,G,yerr=s_G,xerr=s_f,fmt='.',label='Dati sperimentali')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Frequenza [Hz]')
plt.ylabel('G')
plt.grid()
plt.legend()
plt.minorticks_on()
plt.tight_layout()
plt.savefig(filepath+'gain_trianwave.png')
plt.show()

print("popt=",popt)
print("s_popt=",np.sqrt(np.diag(pcov)))
k2=sum((G-vpp(f,*popt))**2/s_G**2)/(len(G)-2)
print("K2",k2)