import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

filepath='dataFFT5/'

#data 0 is a non plugged arduino        'data0',
#data 1,2,3 sin tr, sq                  'data1','data2','data3',
#data 4,5,6 same but with duty cycle    'data4','data5','data6',
#data 14 15 are long acquisitions       'data14','data15'
#data 13 is a very short acquisition    'data12','data13'
#the rest is badly taken data           'data7','data8','data9','data10','data11'

## I'm trying a reckless fit
def model(x, a,dx, tau,c):
    return a*np.exp(-(x+dx)/tau)+c


filename=['data0','data7','data13']
filepath_images='img/FFT5/'

# Create a figure with subplots
fig, axes = plt.subplots(len(filename), 2, figsize=(16, 10))

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
    sf_fft=df/(np.sqrt(12))


    if i == 'data0':
        p0=[3000,0,1,500]
        popt,pcov=curve_fit(model,t[:200],v[:200],p0=p0)
        axes[idx,0].plot(t,model(t,*popt),label='Fit con legge esponenziale')
        print('pars=',popt,'spars=',np.sqrt(np.diag(pcov)))
        res=v[:200]-model(t[:200],*popt)
        x2=np.sum((res)**2/1e2)
        print('x2=',x2)




    # Reference lines
    yy = np.linspace(min(v_tilde), max(v_tilde), 4000)
    vv = np.linspace(min(v), max(v), 4000)
    
    # Plot time-domain signal
    axes[idx, 0].plot(t, v, label='Vc(t)')
    axes[idx, 0].grid()
    axes[idx, 0].legend()
    
    # Plot frequency-domain (FFT)
    # Reference lines

    # Shaded regions for uncertainties

    # Plot frequency-domain (FFT)
    axes[idx, 1].plot(ff, v_tilde, label='ADS dell\'FFT')
    if i == 'data13':
        fff=np.linspace(min(ff),max(ff),4000)
        axes[idx,1].plot(fff,5e1/fff,label='1/x')    


    axes[idx, 1].set_yscale('log')
    axes[idx, 1].grid()
    axes[idx, 1].minorticks_on()
    axes[idx, 1].legend(loc='upper right')



# Add common labels
fig.text(0.74, 0.90, 'FFT', ha='center', fontsize=18)
fig.text(0.34, 0.90, 'Segnale', ha='center', fontsize=18)

fig.text(0.34, 0.04, 't [ms]', ha='center', fontsize=18)
fig.text(0.74, 0.04, 'f [kHz]', ha='center', fontsize=18)

fig.text(0.04, 0.5, 'Vc(t)[arb. units]', va='center', rotation='vertical', fontsize=18)
fig.text(0.5, 0.5, 'ADS [arb. units]', va='center', rotation='vertical', fontsize=18)

fig.text(0.91, 0.80, 'Arduino Scollegato', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.50, 'Sovracampionamento', va='center', rotation='vertical', fontsize=18)
fig.text(0.91, 0.20, 'Sottocampionamento', va='center', rotation='vertical', fontsize=18)

# Show all plots in a single figure
plt.savefig(filepath_images + 'FFTwaveforms4.png')
plt.show()
