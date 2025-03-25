import numpy as np
import matplotlib.pyplot as plt

fontsize = 18
params = {
    'figure.figsize': (15, 8),  # Dimensione della figura
    'axes.labelsize': fontsize,
    'axes.titlesize': fontsize,
    'xtick.labelsize': fontsize,
    'ytick.labelsize': fontsize,
    'legend.fontsize': fontsize,
    'lines.linewidth': 2,
    'lines.markersize': 6
}
plt.rcParams.update(params)
plt.style.use('seaborn-v0_8-muted')  # Stile pulito

wosc=1e1
C = 1e-6  # F
r1=30
r2=68
R = r1+r2  # ohm
a = 1  # volts
dt=0  # rad
L=0.4
c=0
rG=40
toscmax=0.06
wgenfun=1e1

w0=1/np.sqrt(L*C)
tau = 2*L/R  # s
tau0=r2*C   #s tau of the resistor and capacitor

w=np.sqrt(w0**2-1/tau**2)
theta=-np.arctan(w*tau)


# Define v0 (source voltage)
def T_AC(w,wosc):
    """
    Transfer function of the circuit when the oscilloscope is in AC mode

    Params:
    -------
    w: float
        Frequency of the signal
    wosc: float
        Frequency of the oscillation/oscilloscope?
    
    Returns:
    --------
    T: float
        Value of the transfer function with given values of w and wosc
    """
    return 1/(1-1j*wosc/w)


def vc(t, w, tau, a, dt):
    return a  * np.exp(-t/tau+1j * (w * (t+dt) ))


def vc_AC(t, w, tau, a, dt):
    return a  *T_AC(w,wosc)* np.exp(-t/tau+1j * (w * (t+dt) ))


def vr2(t, w, tau,tau0, a, dt,theta):
    return a*(tau0/tau)*np.sqrt(1+(tau*w)**2)  * np.exp(-t/tau+1j * (w * (t+dt)+theta))


def vr2_AC(t, w, tau,tau0, a, dt,theta):
    return a*T_AC(w,wosc)*(tau0/tau)*np.sqrt(1+(tau*w)**2)  * np.exp(-t/tau+1j * (w * (t+dt)+theta))


def vwc_AC(t, w, a, dt,c, iter=10000):
    """
    Real amplitude of the signal exiting the capacitator in AC mode

    Params:
    -------
    t: float
        list of time values
    w: float
        Frequency of the signal
    a: float
        Amplitude of the signal
    dt: float
        Time step?
    c: float
        offset of the signal
    iter: int
        Number of Fourier terms to consider
    
    Returns:
    --------
    f: float
        Real amplitude of the signal
    """
    iter += 1
    f = 0
    t = dt + t-toscmax
    for k in range(1, iter, 2):
        z1=1/(1j*(w*k)*C)
        z2=(r1+r2+1j*(w*k)*L)
        z=(rG+1/((1/z1)+(1/z2)))
        f += T_AC(w*k,wosc)*(1-rG/z)*(2 / (k * np.pi)) * np.exp(1j*(k * t * w-np.pi/2))
    return np.real(a *f+ c)


def vwc(t, w, a, dt,c, iter=10000):
    """
    Real amplitude of the signal exiting the capacitator

    Params:
    -------
    t: float
        list of time values
    w: float
        Frequency of the signal
    a: float
        Amplitude of the signal
    dt: float
        Time step?
    c: float
        offset of the signal
    iter: int
        Number of Fourier terms to consider
    
    Returns:
    --------
    f: float
        Real amplitude of the signal
    """
    iter += 1
    f = 0
    t = dt + t-toscmax
    for k in range(1, iter, 2):
        z1=1/(1j*(w*k)*C)
        z2=(r1+r2+1j*(w*k)*L)
        z=(rG+1/((1/z1)+(1/z2)))
        f += (1-rG/z)*(2 / (k * np.pi)) * np.exp(1j*(k * t * w-np.pi/2))
    return np.real(a *f+ c)


def vwr_AC(t, w, a, dt,c, iter=10000):
    """
    Real amplitude of the signal exiting the inductor in AC mode

    Params:
    -------
    t: float
        list of time values
    w: float
        Frequency of the signal
    a: float
        Amplitude of the signal
    dt: float
        Time step?
    c: float
        offset of the signal
    iter: int
        Number of Fourier terms to consider
    """
    iter += 1
    f = 0
    t = dt + t-toscmax
    for k in range(1, iter, 2):
        z1=1/(1j*(w*k)*C)
        z2=(r1+r2+1j*(w*k)*L)
        z=(rG+1/((1/z1)+(1/z2)))
        zl=1j*(k*w)*L+r1
        f += T_AC(w*k,wosc)*(1-rG/z-(zl*z1/(z1*z+z2*z)))*(2 / (k * np.pi)) * np.exp(1j*(k * t * w-np.pi/2))
    return np.real(a * f + c)


def vwr(t, w, a, dt,c, iter=10000):
    """
    Real amplitude of the signal exiting the inductor 

    Params:
    -------
    t: float
        list of time values
    w: float
        Frequency of the signal
    a: float
        Amplitude of the signal
    dt: float
        Time step?
    c: float
        offset of the signal
    iter: int
        Number of Fourier terms to consider
    """
    iter += 1
    f = 0
    t = dt + t-toscmax
    for k in range(1, iter, 2):
        z1=1/(1j*(w*k)*C)
        z2=(r1+r2+1j*(w*k)*L)
        z=(rG+1/((1/z1)+(1/z2)))
        zl=1j*(k*w)*L+r1
        f += (r2*z1/(z1*z+z2*z))*(2 / (k * np.pi)) * np.exp(1j*(k * t * w-np.pi/2))
    return np.real(a * f + c)


def signal(t, w, a, dt,c, iter=10000):
    """
    Real amplitude of the signal exiting the function generator (in AC mode??)

    Params:
    -------
    t: float
        list of time values
    w: float
        Frequency of the signal
    a: float
        Amplitude of the signal
    dt: float
        Time step?
    c: float
        offset of the signal
    iter: int
        Number of Fourier terms to consider

    Returns:
    --------
    f: float
        Real amplitude of the signal
    """
    iter += 1
    f = 0
    t = dt + t-toscmax
    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.exp(1j*(k * t * w-np.pi/2))
    return np.real(a * f + c)

tt1 = np.linspace(0, toscmax, 5000)
tt2=np.linspace(toscmax,0.2, 5000)

fig, axes = plt.subplots(2, 2, figsize=(16, 10), sharex='col', sharey='col',  gridspec_kw={'hspace': 0.5, 'wspace': 0.3})

axes[0,0].plot(tt1, np.real(vc_AC(tt1, w, tau, 0.4*a, dt)), label="vc(t)")
axes[0,0].plot(tt1,np.real(vr2_AC(tt1, w, tau,tau0, 0.4*a, dt,theta)), label="vr2(t)")
axes[0,0].plot(tt2,np.real(vwc_AC(tt2,wgenfun,a,dt,c))+ np.real(vc_AC(tt2, w, tau, 0.4*a, dt)))
axes[0,0].plot(tt2,np.real(vwr_AC(tt2,wgenfun,a,dt,c))+np.real(vr2_AC(tt2, w, tau,tau0, 0.4*a, dt,theta)))
axes[0,0].set_title("Segnali oscilloscopio in AC")
axes[0,0].set_xlabel("t[arb.un]")
axes[0,0].set_ylabel("V[arb.un]")
axes[0, 0].legend()

axes[0,1].plot(np.real(vc(tt1, w, tau, 0.4*a, dt)),np.real(vr2(tt1, w, tau,tau0, 0.4*a, dt,theta)), label="XY")
axes[0,1].plot(np.real(vwc_AC(tt2,wgenfun,a,dt,c))+ np.real(vc_AC(tt2, w, tau, 0.4*a, dt)),np.real(vwr_AC(tt2,wgenfun,a,dt,c))+ np.real(vr2_AC(tt2, w, tau,tau0, 0.4*a, dt,theta)))
axes[0,1].set_title("Segnali XY oscilloscopio in AC")
axes[0,1].set_xlabel("V[arb.un]")
axes[0,1].set_ylabel("V[arb.un]")
axes[0,1].legend()


axes[1,0].plot(tt1, np.real(vc(tt1, w, tau, 0.4*a, dt)), label="vc(t)")
axes[1,0].plot(tt1,np.real(vr2(tt1, w, tau,tau0, 0.4*a, dt,theta)), label="vr2(t)")
axes[1,0].plot(tt2,vwc(tt2,wgenfun,a,dt,c)+ np.real(vc(tt2, w, tau, 0.4*a, dt)))
axes[1,0].plot(tt2,vwr(tt2,wgenfun,a,dt,c)+np.real(vr2(tt2, w, tau,tau0, 0.4*a, dt,theta)))
axes[1,0].set_title("Segnali ")
axes[1,0].set_xlabel("t[arb.un]")
axes[1,0].set_ylabel("V[arb.un]")
axes[1,0].legend()

axes[1,1].plot(np.real(vc(tt1, w, tau, 0.4*a, dt)),np.real(vr2(tt1, w, tau,tau0, 0.4*a, dt,theta)), label="XY")
axes[1,1].plot(vwc(tt2,wgenfun,a,dt,c)+ np.real(vc(tt2, w, tau, 0.4*a, dt)),vwr(tt2,wgenfun,a,dt,c)+np.real(vr2(tt2, w, tau,tau0, 0.4*a, dt,theta)))
axes[1,1].set_title("Segnali XY")
axes[1,1].set_xlabel("t[arb.un]")
axes[1,1].set_ylabel("V[arb.un]")
axes[1, 1].legend()
plt.show()