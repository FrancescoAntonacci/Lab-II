import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from fit import fitting
import os # To list files in a directory (to loop)
# Plotting the rfft of the signal for FFT11 data
# Graphical setting for the plots
fontsize = 14
params = {
    'figure.figsize': (12, 8),  # Dimensione della figura
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









fig, axes = plt.subplots(2, 2, figsize=(20, 10), gridspec_kw={'hspace': 1.5, 'wspace': 0.3})
axes = axes.flatten()
_file = os.getcwd() + "\\dataFFT11\\"
_file = os.listdir(_file)
for el in range(len(_file)):
    _file[el] = os.getcwd() + "\\dataFFT11\\" + _file[el]
init = ((np.pi/(2650*1e-6), 1300, -0.1/(1e6), 1500), # data_11_11 
        (np.pi/(2500*1e-6), 600, 0.1/1e-6, 800),    # data_12_97
        (np.pi/(2500*1e-6), 600, -0.5/1e-6, 800),    # data_13_02
        (np.pi/(2250*1e-6), 250, -0.5/1e-6, 450), # data_13_77
        ##### data 15_06 da far vedere al Fra sperimentale
        ##### PORCODIO anche i data 17_04 speriamo che gli altri siano migliori
        (np.pi/(3100*1e-6), 1500, 1.25/1e-6, 2250), # data6_88
        (np.pi/(3100*1e-6), 1500, 1.25/1e-6, 2250), # data7_08
        (np.pi/(3100*1e-6), 1500, 1.5/1e-6, 2250), # data7_48
        (np.pi/(2900*1e-6), 1500, 5.5/1e-6, 2250), # data8_06,
        (np.pi/(2750*1e-6), 1500, 5.5/1e-6, 1900), # data9_01,
        (np.pi/(2750*1e-6), 1500, 7/1e-6, 1900), #data9_77
        (np.pi/(2650*1e-6), 1600, 5/1e-6, 1800), #data9_92
        )
print(_file[0])
#with open(_file[i], 'r') as file:
#    t, V = np.loadtxt(file, unpack=True)
#    t = t * 1e-6
#    popt, _ = fitting(t, V, init[i])
#    puntifft = int(len(V)/2)
#    plt.figure(1)
#    plt.plot(t, V, label='Func. nel dom. temporale')
#    V = abs(np.fft.rfft(V))
#    # deltaf = (1)/(2 * np.mean(np.diff(t)))
#    deltaf = 1/(max(t))
#    ff = np.linspace(0, deltaf*puntifft, puntifft+1)
#    plt.figure(2)
#    plt.plot(ff, V, label='Func. nel dom. delle freq.')
#    i = 1
#    plt.axhline((1/(np.sqrt(1 + (2 * np.pi * i/omega)))) * (2/(i*np.pi)), color='red', linestyle='--', label='Omega')
#    plt.show()
print(_file[:4])
for el in range(0,len(_file[:4])):
   with open(_file[el], 'r') as file:
        t, V = np.loadtxt(file, unpack=True)
        ax_main = axes[el]  # Subplot per il grafico principale
        # ax_main.errorbar(t, V, fmt='.', label="Dati sperimentali", alpha=0.8)
        puntifft = int(len(V)/2)
        t = t * 1e-6
        popt, _ = fitting(t, V, init[el])
        V= abs(np.fft.rfft(V))
        deltaf = (1)/(max(t))
        ff = np.linspace(0, deltaf*puntifft, puntifft+1)
        ax_main.plot(ff, V, 'r-', label="Best Fit")
        ax_main.set_yscale('log')
        ax_main.set_title(f'Grafico {el+1}')
        ax_main.grid(True, linestyle='--', alpha=0.5)
        ax_main.axvline(popt[0]/(2*np.pi), color='black', linestyle='--')
        #if idx<1:
        #    ax_main.legend(loc='lower center', bbox_to_anchor=(0.5, 1.15), ncol=2)
fig.supxlabel('Frequenze [kHz]', fontsize=fontsize)
fig.supylabel('V [arb. un.]', fontsize=fontsize)

# Salvataggio e visualizzazione
plt.tight_layout(rect=[0.05, 0.05, 1, 1])
plt.show()