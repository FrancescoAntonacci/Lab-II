import matplotlib.pyplot as plt
import numpy as np
data = "/home/studentelab2/doppi_fra/Lab2_26112024/data.txt"
data_2 = "/home/studentelab2/doppi_fra/Lab2_26112024/data_2.txt"

f, v_1, v_2 = np.loadtxt(data, unpack=True)
sigma_f = f * (5/100)
sigma_v_1 = v_1 * (3/100)
sigma_v_2 = v_2 * (3/100)

print(f"Il guadagno in onde quadre {v_1 /v_2}")

f, t_1, t_2, s_1, s_2 = np.loadtxt(data_2, unpack=True)
print(f"Il guadagno in onde triangolari {t_1/t_2}")
print(f"Il guadagno in onde sinusoidali {s_1/s_2}")

