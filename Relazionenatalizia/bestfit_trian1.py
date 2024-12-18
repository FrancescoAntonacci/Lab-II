import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 14
num_plots = 4
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


##################
def G_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(f/ft)**2)
def dphi_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(-f/ft)


##################
def ff(x,a, omega, phi,c,ft, iter=1000):
    iter += 1
    f = 0
    x=phi+x
    for k in range(1, iter, 2):
        f += G_lpf(k*omega,ft)*((2 / (k * np.pi))**2) * np.cos(k * x * omega + dphi_lpf(k*omega,ft) )
    f=f-np.mean(f)
    return a*f+c


def sin(x,a,omega,phi,c):
    return a*np.sin(omega*x+phi)+c


##################

t1,v1=np.loadtxt(filepath+"data/trian1.txt",unpack=True)
t2,v2=np.loadtxt(filepath+"data/trian2.txt",unpack=True)
t3,v3=np.loadtxt(filepath+"data/trian3.txt",unpack=True)
t4,v4=np.loadtxt(filepath+"data/trian4.txt",unpack=True)#Bad dataset-but do not discard!
t5,v5=np.loadtxt(filepath+"data/trian4bis.txt",unpack=True)



xx=np.linspace(max(t1),min(t1),10000)
p0=(2.6e3,2*np.pi/2.1e5,0.1e6,2000,1e-3)

popt1,pcov1=curve_fit(ff,t1,v1,p0=p0,absolute_sigma=False)
plt.figure()
plt.errorbar(t1,v1,fmt='.',label="Dati sperimentali")
plt.plot(xx,ff(xx,*popt1))

xx=np.linspace(max(t2),min(t2),10000)
p0=(2.6e3,2*np.pi/2.1e4, 2e5,2000,1e-3)
popt2,pcov2=curve_fit(ff,t2,v2,p0=p0,absolute_sigma=False)

plt.figure()
plt.errorbar(t2,v2,fmt='.',label="Dati sperimentali")
plt.plot(xx,ff(xx,*popt2))

xx=np.linspace(max(t3),min(t3),10000)
p0=(1e3,2*np.pi/2.1e3, -1e5,2000,1e-3)
popt3,pcov3=curve_fit(ff,t3,v3,p0=p0,absolute_sigma=False)


plt.figure()
plt.errorbar(t3,v3,fmt='.',label="Dati sperimentali")
plt.plot(xx,ff(xx,*popt3))

#Bad dataset-but do not discard!
# xx=np.linspace(max(t4),min(t4),10000)
# p0=(2.6e3,2*np.pi/2.1e2, 2e5,2000,1e-3)
# popt4,pcov4=curve_fit(ff,t4,v4,p0=p0,absolute_sigma=False)

# plt.figure()
# plt.errorbar(t4,v4,fmt='.',label="Dati sperimentali")
# plt.plot(xx,ff(xx,*popt4))


xx=np.linspace(max(t5),min(t5),10000)
p0=(2.6e3,2*np.pi/2.1e2, 2e5,2000,1e-3)
popt5,pcov5=curve_fit(ff,t5,v5,p0=p0,absolute_sigma=False)

plt.figure()
plt.errorbar(t5,v5,fmt='.',label="Dati sperimentali")
plt.plot(xx,ff(xx,*popt5))


plt.show()