import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, ifft, fftshift
t, x = np.loadtxt("/home/studentelab2/doppi_fra/Lab2_11112024/sinusoide.txt", unpack=True)
fourier = fftshift(fft(x))
print(fourier)
plt.figure(1)
plt.plot(t, x, marker='o')
plt.show()