import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

plt.rc('font',size=16)
plt.minorticks_on()

file_data = "/home/studentelab2/doppi_fra/Lab2_18022025/freq.txt"
f, s_f, vin, s_vin, vout, s_vout = np.loadtxt(file_data, unpack=True)
f = f * 1e3
s_f = s_f * 1e3
vin=vin*1e-3
s_vin=s_vin*1e-3
vout=vout*1e-3
s_vout=s_vout*1e-3
rc = 1.0e3
cf = 1e-6
ib = 9.1e-6
s_ib = 0.2e-6
ic = 1.80e-3
s_ic = 0.05e-3
rb=561
s_rb=3
guad = vout/vin
s_guad = ((s_vin/vin) + (s_vout/vout)) * guad



rb1=rb+30e-3/ib # rb+Rb
beta=ic/ib

init=(rb1)

def model(f,Rb1):
    omega=2*np.pi*f
    T=-(rc/(Rb1))*beta*((1-1j*omega*Rb1*(cf/beta))/(1+1j*omega*rc*cf))
    G=np.abs(T)
    return G



##
popt,pcov=curve_fit(model,f,guad,p0=init,sigma=s_guad, absolute_sigma=False)

print(popt,np.sqrt(pcov.diagonal()))

corr=np.copy(pcov)

for j in range(len(popt)):
    for i in range(len(popt)):
        corr[i,j]=corr[i,j]/np.sqrt(pcov[i,i]*pcov[j,j])
print(corr)
##
xx=np.linspace(min(f),max(f),1000)
plt.figure(1)
plt.errorbar(f, guad, s_guad, s_f, fmt='.',label="Dati raccolti")
plt.plot(xx,model(xx,*popt),label="modello")
plt.xscale("log")
plt.xlabel(r"$f$[Hz]")
plt.ylabel(r"$G$")
plt.legend()
plt.show()