import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

fontsize=20
params={
    'figure.figsize': (12,8),
    'axes.labelsize': fontsize,
    'axes.titlesize': fontsize,
    'xtick.labelsize': fontsize,
    'ytick.labelsize': fontsize,
    'legend.fontsize': fontsize
}
plt.rcParams.update(params)
dati = "/home/studentelab2/doppi_fra/Lab2_11032025/data/"
file = ["nulla1.txt", "bacchettasermi1.txt", "buho1.txt", "combo1.txt", "durlindana1.txt", "pieno1.txt","quellechemifaccioio.txt"]
def model(t, A, tau, omega, phi, c):
    return A * np.exp(- t/tau) * np.cos(omega * t + phi) + c

C = 0.1e-6
init = [[1200, 0.02, 3.8e3, np.pi/2, 1900],
[1200, 0.002, 3.8e3, np.pi/2, 1900],
[1200, 0.02, 3.8e3, np.pi/2, 1900],
[1200, 0.02, 3.8e3, np.pi/2, 1900],
[1200, 0.02, 3.8e3, np.pi/2, 1900],
[1200, 0.02, 3.8e3, np.pi/2, 1900], [1200, 0.02, 3.8e3, np.pi/2, 1900], [1200, 0.02, 3.8e3, np.pi/2, 1900]]
"""
t, st, V, sV = np.loadtxt(dati+"pieno1.txt", unpack=True)
t = t * 1e-6
st = st * 1e-6
plt.errorbar(t, V, xerr=st, yerr=sV, fmt='o')
tt = np.linspace(min(t), max(t), 3000)
plt.plot(tt, model(tt, *init[1]), label="guess")
pars, covm = curve_fit(model, t, V, sigma=sV, absolute_sigma=True, p0=init[5])
plt.plot(tt, model(tt, *pars), label="fit")
plt.legend()
plt.show()
"""
for i in range(len(file)):
    print(f"{i+1}-fit: file {file[i]}")
    t, st, V, sV = np.loadtxt(dati+file[i], unpack=True)
    t = t * 1e-6
    st = st * 1e-6
    ##

    pars, covm = curve_fit(model, t, V, sigma=sV, absolute_sigma=True, p0=init[i])
    ##



    tt = np.linspace(min(t), max(t), 3000)

    plt.figure()
    plt.errorbar(t, V, xerr=st, yerr=sV, fmt='o', label="Dati")
    plt.plot(tt, model(tt,*pars), label="Best-fit")
    plt.xlabel(r"$t$ [s]")
    plt.ylabel(r"$V$ [arb. un.]")
    plt.title(f"{i+1} fit")
    plt.legend()
    #plt.show()


    ##
    res=(V-model(t,*pars))/sV
    x2norm=sum(res**2)/len(res)
    print("X2norm:",x2norm)
    Q=pars[2] * pars[1]/2
    sQ=np.sqrt((pars[1]**2)*covm[2,2]+covm[1,1]*(pars[2]**2))

    print(f"Fattore di qualità: {Q} +- {sQ}")
    print(f"L: {1/(C * (pars[2]**2 - (pars[1])**(-2)))} +-{0.1/(C * (pars[2]**2 - (pars[1])**(-2)))}")


    pars[1]=pars[1]*1e3
    covm[1,1]=covm[1,1]*1e6
    print("Parametri di best fit:",pars)
    print("Incertezze:",np.sqrt(covm.diagonal()))


    print("\n \n \n")