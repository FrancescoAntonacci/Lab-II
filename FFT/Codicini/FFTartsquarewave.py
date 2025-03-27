import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

fontsize = 13
params = {'legend.fontsize': fontsize}
plt.rcParams.update(params)

def signal(t, w=2*np.pi, a=1, dt=0, c=0, iter=5000):
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
    t = dt + t
    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.exp(1j * (k * t * w - np.pi / 2))
    return np.real(a * f + c)

# Time values
xx = np.linspace(1, 2, int(1e5))

# Create figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(16, 10), sharex='col', sharey='col')

# Load data
t = xx
v = signal(xx)

# Compute sampling parameters
numpoints = len(t)  
df = 1 / (2 * max(t))
ff = np.linspace(0, df * numpoints, numpoints // 2 + 1)

# Compute FFT
v_tilde = abs(np.fft.rfft(v))

# Find dominant frequency
k = np.argmax(v_tilde[1:]) + 1
f_fft = ff[k]
sf_fft = df / (np.sqrt(12))

print("f0_fft =", f_fft, "+-", sf_fft)

# Plot time-domain signal
axes[0].plot(t, v, label='Segnale')
axes[0].grid()
axes[0].legend(loc='upper right')

# Plot frequency-domain (FFT)
axes[1].plot(ff, v_tilde, label=r"ADS dell'FFT")

axes[1].set_yscale('log')
axes[1].set_xlim(-0.1, 6 * f_fft)
axes[1].grid()
axes[1].minorticks_on()
axes[1].legend(loc='upper right')

# Add common labels
fig.text(0.74, 0.90, 'FFT', ha='center', fontsize=18)
fig.text(0.34, 0.90, 'Segnale', ha='center', fontsize=18)

fig.text(0.34, 0.04, 't [ms]', ha='center', fontsize=18)
fig.text(0.74, 0.04, 'f [kHz]', ha='center', fontsize=18)

fig.text(0.04, 0.5, 'V(t) [arb. units]', va='center', rotation='vertical', fontsize=18)
fig.text(0.5, 0.5, 'ADS [arb. units]', va='center', rotation='vertical', fontsize=18)

fig.text(0.91, 0.22, 'Onda quadra', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.5, 'Onda triangolare', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.77, 'Onda sinusoidale', va='center', rotation='vertical', fontsize=18)

# Show plots
plt.show()
