import numpy as np 
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def hpf(f,fth): #gain of high pass filter
    return 1/np.sqrt(1+(fth/f)**2)



filepath=r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Lab2_03122024/'

f,s_f,vac,vdc=np.loadtxt(filepath+"data5.txt",unpack=True)
g=vac/vdc
s_g=g*1e-2

p0=(2.2)

popt,pcov=curve_fit(hpf,f,g,p0=p0,sigma=s_g,absolute_sigma=False)


corr = np.copy(pcov)
for i in range(len(pcov)):
    for j in range(len(pcov)):
        corr[i, j] = pcov[i,j]/(np.sqrt(pcov[i, i] * pcov[j, j]))
s_popt=np.sqrt(pcov.diagonal())

print(popt,s_popt, corr)

xx=np.linspace(min(f),max(f),2000)   


##Plottino(
plt.figure()
plt.errorbar(f,g,s_g,s_f,'o',label="Dati raccolti")
plt.plot(xx,hpf(xx,popt))
plt.legend()
plt.xlabel('$f$[Hz]')
plt.ylabel('$G=Vac/Vdc$')
plt.savefig(filepath+"plot_cosc.png")
plt.show()

print(f"Dunque la supposto che la resistenza interna dell'oscilloscopio sia 1 Mohm, allora C={1/(2*1e6*np.pi*popt)}")

