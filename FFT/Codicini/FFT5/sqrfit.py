import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit


t,v=np.loadtxt('dataFFT5/data3.txt',unpack=True)
t = t * 1e-6

init =[1.12e3, -0.0008, 3.5e3, 1600]



##model #AS IT TURNS OUTFY THE FREQ IT IS Enought to fit with a sin

def model(x, omega=2 * np.pi, phi=0, a=1, c=1500):
    return a * np.sin(omega * x + phi) + c
"""def model(x, omega=2 * np.pi, phi=0, a=1, c=1500, iter=1000):
    iter += 1
    f = 0
    x = phi + x
    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.sin(k * x * omega )
    return a * (f - np.mean(f)) + c
"""

tt=np.linspace(min(t),max(t),10000)

popt,pcov=curve_fit(model,t,v,p0=init, absolute_sigma=False)
print(popt,np.sqrt(np.diag(pcov)))

plt.figure()
plt.errorbar(t,v,fmt='o')
plt.plot(tt,model(tt,*popt))
plt.show()

# 1.11876554e+03 +-5.46413047e-03 the good one
# 1.11638970e+03 +-1.39100772e-01 the bad one

f0=1.11876554e+03/(2*np.pi)
sf0=5.46413047e-03/(2*np.pi)
print("f0=",f0,"+-",sf0)

