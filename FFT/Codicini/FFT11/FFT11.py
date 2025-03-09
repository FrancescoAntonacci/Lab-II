import numpy as np
import matplotlib.pyplot as plt

filepath='dataFFT11/'
filename=['data_6_88','data_7_08','data_7_48','data_8_06','data_9_01','data_9_77','data_9_92','data_11_11','data_12_97','data_13_02','data_13_77','data_15_06','data_17_04']
filepath_images='img/FFT11/'


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

