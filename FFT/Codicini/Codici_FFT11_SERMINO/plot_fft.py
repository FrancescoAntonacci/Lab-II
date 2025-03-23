import numpy as np
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from fit import fitting
import os  # To list files in a directory (to loop)

# Plotting the rfft of the signal for FFT11 data
# Graphical setting for the plots
fontsize = 18
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

_file = os.getcwd() + "\\dataFFT11\\"
_file = os.listdir(_file)
_file = [x for x in _file if ".txt" in x]
print(_file)
for el in range(len(_file)):
    _file[el] = os.getcwd() + "\\dataFFT11\\" + _file[el]

init = ((np.pi/(2650*1e-6), 1300, -0.1/(1e6), 1500),  # data_11_11 
        (np.pi/(2500*1e-6), 600, 0.1/1e-6, 800),    # data_12_97
        (np.pi/(2500*1e-6), 600, -0.5/1e-6, 800),    # data_13_02
        (np.pi/(2250*1e-6), 250, -0.5/1e-6, 450),  # data_13_77
        (np.pi/(4.25 * 2650*1e-6), 5, 1/1e-6, 235),  # data 15_06
        (np.pi/(4.25 * 2650*1e-6), 5, 1/1e-6, 235),  # data 17_04
        (np.pi/(3100*1e-6), 1500, 1.25/1e-6, 2250),  # data6_88
        (np.pi/(3100*1e-6), 1500, 1.25/1e-6, 2250),  # data7_08
        (np.pi/(3100*1e-6), 1500, 1.5/1e-6, 2250),  # data7_48
        (np.pi/(2900*1e-6), 1500, 5.5/1e-6, 2250),  # data8_06
        (np.pi/(2750*1e-6), 1500, 5.5/1e-6, 1900),  # data9_01
        (np.pi/(2750*1e-6), 1500, 7/1e-6, 1900),  # data9_77
        (np.pi/(2650*1e-6), 1600, 5/1e-6, 1800),  # data9_92
        )
# Plotting gruppi di 4
num_sig = int(input("Quanti segnali vuoi visualizzare in una finestra? (Sconsigliato andare oltre i 4) "))

i = 0
while i < len(_file):
    if i + num_sig < len(_file):
        fig, axes = plt.subplots(2, 2, figsize=(45, 15), gridspec_kw={'hspace': 0.5, 'wspace': 0.3})
        axes = axes.flatten()
        
        for j in range(num_sig):
            with open(_file[i + j], 'r') as file:
                t, V = np.loadtxt(file, unpack=True)
                t = t * 1e-6
                popt, pcov = fitting(t, V, init[i + j])
                
                # Grafico del segnale a sinistra
                ax_left = axes[2 * j]
                ax_left.plot(t, V, 'r-', label="Segnale")
                ax_left.set_title(f'Segnale {i + j + 1}')
                ax_left.grid(True, linestyle='--', alpha=0.5)
                puntifft = int(len(V) / 2)
                
                # Grafico della rfft a destra
                ax_right = axes[2 * j + 1]
                V = abs(np.fft.rfft(V))
                deltaf = (1) / max(t)
                ff = np.linspace(0, deltaf * puntifft, puntifft + 1)
                ax_right.plot(ff, V, 'blue', label="ADS della FFT")
                ax_right.set_yscale('log')
                ax_right.set_title(f'FFT {i + j + 1}')
                ax_right.grid(True, linestyle='--', alpha=0.5)
                ax_right.axvline(popt[0] / (2 * np.pi), color='red', linestyle='--', label='Valore atteso dal best-fit')
                s_w = np.sqrt(np.diag(pcov))[0]
                ax_right.fill_betweenx([min(V), max(V)], (popt[0] - s_w) / (2 * np.pi), (popt[0] + s_w) / (2 * np.pi), color='r', alpha=0.5)
                ax_right.legend()
                print(f"La frequenza stimata è: {popt[0] / (2 * np.pi)} +- {s_w} con un deltaf pari a {deltaf/np.sqrt(12)}")
        
        # Etichette personalizzate per gli assi X e Y
        fig.text(0.29, 0.02, 'Tempo [s]', ha='center', va='center', fontsize=14)   # Etichetta X per i grafici a sinistra
        fig.text(0.735, 0.02, 'Frequenza [Hz]', ha='center', va='center', fontsize=14)  # Etichetta X per i grafici a destra
        
        fig.text(0.02, 0.5, 'V [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=14)  # Etichetta Y per i grafici a sinistra
        fig.text(0.50, 0.5, 'ASD del segnale [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=14)  # Etichetta Y per i grafici a destra
        
        plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
        plt.show()
        i += num_sig
    else:
        with open(_file[i], 'r') as file:
            fig, axes = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={'hspace': 1.5, 'wspace': 0.3})
            t, V = np.loadtxt(file, unpack=True)
            t = t * 1e-6
            ax_left = axes[0]
            deltaf = (1) / max(t)
            puntifft = int(len(V) / 2)
            ax_left.plot(t, V, 'blue', label="Segnale")
            ax_left.set_title(f'Segnale {i + 1}')
            ax_left.grid(True, linestyle='--', alpha=0.5)
            
            popt, pcov = fitting(t, V, init[i])
            V = abs(np.fft.rfft(V))
            ff = np.linspace(0, deltaf * puntifft, puntifft + 1)
            
            ax_right = axes[1]
            ax_right.plot(ff, V, 'blue', label="Best Fit")
            ax_right.set_yscale('log')
            ax_right.set_title(f'FFT {i + 1}')
            ax_right.grid(True, linestyle='--', alpha=0.5)
            ax_right.axvline(popt[0] / (2 * np.pi), color='red', linestyle='--', label='Valore atteso dal best-fit')
            s_w = np.sqrt(np.diag(pcov))[0]
            ax_right.fill_betweenx([min(V), max(V)], (popt[0] - s_w) / (2 * np.pi), (popt[0] + s_w) / (2 * np.pi), color='r', alpha=0.5)
            ax_right.legend()
            
            fig.text(0.29, 0.02, 'Tempo [s]', ha='center', va='center', fontsize=14)
            fig.text(0.735, 0.02, 'Frequenza [Hz]', ha='center', va='center', fontsize=14)
            fig.text(0.02, 0.5, 'V [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=14)
            fig.text(0.50, 0.5, 'ASD del segnale [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=14)
            
            plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
            plt.show()
        i += 1
