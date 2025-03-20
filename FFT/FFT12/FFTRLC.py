import numpy as np
import matplotlib.pyplot as plt

# File paths
filepath = 'dataFFT12/'
filename = ['dataFFT01uF', 'dataFFT022uF', 'dataFFT047uF']
filepath_images = 'img/FFT12/'

# Plot settings
plt.rcParams.update({"font.size": 18})

# Constants and uncertainties
C = np.array([1e-7, 2.2e-7, 4.7e-7])
sC = C * 0.2
R = 40.1  # Direct measurement
sR = 0.5
Rfit = np.array([100, 80, 60])
sRfit = np.array([10, 8, 6])
Lfit = np.array([0.7, 0.68, 0.58])
sLfit = np.array([0.07, 0.07, 0.06])
Tfit = np.array([1.6663, 2.4312, 3.2902])
sTfit = np.array([0.0007, 0.0001, 0.0003])
taufit = np.array([13.96e-3, 16.69e-3, 19.16e-3])
staufit = np.array([0.02e-3, 0.03e-3, 0.01e-3])

Tmis=np.array([1.51, 2.31, 3.18])
sTmis=np.array([0.04, 0.07, 0.09])

fmis=np.array([1/T for T in Tmis])
sfmis=fmis*(sTmis/Tmis)

# Frequency calculations
f = 1 / Tfit  # kHz
sf = sTfit / Tfit**2  # kHz

# Create a figure with subplots
fig, axes = plt.subplots(len(filename), 2, figsize=(16, 10), sharex='col', sharey='col')
axes = np.atleast_2d(axes)  # Ensure axes is 2D

for idx, i in enumerate(filename):
    # Load data
    t, v = np.loadtxt(filepath + i + '.txt', unpack=True)
    t = t / 1000  # Convert to ms
    
    # Compute sampling parameters
    delta_t = np.mean(np.diff(t))  # Mean delta_t
    f_s = 1 / (2 * delta_t)
    ff = np.linspace(0, f_s, len(t) // 2 + 1)
    

    # Compute FFT
    v_tilde = abs(np.fft.rfft(v))


    k=np.argmax(v_tilde[1:])+1
    f_fft=ff[k]
    sf_fft=f_s/(len(ff)*np.sqrt(12))

    print("f0_fft=",f_fft,"+-",sf_fft)
    print("f0_bestfit=",f[idx],"+-",sf[idx])
    print("f0_mis=",fmis[idx],"+-",sfmis[idx])
    print()
    
    # Reference lines
    yy = np.linspace(min(v_tilde), max(v_tilde), 4000)
    xx = np.full_like(yy, f[idx])
    xxx=np.full_like(yy,fmis[idx])
    vv = np.linspace(min(v), max(v), 4000)
    TT = np.full_like(vv, Tfit[idx])
    
    # Plot time-domain signal
    axes[idx, 0].plot(t, v, label='Vc(t)')
    axes[idx, 0].plot(TT, vv, 'r--', label='T best-fit')
    axes[idx, 0].grid()
    axes[idx, 0].legend()
    
    # Plot frequency-domain (FFT)
    # Reference lines

    # Shaded regions for uncertainties
    axes[idx, 1].fill_betweenx(yy, f[idx] - sf[idx], f[idx] + sf[idx], color='r', alpha=0.3)
    axes[idx, 1].fill_betweenx(yy, fmis[idx] - sfmis[idx], fmis[idx] + sfmis[idx], color='g', alpha=0.3)

    # Plot frequency-domain (FFT)
    axes[idx, 1].plot(ff, v_tilde, label='ADS dell\'FFT')
    axes[idx, 1].plot(xx, yy, 'r--', label='f0 best-fit')
    axes[idx, 1].plot(xxx, yy, 'g--', label='f0 misurata')

    axes[idx, 1].set_yscale('log')
    axes[idx, 1].set_xlim(-0.1, 5 * f[idx])
    axes[idx, 1].grid()
    axes[idx, 1].minorticks_on()
    axes[idx, 1].legend()



# Add common labels
fig.text(0.74, 0.96, 'Trasformata di Fourier', ha='center', fontsize=18)
fig.text(0.34, 0.96, 'Segnale', ha='center', fontsize=18)

fig.text(0.34, 0.04, 't [ms]', ha='center', fontsize=18)
fig.text(0.74, 0.04, 'f [kHz]', ha='center', fontsize=18)

fig.text(0.04, 0.5, 'Vc(t)[arb. units]', va='center', rotation='vertical', fontsize=18)
fig.text(0.5, 0.5, 'ADS [arb. units]', va='center', rotation='vertical', fontsize=18)

fig.text(0.91, 0.22, 'C=$0.47$[$\mu$F]', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.5, 'C=$0.22$[$\mu$F]', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.77, 'C=$0.1$[$\mu$F]', va='center', rotation='vertical', fontsize=18)

# Show all plots in a single figure
plt.savefig(filepath_images + 'FFTRLC.png')
plt.show()
