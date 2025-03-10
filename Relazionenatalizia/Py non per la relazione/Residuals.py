import numpy as np
from matplotlib import pyplot as plt

filepath = r'/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Materiale/Esercizi/Relazionenatalizia/'

### Aesthetic Settings
fontsize = 14
num_plots = 6
params = {
    'figure.figsize': (6 * 1.618, 6),  # Figure size
    'axes.labelsize': fontsize,        # Axis label size
    'axes.titlesize': fontsize,        # Title size
    'xtick.labelsize': fontsize,       # X-axis tick label size
    'ytick.labelsize': fontsize,       # Y-axis tick label size
    'legend.fontsize': fontsize,       # Legend font size
}
plt.rcParams.update(params)



# Fourier sine series for a triangular wave
def ft(x, iter=1000,a=1, omega=2 * np.pi, phi=0):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += ((2 / (k * np.pi))**2) * np.cos(k * x * omega + phi)
    return a*f

# Analytical triangular wave
def triangwave(x, a, omega=2 * np.pi, phi=0):
    return a * (1-(2/np.pi)*np.arccos(np.cos(x * omega + phi)))

def fs(x,iter,a, omega=2 * np.pi, phi=0):
    iter += 1
    f = 0
    for k in range(1, iter, 2):
        f += (2 / (k * np.pi)) * np.sin(k * x * omega + phi)
    return a*f

# Analytical square wave
def squarewave(x, a, omega=2 * np.pi, phi=0):
    return a * np.sign(np.sin(x * omega + phi))

# Residuals: Difference between square wave and Fourier series
def residuals(func,fou,x,iter, pars): # func is the analytical function, fou is the Fourier series
    return func(x, *pars) - fou(x, iter,*pars)

# Compute squared residuals and residual area ratios
def squaredresiduals_and_ratios(func,fuo,x,iterations, pars):
    residual_sums = []
    residual_areas = []

    for i in iterations:
        res = residuals(func,fuo,x,i, pars)
        residual_sums.append(np.sum(res**2))  # Squared residuals
        residual_areas.append(np.sum(np.abs(res)) * (max(x) - min(x)) / len(x))  # Area of the residuals

    ratios = np.array(residual_areas)   # Ratios of residual area to total area
    return residual_sums, ratios




# Parameters
iter = np.logspace(1, num_plots, num_plots, base=10)  # Logarithmically spaced
res_im = 1000
xx = np.random.uniform(-2, 2, res_im)

pars=(0.5,2*np.pi,0)

################ Logarithmic spacing for iterations
maxiter =3
resolution = int(1e2)
iter = np.logspace(1, maxiter, resolution, base=10, dtype=int)  # Logarithmically spaced

# Compute squared residuals and residual area ratios
sq_res, sq_area = squaredresiduals_and_ratios(squarewave,fs,xx, iter,pars)
tr_res, tr_area = squaredresiduals_and_ratios(triangwave,ft,xx, iter,pars)
# Plot squared residuals vs. iterations
plt.figure()
plt.plot(iter, sq_res, color='b',label="Residui onda quadra")
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Iterations (log scale)', fontsize=fontsize)
plt.ylabel('Squared Residuals (log scale)', fontsize=fontsize)
plt.grid(True)
plt.title('Squared Residuals vs Iterations', fontsize=fontsize)

# Plot residual area ratios vs. iterations
plt.figure()
plt.plot(iter, sq_area, color='r',label="area onda quadra")
plt.xscale('log')
plt.yscale('log')

plt.xlabel('Iterations (log scale)', fontsize=fontsize)
plt.ylabel('Residual Area Ratio', fontsize=fontsize)
plt.grid(True)
plt.title('Residual Area Ratio vs Iterations', fontsize=fontsize)

plt.show()