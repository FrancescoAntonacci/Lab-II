import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

## Belloccerie
fontsize = 14
params = {
    'figure.figsize': (10, 6),          # Figura più ampia
    'axes.labelsize': fontsize,        # Dimensione etichette assi
    'axes.titlesize': fontsize,        # Dimensione titolo
    'xtick.labelsize': fontsize,       # Dimensione tick asse X
    'ytick.labelsize': fontsize,       # Dimensione tick asse Y
    'legend.fontsize': fontsize,       # Dimensione leggenda
    'grid.alpha': 0.6,                 # Trasparenza della griglia
    'grid.linestyle': '--',            # Stile griglia
}
plt.rcParams.update(params)

# Fourier sine series for a triangular wave
def ft(x, iter=1000, a=1, omega=2 * np.pi, phi=0):
    f = 0
    for k in range(1, iter + 1, 2):
        f += ((2 / (k * np.pi)) ** 2) * np.cos(k * x * omega + phi)
    return 2 * a * f

# Analytical triangular wave
def triangwave(x, a, omega=2 * np.pi, phi=0):
    return a * (1 - (2 / np.pi) * np.arccos(np.cos(x * omega + phi)))

# Fourier sine series for a square wave
def fs(x, iter, a, omega=2 * np.pi, phi=0):
    f = 0
    for k in range(1, iter + 1, 2):
        f += (2 / (k * np.pi)) * np.sin(k * x * omega + phi)
    return 2 * a * f

# Analytical square wave
def squarewave(x, a, omega=2 * np.pi, phi=0):
    return a * np.sign(np.sin(x * omega + phi))

# Residuals: Difference between the original wave and Fourier series
def residuals(func, fou, x, iter, pars):
    return func(x, *pars) - fou(x, iter, *pars)

# Compute squared residuals and residual area ratios
def squaredresiduals_and_ratios(func, fou, x, iter, pars):
    residual_sums = []
    residual_areas = []
    for i in iter:
        res = residuals(func, fou, x, i, pars)
        residual_sums.append(np.sum(res ** 2))  # Somma dei residui quadrati
        residual_areas.append(np.sum(np.abs(res)) * (max(x) - min(x)) / len(x))  # Area dei residui
    yy = func(x, *pars)
    area = calc_area(x, yy)
    ratios = np.array(residual_areas) / area  # Rapporto area residui/area totale
    return residual_sums, ratios

def calc_area(x, y):
    return sum(abs(y) * (max(x) - min(x)) / len(x))

# Parametri
maxiter = 3
resolution = int(1e2)
resolutionx=int(1e5)
iter = np.logspace(1, maxiter, resolution, base=10, dtype=int)  # Spaziatura logaritmica
x = np.random.uniform(-1, 1, resolutionx)  # Intervallo di campionamento
pars = (0.5, 2 * np.pi, 0)  # Parametri delle onde

# Calcolo dei residui quadrati e dei rapporti d'area
sq_res, sq_area = squaredresiduals_and_ratios(squarewave, fs, x, iter, pars)
tr_res, tr_area = squaredresiduals_and_ratios(triangwave, ft, x, iter, pars)

# Creazione dei grafici
fig, ax = plt.subplots(1, 2, figsize=(14, 6), sharex=True)

# Grafico residui quadrati
ax[0].plot(iter, sq_res, color='r', label="Onda quadra")
ax[0].plot(iter, tr_res, color='g', label="Onda triangolare")
ax[0].set_title("Residui Quadrati in funzione del numero di iterazioni")
ax[0].set_xlabel("Numero di Iterazioni")
ax[0].set_ylabel("Somma dei Residui Quadrati")
ax[0].set_xscale("log")
ax[0].set_yscale("log")
ax[0].grid(True)
ax[0].legend()

# Grafico rapporto area residui
ax[1].plot(iter, sq_area, color='r', label="Onda quadra")
ax[1].plot(iter, tr_area, color='g', label="Onda triangolare")
ax[1].set_title("Rapporto dell'area tra i grafici con l'area dell'onda ")
ax[1].set_xlabel("Numero di Iterazioni")
ax[1].set_ylabel("Rapporto Area tra i grafici/Area onda")
ax[1].set_xscale("log")
ax[1].set_yscale("log")
ax[1].grid(True)
ax[1].legend()
# Layout finale
fig.tight_layout()

plt.savefig(filepath+"residuals.png")

plt.show()
