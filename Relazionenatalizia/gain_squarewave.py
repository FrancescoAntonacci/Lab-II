import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# Filepath for saving the output image
filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/data/031224/'

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
def ff(x,a=1, omega=2 * np.pi*1e1,ft=1e1, iter=3000):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        phi=dphi_lpf(k*omega,ft)
        G=G_lpf(k*omega,ft)
        f += a*G*(2 / (k * np.pi)) * np.sin(k * x * omega+phi)
    return f

def vpp(f=1e3,a=1,ft=1e1, iter=1000):
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

##################
p0=[1,1e3]

f,s_f,V_i,s_V_i,V_out,s_V_out,_=np.loadtxt(filepath+"data2.txt",unpack=True)
G=V_out/V_i
s_G=G*np.sqrt((s_V_out/V_out)**2+(s_V_i/V_i)**2)

popt,pcov=curve_fit(vpp,f,G,p0=p0,sigma=s_G,absolute_sigma=True)
_, ft = popt

xx=np.logspace(min(np.log10(f)),max(np.log10(f)),3000)

plt.figure()
plt.plot(xx,vpp(xx,*popt),label='Best-fit onda quadra')
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
plt.savefig(filepath+'gain_squarewave.png')
plt.show()

print("popt=",popt)
print("s_popt=",np.sqrt(np.diag(pcov)))
k2=sum((G-vpp(f,*popt))**2/s_G**2)/(len(G)-2)
print("K2",k2)