import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filepath='dataFFT5/'

#data 0 is a non plugged arduino        'data0',
#data 1,2,3 sin tr, sq                  'data1','data2','data3',
#data 4,5,6 same but with duty cycle    'data4','data5','data6',
#data 14 15 are long acquisitions       'data14','data15'
#data 13 is a very short acquisition    'data13',
#the rest is badly taken data           'data7','data8','data9','data10','data11','data12',


filename=['data1','data2','data3']
filepath_images='img/FFT5/'
f = np.array([177.455,178.0571,178.0571])*1e-3 #Just data1,2,3; converting to kHz 
sf = np.array([0.002,0.0009,0.0009])*1e-3#Just data1,2,3 ;converting to kHz


# Create a figure with subplots
fig, axes = plt.subplots(len(filename), 2, figsize=(16, 10), sharex='col', sharey='col')

for idx, i in enumerate(filename):
    # Load data
    t, v = np.loadtxt(filepath + i + '.txt', unpack=True)
    t = t / 1000  # Convert to ms
    
    # Compute sampling parameters
    numpoints = len(t)  # Number of points
    df = 1 / (2 * max(t))
    ff = np.linspace(0, df*numpoints, numpoints//2 + 1)
    

    # Compute FFT
    v_tilde = abs(np.fft.rfft(v))


    k=np.argmax(v_tilde[1:])+1
    f_fft=ff[k]
    sf_fft=df/(len(ff)*np.sqrt(12))

    print("f0_fft=",f_fft,"+-",sf_fft)
    print("f0_bestfit=",f[idx],"+-",sf[idx])
    print()
    
    # Reference lines
    yy = np.linspace(min(v_tilde), max(v_tilde), 4000)
    xx = np.full_like(yy, f[idx])
    vv = np.linspace(min(v), max(v), 4000)
    
    # Plot time-domain signal
    axes[idx, 0].plot(t, v, label='Vc(t)')
    axes[idx, 0].grid()
    axes[idx, 0].legend()
    
    # Plot frequency-domain (FFT)
    # Reference lines

    # Shaded regions for uncertainties
    axes[idx, 1].fill_betweenx(yy, f[idx] - sf[idx], f[idx] + sf[idx], color='r', alpha=0.3)

    # Plot frequency-domain (FFT)
    axes[idx, 1].plot(ff, v_tilde, label='ADS dell\'FFT')
    axes[idx, 1].plot(xx, yy, 'r--', label='f0 best-fit')


    if i=='data1':
            xxx=np.full_like(yy,0.35)
            axes[idx, 1].plot(xxx, yy,'g--', label="rumore?")

    if i=='data3' or i=='data2':
        axes[idx, 1].plot(xx*2, yy,'g--', label="armoniche successive")
        for j in range(2,20):
                axes[idx, 1].plot(xx*j, yy, 'g--')

    if i=='data2':
        yy_data2=1e-1*(max(v)/(np.pi*ff))**2
        axes[idx, 1].plot(ff,yy_data2 , 'k--',label='andamento delle armoniche')


    if i=='data3':
        yy_data3=1e3*max(v)/(np.pi*ff)
        axes[idx, 1].plot(ff,yy_data3 , 'k--',label='andamento delle armoniche')


        

    axes[idx, 1].set_yscale('log')
    axes[idx, 1].set_xlim(-0.1, 10 * f[idx])
    axes[idx, 1].grid()
    axes[idx, 1].minorticks_on()
    axes[idx, 1].legend(loc='upper right')



# Add common labels
fig.text(0.74, 0.96, 'Trasformata di Fourier', ha='center', fontsize=18)
fig.text(0.34, 0.96, 'Segnale', ha='center', fontsize=18)

fig.text(0.34, 0.04, 't [ms]', ha='center', fontsize=18)
fig.text(0.74, 0.04, 'f [kHz]', ha='center', fontsize=18)

fig.text(0.04, 0.5, 'Vc(t)[arb. units]', va='center', rotation='vertical', fontsize=18)
fig.text(0.5, 0.5, 'ADS [arb. units]', va='center', rotation='vertical', fontsize=18)

fig.text(0.91, 0.22, 'Onda sinusoidale', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.5, 'Onda triangolare', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.77, 'Onda quadra', va='center', rotation='vertical', fontsize=18)

# Show all plots in a single figure
plt.savefig(filepath_images + 'FFTwaveforms.png')
plt.show()
