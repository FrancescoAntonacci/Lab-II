import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Caricamento dati
def load_data(filename):
    t, V = np.loadtxt(filename, unpack=True)
    t = t * 1e-6  # Conversione in secondi se necessario
    return t, V

def anal(t,w,a,phi, c):
    return a * np.sin(w * t + phi) + c

def fitting(t, V, init):
    return curve_fit(anal, t, V, p0=init)

if __name__ == "__main__":
    init = (np.pi/(2650*1e-6), 10, 5/1e-6, 230)
    # Import niggers from africa s
    t, V = load_data("C:\\Users\\franc\\Lab-II\\FFT\\dataFFT11\\data_15_06.txt")

    # Fit della serie di STOCAZZONEEEEEEEEEEEEEEEEEEEEEE
    popt, _ = fitting(t, V, init)

    # Stima della frequenza ducica di taglio (scrivo 3 volte duce nella scheda elettorale-FSK GANG NO SNITCH)
    print(f"Heil omega di taglio ducizzata è: {popt[0]} +- {np.sqrt(np.diag(_))[0]}")

    tt=np.linspace(min(t),max(t),4000)
    plt.figure()
    plt.plot(t,V, label='CAZZI NEL CULO')
    plt.plot(tt,anal(tt,*init), label='ANALE')
    plt.plot(tt, anal(tt, *popt), label='ANALE CHE VORREMMO FITTARE')
    plt.legend()
    plt.show()