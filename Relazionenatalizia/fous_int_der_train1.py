import numpy as np
from matplotlib import pyplot as plt
##  Code to generate the plots of an integrator, derivator and band-pass filter of a train pulse wave
##  The function ff generates the Fourier series of a train pulse wave
##  The function fi generates the Fourier series of a low-pass filter of a train pulse wave (the 'i' means integrator)
##  The function fd generates the Fourier series of a high-pass filter of a train pulse wave (the 'd' means derivator)
##  Change the function where in the for cycle denoted by the comment "Ciclo per creare i plot" to generate the plots of the integrator, derivator and band-pass filter
filepath = r'./'

### Aesthetic Settings
fontsize = 18
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

# Fourier sine series for a train pulse wave
def ff(x, a=1, omega=2 * np.pi, delta=0.3, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += (2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega)
    return a * f 

# Fourier sine series for a low-pass pulse wave
def fi(x, a=1, omega=2 * np.pi, delta=0.3,ft=1e-3, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += G_lpf(k*omega,ft)*(2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega+dphi_lpf(k*omega,ft))
    return a * f 

#Fourier sine series for a high-pass pulse wave
def fd(x, a=1, omega=2 * np.pi, delta=0.3,ft=1e1, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += G_hpf(k*omega,ft)*(2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega+dphi_hpf(k*omega,ft))
    return a * f 

# Fourier sine series for a band-pass pulse wave
def fpb(x, a=1, omega=2 * np.pi, delta=0.3,ft1=1e1,ft2=1e-3, iter=1000):
    iter += 1
    f = 0
    for k in range(1, iter):
        f += G_lpf(k*omega,ft2)*G_hpf(k*omega,ft1)*(2 / (k * np.pi)) * np.sin(np.pi * k * delta) * np.cos(k * x * omega+dphi_hpf(k*omega,ft1)+dphi_lpf(k*omega,ft2))
    return a * f 



##################
def G_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(f/ft)**2)
def dphi_lpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(-f/ft)

def G_hpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return 1/np.sqrt(1+(ft/f)**2)
def dphi_hpf(omega,ft=1000):
    f=omega/(2*np.pi)
    return np.arctan(ft/f)





res_im = 100000
xx = np.linspace(-1, 1, res_im)
ft=(1e-3,1e-2,1e-1,1e-0,1e1,1e2)


fig, axes = plt.subplots(int(len(ft)/2), 2, sharex=True, figsize=(12, len(ft)))
axes=axes.flatten()
## --------- FOR LOOP TO CREATE PLOTS ------------
# Ciclo per creare i plot
for i, ax in enumerate(axes):
    ft_iteration=ft[i]
    ax.plot(xx, fi(xx,ft=ft_iteration ))
    ax.set_title(f'$ft1,ft2={ft_iteration}$[arb.un.]')
    ax.grid(True)

# Add shared labels for x and y axes
fig.supxlabel('t  [arb.un.]', fontsize=fontsize)  # Shared x-axis label
fig.supylabel('x(t)[arb.un.]', fontsize=fontsize)  # Shared y-axis label

# Save and display the figure
plt.tight_layout()  # Adjust layout to avoid overlaps
plt.savefig(filepath + "int_train1.png")  # Save the plot as an image
plt.show()  # Display the plot
