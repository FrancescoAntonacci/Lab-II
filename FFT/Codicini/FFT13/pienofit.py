import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit


t,st,v,sv=np.loadtxt('dataFFT13/pieno1.txt',unpack=True)
t = t * 1e-6
st = st * 1e-6

init =[1200, 0.02, 3.8e3, np.pi/2, 1900]

def model(t, A, tau, omega, phi, c):
    return A * np.exp(-t/tau) * np.cos(omega * t + phi) + c
tt=np.linspace(min(t),max(t),10000)

popt,pcov=curve_fit(model,t,v,p0=init, sigma=sv,absolute_sigma=True)
print(popt,np.sqrt(np.diag(pcov)))

plt.figure()
plt.errorbar(t,v,sv,st,fmt='o')
plt.plot(tt,model(tt,*popt))
plt.show()