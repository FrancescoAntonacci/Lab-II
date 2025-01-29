import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


path= r'/home/studentelab2/doppi_fra/Lab2_28012025/'
v1,v2 = np.loadtxt(path+"Diodo3.txt", unpack=True)
s_v1=np.full_like(v1,8)
s_v2=np.full_like(v2,8)

# bellurie
plt.rc('font',size=16)
plt.xlabel(r'$\Delta$V  [mV]',fontsize=18)
plt.ylabel(r'I  [mA]',fontsize=18)
plt.minorticks_on()


##

def model(x,I0,a):
    return I0 * (np.exp(x/a) - 1)

##

init=(4.07e-4,15)

rd = 363
s_rd = 3
eta = 0.733
s_eta = 0.007

deltav = v1 - v2
s_deltav = np.sqrt(s_v1**2 + s_v2**2)

v2=eta*v2
s_v2 = np.sqrt((s_eta*v2)**2+(eta*s_v2)**2)


i =eta * (deltav)/rd
s_i =np.sqrt((s_eta*deltav/rd)**2+(s_deltav*eta/rd)**2+(s_rd*eta*deltav/rd**2)**2)
##
popt, pcov = curve_fit(model, v2, i, p0=init, sigma=s_i, absolute_sigma=False)

corr = np.copy(pcov) # create a *not* shadow copy of covm
for m in range(len(pcov)):
    for n in range(len(pcov)):
        corr[m, n] = pcov[m,n]/(np.sqrt(pcov[n, n] * pcov[m, m]))


print("Parametri:",popt)
print("Varianza:",np.sqrt(pcov.diagonal()))

print("La correlazione è:\n", corr)


##
xx=np.linspace(min(v2),max(v2),1000)
plt.figure(1)
plt.errorbar(v2,i,s_i,s_v2,fmt='.')
plt.plot(xx,model(xx,*init))
plt.show()






