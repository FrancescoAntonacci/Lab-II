import numpy as np
import matplotlib.pyplot as plt

filepath = 'rubbish/'
filename = ['09_01-27_02', '24_12-02_01']
filepath_images = 'rubbish/'
plt.rcParams.update({"font.size": 16})

# Create figure with subplots (2 rows, 2 columns)
fig, axes = plt.subplots(2, 2, figsize=(16, 10))  
axes = axes.flatten()

for idx, i in enumerate(filename):
    # Load data
    v = np.loadtxt(filepath + i + '.txt', unpack=True)
    t = np.linspace(0, len(v) / 12, len(v))  # Time in hours
    delta_t = t[1] - t[0]  # Time step
    f_s = 1 / (2 * delta_t)  # Nyquist frequency
    ff = np.fft.rfftfreq(len(t), d=delta_t)  # Proper frequency axis

    # Compute FFT magnitude
    v_tilde = np.abs(np.fft.rfft(v))

    # Reference lines for periodicity markers
    yy = np.linspace(min(v_tilde), max(v_tilde), 4000)
    xx24h = np.full_like(yy, 1 / 24)
    xx6h = np.full_like(yy, 1 / 6)
    xx3h = np.full_like(yy, 1 / 3)

    # Time-domain signal (left column)
    ax_time = axes[idx * 2]  # 0 for first dataset, 2 for second
    ax_time.plot(t, v, label=f'{i} glicemia')
    ax_time.set_xlabel("t [h]")
    ax_time.set_ylabel("Glicemia [mg/dl]")
    ax_time.set_title(f"Glicemia - {i}")
    ax_time.grid()

    # Frequency-domain signal (right column)
    ax_freq = axes[idx * 2 + 1]  # 1 for first dataset, 3 for second
    ax_freq.plot(ff, v_tilde, color='k')
    ax_freq.plot(xx24h, yy, 'y--', label='frequenza di 1 giorno')
    ax_freq.plot(xx3h, yy, 'g--', label='frequenza di 3 ore ')
    ax_freq.plot(xx6h, yy, 'm--', label='frequenza di 6 ore')
    ax_freq.set_xlabel("Frequenza [h$^{-1}$]")
    ax_freq.set_ylabel("ASD [arb. units]")
    ax_freq.set_xlim(0, 0.5)  # Focus on low frequencies
    ax_freq.set_yscale('log')  # Log scale for better visibility
    ax_freq.legend()
    ax_freq.set_title(f"FFT - {i}")
    ax_freq.grid()

# Adjust layout and save
plt.tight_layout()
plt.savefig(filepath_images + 'rubbish.png', dpi=300)
plt.show()
