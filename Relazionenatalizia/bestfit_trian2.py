import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 14
params = {
    'figure.figsize': (12, 10),  # Dimensione della figura
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

### Funzioni
def G_lpf(omega, ft=1000):
    f = omega / (2 * np.pi)
    return 1 / np.sqrt(1 + (f / ft)**2)

def dphi_lpf(omega, ft=1000):
    f = omega / (2 * np.pi)
    return np.arctan(-f / ft)

def ff(x, a, omega, phi, c, ft, iter=1000):
    iter += 1
    f = 0
    x = phi + x
    for k in range(1, iter, 2):
        f += G_lpf(omega, ft) * ((2 / (k * np.pi))**2) * np.cos(k * x * omega + dphi_lpf(omega, ft))
    f = f - np.mean(f)
    return a * f + c

def sin(x, a, omega, phi, c):
    return a * np.sin(omega * x + phi) + c

### Caricamento dei dati
data_files = [
    "data/trian1.txt", "data/trian2.txt", 
    "data/trian3.txt", "data/trian4bis.txt"
]
initial_guesses = [
    (2.6e3, 2 * np.pi / 2.1e5, 0.1e6, 2000, 1e-3),
    (2.6e3, 2 * np.pi / 2.1e4, 2e5, 2000, 1e-3),
    (2.6e3, 2 * np.pi / 2.1e3, 2e5, 2000, 1e-3),
    (2.6e3, 2 * np.pi / 2.1e2, 2e5, 2000, 1e-3)
]

# Creazione dei subplot 2x2
fig, axes = plt.subplots(2, 2, figsize=(12, 10), gridspec_kw={'hspace': 0.4, 'wspace': 0.3})
axes = axes.flatten()

# Loop per generare i grafici
for i, (file, p0) in enumerate(zip(data_files, initial_guesses)):
    # Carica i dati
    t, v = np.loadtxt(filepath + file, unpack=True)
    
    # Griglia per il fit
    xx = np.linspace(min(t), max(t), 10000)
    
    # Fit della funzione
    popt, _ = curve_fit(ff, t, v, p0=p0, absolute_sigma=False)
    
    # Plot nel subplot corrispondente
    ax = axes[i]
    ax.errorbar(t, v, fmt='k.', label="Dati sperimentali", alpha=0.8)  # Punti neri
    ax.plot(xx, ff(xx, *popt), 'r-', label="Best Fit")  # Fit in rosso
    
    # Titoli e griglia
    ax.set_title(f'Grafico {i+1}')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.15), ncol=2)

# Rimuovere subplot vuoti se ci sono meno dati
if len(data_files) < len(axes):
    for j in range(len(data_files), len(axes)):
        fig.delaxes(axes[j])

# Etichette condivise
fig.text(0.5, 0.04, 'Tempo [ns]', ha='center', va='center', fontsize=fontsize)
fig.text(0.04, 0.5, 'Segnale [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=fontsize)

# Salvataggio e visualizzazione
plt.tight_layout(rect=[0.03, 0.03, 1, 1])
plt.savefig(filepath + "bestfit_triangle.png")
plt.show()
