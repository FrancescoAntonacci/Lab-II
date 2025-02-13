import matplotlib.pyplot as plt
import numpy as np

f = np.array([0.804, 1.627, 2.4464, 6.35, 15.118, 31.026, 46.493])
sigma_f = no.array([0.1, 0.0003, 0.0001, 0.01, 0.001, 0.001, 0.001])
v_in = np.array([20.0, 16.8, 16.0,16.8, 14.0, 11.40, 9.60])
v_out = np.array([0.46, 0.63, 0.68, 0.62, 0.60, 0.568, 0.484])
sigma_vin = np.array([0.6, 0.5, 0.5, 0.5, 0.4, 0.3, 0.2])
sigma_vout = np.array([0.01, 0.03, 0.05, 0.03, 0.02, 0.02, 0.02])

guad = v_out/v_in
sigma_guad = [(sigma_vin/v_in) + (sigma_vout/v_out)]*guad
pl