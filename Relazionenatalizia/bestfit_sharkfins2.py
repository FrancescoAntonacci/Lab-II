import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 18
params = {
    'figure.figsize': (12, 8),  # Dimensione della figura
    'axes.labelsize': fontsize,
    'axes.titlesize': fontsize,
    'xtick.labelsize': fontsize,
    'ytick.labelsize': fontsize,
    'legend.fontsize': fontsize,
    'lines.linewidth': 2,  # Spessore delle linee
    'lines.markersize': 6  # Dimensione dei marker
}
plt.rcParams.update(params)
plt.style.use('seaborn-v0_8-muted')  # Stile pulito

# Funzioni
def G_lpf(omega, ft=1000):
    f = omega / (2 * np.pi)
    return 1 / np.sqrt(1 + (f / ft)**2)

def dphi_lpf(omega, ft=1000):
    f = omega / (2 * np.pi)
    return np.arctan(-f / ft)

def sharkfin(x, omega=2 * np.pi, ft=1e1, phi=0, a=1, c=0, iter=1000):
    iter += 1
    f = 0
    x = phi + x
    for k in range(1, iter, 2):
        dphi = dphi_lpf(k * omega, ft)
        G = G_lpf(k * omega, ft)
        f += G * (2 / (k * np.pi)) * np.sin(k * x * omega + dphi)
    return a * (f - np.mean(f)) + c

# Caricamento dei dati
data_files = ["data/quadra1.txt", "data/quadra2.txt", "data/quadra3.txt", "data/quadra4.txt"]
initial_guesses = [
    (2 * np.pi / 2.1e5, 5e-5, 0, 3000, 2000),
    (2 * np.pi / 2.2e4, 5e-4, 1, 3000, 2000),
    (2 * np.pi / 2.2e3, 5e-4, 1, 2000, 2000),
    (2 * np.pi / 2.1e2, 5e-4, 1, 1100, 2000),
]

# Creazione dei subplot
fig, axes = plt.subplots(2, 2, figsize=(12, 8), gridspec_kw={'hspace': 0.2, 'wspace': 0.15})
axes = axes.flatten()

# Loop per generare i grafici
for i, file in enumerate(data_files):
    # Carica i dati
    t, v = np.loadtxt(filepath + file, unpack=True)
    
    # Crea un array per il fit più fluido
    xx = np.linspace(min(t), max(t), 10000)
    
    # Parametri iniziali per il fit
    p0 = initial_guesses[i]
    popt, _ = curve_fit(sharkfin, t, v, p0=p0, absolute_sigma=False)
    
    # Plot sui subplot
    ax = axes[i]
    ax.errorbar(t, v, fmt='k.', label="Dati sperimentali", capsize=3, alpha=0.8)
    ax.plot(xx, sharkfin(xx, *popt), 'r-', label="Best Fit", alpha=0.9)
    ax.set_title(f'Grafico {i+1}')
    ax.grid(True, which='both', linestyle='--', alpha=0.5)

    # Spostare la legenda fuori dall'area del grafico
    ax.legend(loc='lower right', ncol=1)

# Etichette condivise
fig.text(0.5, 0.04, 'Tempo [ns]', ha='center', va='center', fontsize=fontsize)  # Etichetta asse x
fig.text(0.04, 0.5, 'Segnale [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=fontsize)  # Etichetta asse y

# Salvataggio e visualizzazione
plt.tight_layout(rect=[0.03, 0.03, 1, 1])  # Margini ottimizzati
plt.savefig(filepath + "bestfit_sharkfins.png")
plt.show()
