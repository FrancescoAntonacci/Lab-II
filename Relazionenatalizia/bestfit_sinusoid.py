import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
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

### Funzione Sinusoidale
def ff(x, omega, phi, a, c):
    return a * np.sin(omega * x + phi) + c

# Caricamento dei dati
data_files = ["data/sin1.txt", "data/sin2.txt", "data/sin3.txt", "data/sin4.txt"]
initial_guesses = [
    (2.8 / 1e5, -1, 1300, 2000),
    (2.8 / 1e4, -1, 1300, 2000),
    (2.8 / 1e3, -1.2, 500, 2000),
    (2.8 / 1e2, -1.4, 60, 2050),
]

# Creazione dei subplot
fig, axes = plt.subplots(2, 2, figsize=(12, 8), gridspec_kw={'hspace': 0.3, 'wspace': 0.2})
axes = axes.flatten()

# Loop per generare i grafici
for i, file in enumerate(data_files):
    # Carica i dati
    t, v = np.loadtxt(filepath + file, unpack=True)
    
    # Genera una griglia per il fit
    xx = np.linspace(min(t), max(t), 10000)
    
    # Parametri iniziali e fit
    p0 = initial_guesses[i]
    popt, _ = curve_fit(ff, t, v, p0=p0)
    
    # Plot sui subplot
    ax = axes[i]
    ax.errorbar(t, v, fmt='k.', label="Dati sperimentali", alpha=0.8)  # Dati in nero
    ax.plot(xx, ff(xx, *popt), 'r-', label="Best Fit")  # Fit in rosso
    
    # Titoli e griglia
    ax.set_title(f'Grafico {i+1}')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)

# Etichette condivise per gli assi
fig.text(0.5, 0.04, 'Tempo [ns]', ha='center', va='center', fontsize=fontsize)
fig.text(0.04, 0.5, 'Segnale [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=fontsize)

# Salvataggio e visualizzazione
plt.tight_layout(rect=[0.03, 0.03, 1, 1])
plt.savefig(filepath + "bestfit_sinusoide.png")
plt.show()
