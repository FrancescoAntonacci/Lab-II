import numpy as np
i_c = np.array([1.60, 1.80, 3.80, 4.62, 2.20, 2.19])
i_c = i_c * 1e-3
sigma_ic = np.ones_like(0.05e-3, shape=len(i_c))

i_b = np.array([8.88, 9.82, 18.4, 39.0, 39.9, 18.4])
i_b = i_b * 1e-6
sigma_ib = np.array([0.05, 0.06, 0.2, 0.4, 0.5, 0.2])
sigma_ib = sigma_ib * 1e-6
beta = i_c / i_b
sigma_beta = []
for el in range(len(i_c)):
    sigma_beta = ((sigma_ib/i_b) + (sigma_ic/i_c))*beta
print(f"val: {beta} +- {sigma_beta}")