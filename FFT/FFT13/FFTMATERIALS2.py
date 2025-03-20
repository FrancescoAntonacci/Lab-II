import numpy as np
import matplotlib.pyplot as plt

# File paths
filepath = 'dataFFT13/'
filename = ['bacchettasermi1','durlindana1',  'combo1']
filepath_images = 'img/FFT13/'

# Plot settings
plt.rcParams.update({"font.size": 18})

# Constants and uncertainties

omega=np.array([2833,2198.4,4016.8]) *1e-3 
somega=np.array([1,0.4,0.8])*1e-3

f=omega/(2*np.pi)
sf=somega/(2*np.pi)

Tfit = 2 * np.pi / omega
sTfit = 2*np.pi*somega/omega**2


# Frequency calculations
f = 1 / Tfit  # kHz
sf = sTfit / Tfit**2  # kHz"""

# Create a figure with subplots
fig, axes = plt.subplots(len(filename), 2, figsize=(16, 10), sharex='col', sharey='col')
axes = np.atleast_2d(axes)  # Ensure axes is 2D

for idx, i in enumerate(filename):
    # Load data
    t,st , v, sv = np.loadtxt(filepath + i + '.txt', unpack=True)
    t = t *1e-3  # Convert to ms
    
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
    print()
    
    # Reference lines
    yy = np.linspace(min(v_tilde), max(v_tilde), 4000)
    xx = np.full_like(yy, f[idx])
    vv = np.linspace(min(v), max(v), 4000)
    TT = np.full_like(vv, Tfit[idx])
    
    # Plot time-domain signal
    axes[idx, 0].plot(t, v, label='Vc(t)')
    axes[idx, 0].plot(TT, vv, 'r--', label='T best-fit')
    axes[idx,0].set_xlim(0,5*max(Tfit))
    axes[idx, 0].grid()
    axes[idx, 0].legend()
    
    # Plot frequency-domain (FFT)
    # Reference lines

    # Shaded regions for uncertainties
    axes[idx, 1].fill_betweenx(yy, f[idx] - sf[idx], f[idx] + sf[idx], color='r', alpha=0.3)

    # Plot frequency-domain (FFT)
    axes[idx, 1].plot(ff, v_tilde, label='ADS dell\'FFT')
    axes[idx, 1].plot(xx, yy, 'r--', label='f0 best-fit')

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

fig.text(0.91, 0.22, 'Profilato e bacchetta', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.5, 'Ferro laminato', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.77, 'Bacchetta di ferro', va='center', rotation='vertical', fontsize=18)


# Show all plots in a single figure
plt.savefig(filepath_images + 'FFTMATERIALS2.png')
plt.show()
