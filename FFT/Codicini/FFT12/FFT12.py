import numpy as np
import matplotlib.pyplot as plt

filepath='dataFFT12/'
filename=['dataFFT01uF','dataFFT01uFnoisy','dataFFT01uFtrans1','dataFFT01uFtrans2','dataFFT01uFtrans3', 'dataFFT01uFtrans4', 'dataFFT01uFtrans5', 'dataFFT01uFtrans6', 'dataFFT022uF','dataFFT022uFnoisy','dataFFT047uF','dataFFT047uFnoisy']
filepath_images='img/FFT12/'


for i in filename:
    t,v=np.loadtxt(filepath+i+'.txt', unpack=True)
    delta_t=t[1]-t[0]
    f_s=1/(2*delta_t)
    ff=np.linspace(0,f_s,len(t)//2+1)
    ## FFT
    v_tilde= abs(np.fft.rfft(v))
    ##

    ## Plot
    columns=1
    rows=2

    fig,axes=plt.subplots(rows,columns,figsize=(10,6.18))
    axes=axes.flatten()

    axes[0].plot(t,v)
    axes[1].plot(ff,v_tilde)

    axes[1].set_yscale('log')    
    plt.savefig(filepath_images+i+'.png')
    plt.show()

