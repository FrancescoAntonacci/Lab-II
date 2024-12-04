import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

Directory='/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Lab2_03122024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data2.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
f,sigma_f,V_i,sigma_Vi, V_out, sigma_Vout, delta_t = np.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

phi=delta_t*f*(2*np.pi)
sigma_phi=phi*(sigma_f/f)/np.sqrt(3)


xx=np.linspace(min(f),max(f),1000)

def ff(x,a,ft):
    return a*np.arctan(x/ft)

init=(1,430)

popt,pcov= curve_fit(ff, f,phi, p0=init,sigma=sigma_phi,absolute_sigma=False)

print("Parametri ottimizzati:",popt)
print("incertezze",np.sqrt(pcov.diagonal()))

corr=np.copy(pcov)
for i in range(len(pcov)):
    for j in range(len(pcov)):
        corr[i, j] = pcov[i,j]/(np.sqrt(pcov[i, i] * pcov[j, j]))

print("Matrice di correlazione",corr)

plt.rc('font',size=16)
plt.xlabel('f [Hz]',fontsize=18)
plt.ylabel('$\Delta\phi$[rad]',fontsize=18)
plt.minorticks_on()

##
ndof=len(f)-len(popt)
x2rid= sum(((phi-ff(f,*popt))/sigma_phi)**2)/ndof
print("Il x2 ridotto è:",x2rid)


##

plt.figure(1)
plt.errorbar(f,phi,sigma_phi,sigma_f,fmt="o")
plt.errorbar(xx,ff(xx,*popt))
plt.show()

