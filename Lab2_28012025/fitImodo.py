import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
path= r'/home/studentelab2/doppi_fra/Lab2_28012025/'
t1, sigma_t1, v1, sigma_v1 = np.loadtxt(path+"Diodo1.txt", unpack=True)
t2, sigma_t2, v2, sigma_v2 = np.loadtxt(path+"Diodo2.txt", unpack=True)
# bellurie

plt.figure(figsize=(8,5))

plt.rc('font',size=16)
plt.xlabel(r'$\Delta$V  [mV]',fontsize=18)
plt.ylabel(r'I  [mA]',fontsize=18)
plt.minorticks_on()

def model(x,I0,a):
    return I0 * (np.exp(x/a) - 1)


##
"""
_v_i is the converted potential in current


"""
init=(25e-9,33)

rd = 363
sigma_rd = 3
eta = 0.733
sigma_eta = 0.007

deltav = v1 - v2
sigma_deltav = np.sqrt(sigma_v1**2 + sigma_v2**2)

v2=eta*v2
sigma_v2 = np.sqrt((sigma_eta*v2)**2+(eta*sigma_v2)**2)


i =eta * (deltav)/rd
sigma_i =np.sqrt((sigma_eta*deltav/rd)**2+(sigma_deltav*eta/rd)**2+(sigma_rd*eta*deltav/rd**2)**2)
s_i = np.copy(sigma_i)

##

popt, pcov = curve_fit(model, v2, i, p0=init, sigma=sigma_i, absolute_sigma=False)

for n in range(100):
    for j in range(len(s_i)):
        s_i[j] = sigma_i[j] + popt[0] * np.exp(deltav[j]/popt[1]) * sigma_deltav[j]
    popt, pcov = curve_fit(model, v2, i, p0=init, sigma=sigma_i, absolute_sigma=False)
corr = np.copy(pcov) # create a *not* shadow copy of covm
for m in range(len(pcov)):
    for n in range(len(pcov)):
        corr[m, n] = pcov[m,n]/(np.sqrt(pcov[n, n] * pcov[m, m]))


print("Il fittino:",popt)
print("Il sigma fittino:",np.sqrt(pcov.diagonal()))

print("La correlazione è:\n", corr)


##

res= i-model(v2,*popt)


##
xx = np.linspace(min(v2), max(v2))

plt.plot(xx, model(xx, *popt))
plt.errorbar(v2,i,sigma_i,sigma_v2, fmt='.')
plt.savefig("Grafico_diodo.pdf")
plt.show()




