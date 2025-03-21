import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit


t,v=np.loadtxt('dataFFT5/data6.txt',unpack=True)
t = t * 1e-6

init =[1e3, 0.003, 1.5e3, 1600]



##model #AS IT TURNS OUTFY THE FREQ IT IS Enought to fit with a sin

def model(x, omega=2 * np.pi, dx=0, a=1, c=1500):

    return a * np.sin(omega * (x+dx)) + c

tt=np.linspace(min(t),max(t),10000)

popt,pcov=curve_fit(model,t,v,p0=init, absolute_sigma=False)
print(popt,np.sqrt(np.diag(pcov)))

plt.figure()
plt.errorbar(t,v,fmt='o')
plt.plot(tt,model(tt,*popt))
plt.show()


f0=popt[0]/(2*np.pi)
sf0=np.sqrt(np.diag(pcov))[0]/(2*np.pi)
print("f0=",f0,"+-",sf0)

