import numpy as np
import matplotlib.pyplot as plt

filepath='dataFFT5/'
filename=['data0','data1','data2','data3','data4','data5','data6','data7','data8','data9','data10','data11','data12','data13','data14','data15']
filepath_images='img/FFT5/'


for i in filename:
    data=np.loadtxt(filepath+i+'.txt', unpack=True)
    t=data[0]
    v=data[1]
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

