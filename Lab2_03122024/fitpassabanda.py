import numpy as np 
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def lpf(f,ftl): #Gain for low pass filter
    return 1/np.sqrt(1+(f/ftl)**2)

def hpf(f,fth): #Gain for high pass filter
    return 1/np.sqrt(1+(fth/f)**2)

def v_bpf(f,v,ftl,fth): #Potential given pass out a pass band filter
    return v*lpf(f,ftl)*hpf(f,fth)

filepath=r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Lab2_03122024/'

f,s_f,vpp,s_vpp=np.loadtxt(filepath+"data4.txt",unpack=True)
v=vpp/2
s_v=s_vpp/2

p0=(0.4,5100,1100)
popt,pcov=curve_fit(v_bpf,f,v,p0=p0,sigma=s_v,absolute_sigma=True)

corr = np.copy(pcov)
for i in range(len(pcov)):
    for j in range(len(pcov)):
        corr[i, j] = pcov[i,j]/(np.sqrt(pcov[i, i] * pcov[j, j]))

s_popt=np.sqrt(pcov.diagonal())

xx=np.logspace(min(np.log10(f)),max(np.log10(f)),2000)   

print(popt,s_popt,corr)

##Plottino(
plt.figure()
plt.errorbar(f,v,s_v,s_f,'o',label="Dati raccolti")
plt.plot(xx,v_bpf(xx,*popt),label="Bestfit")
plt.legend()
plt.xscale('log')
plt.xlabel('$f$[Hz]')
plt.ylabel('$V$[V]')
plt.show()
plt.savefig(filepath+"plot_passabanda.png")



