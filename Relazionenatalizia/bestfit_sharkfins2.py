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

def residuals(yy,xx,pars):
    return yy-sharkfin(xx, *pars)


# Caricamento dei dati
data_files = ["data/quadra1.txt", "data/quadra2.txt", "data/quadra3.txt", "data/quadra4.txt"]
initial_guesses = [
    (2 * np.pi / 2.1e5, 5e-5, 0, 3000, 2000),
    (2 * np.pi / 2.2e4, 5e-4, 1, 3000, 2000),
    (2 * np.pi / 2.2e3, 5e-4, 1, 2000, 2000),
    (2 * np.pi / 2.1e2, 5e-4, 1, 1100, 2000),
]

s_v=10 #Basto su esperienze precedenti

# Creazione dei subplot 4x2 con due righe alternate di grafici principali e residui
fig, axes = plt.subplots(4, 2, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1, 2, 1], 'hspace': 0.4, 'wspace': 0.3})
axes = axes.flatten()

# Loop per generare i grafici principali e residui
i=1
for idx, (file, p0) in enumerate(zip(data_files, initial_guesses)):
    j=idx+1
    if idx>1:
        idx+=2

    
    # Caricamento dati
    t, v = np.loadtxt(filepath + file, unpack=True)
    s_v = np.full_like(v, s_v)
    
    # Fit della funzione
    popt, pcov = curve_fit(sharkfin, t, v, sigma=s_v,p0=p0, absolute_sigma=True)
    xx = np.linspace(min(t), max(t), 10000)  # Griglia per il fit
    res = residuals(v, t, popt) / s_v       # Calcolo residui normalizzati
    
    # Grafico principale (colonna sinistra)
    ax_main = axes[idx]  # Subplot per il grafico principale
    ax_main.errorbar(t, v, s_v, fmt='k.', label="Dati sperimentali", alpha=0.8)
    ax_main.plot(xx, sharkfin(xx, *popt), 'r-', label="Best Fit")
    ax_main.set_title(f'Grafico {j}')
    ax_main.grid(True, linestyle='--', alpha=0.5)
    if idx<1:
        ax_main.legend(loc='lower center', bbox_to_anchor=(0.5, 1.15), ncol=2)
    
    # Grafico dei residui (colonna destra)
    ax_res = axes[idx+2]  # Subplot per i residui
    ax_res.plot(t, res, '.r', label="Residui")
    ax_res.set_title(f'Residui Normalizzati {j}')
    ax_res.grid(True, linestyle='--', alpha=0.5)
    i+=1
    ###Printaggio selvaggio dei risultati
    print(f"\n\nBest_fit{idx}")
    print("parametri:", popt)
    print("incertezze:", np.sqrt(pcov.diagonal()))

    corr12 = np.copy(pcov)
    for i in range(len(pcov)):
        for j in range(len(pcov)):
            corr12[i, j] = pcov[i,j]/(np.sqrt(pcov[i, i] * pcov[j, j]))
    print("matrice di correlazione:\n",corr12)
    k2=sum((res/s_v)**2)/(len(v)-len(popt))
    print("x2=",k2)


# Etichette condivise
fig.text(0.5, 0.04, 'Tempo [$\mu$s]', ha='center', va='center', fontsize=fontsize)
fig.text(0.04, 0.5, 'V [arb. un.]', ha='center', va='center', rotation='vertical', fontsize=fontsize)

# Salvataggio e visualizzazione
plt.tight_layout(rect=[0.03, 0.03, 1, 1])
plt.savefig(filepath + "bestfit_sharkfins.png")
plt.show()