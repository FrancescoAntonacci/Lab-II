import numpy as np
import matplotlib.pyplot as plt

filepath='dataFFT12/'
filename=['dataFFT01uF']
filepath_images='img/FFT12/'


plt.rcParams.update({"font.size": 18})

C=1e-7
sC=C*0.2
R=40.1# Direct measurement
sR=0.5

Rfit=100
sRfit=10

Lfit=0.7
sLfit=0.07

Tfit=1.6663
sTfit=0.0007

taufit=13.96e-3
staufit=0.02e-3

f=1/Tfit#kHz
sf=1*sTfit/Tfit**2 #kHz

print(f,sf)
for i in filename:
    t,v=np.loadtxt(filepath+i+'.txt', unpack=True)
    t=t/1000 #ms
    
    delta_t=np.mean(np.diff(t)) #delta_t must be calculated sa a mean for it is a aleatory variable
    f_s=1/(2*delta_t)
    ff=np.linspace(0,f_s,len(t)//2+1)
    ## FFT
    v_tilde= abs(np.fft.rfft(v))
    ##

    ## Plot
    columns=1
    rows=2

    fig,axes=plt.subplots(rows,columns,figsize=(10,10))
    axes=axes.flatten()

    yy=np.linspace(min(v_tilde),max(v_tilde),4000)
    xx=np.full_like(yy,f)

    vv=np.linspace(min(v),max(v),4000)
    TT=np.full_like(vv,Tfit)


    axes[0].plot(t,v)
    axes[0].plot(TT,vv,'r--')
    axes[1].plot(ff,v_tilde)
    axes[1].plot(xx,yy,'r--')

    axes[0].set_xlabel('t [ms]')
    axes[0].set_ylabel('Vc(t) [arb.un.]')
    axes[1].set_xlabel('f[kHz]')
    axes[1].set_ylabel('ADS [arb.un.]')
    axes[1].set_yscale('log')   


    axes[1].set_xlim(-0.1,3*f)

    axes[0].grid()
    axes[1].grid()
    axes[1].minorticks_on()
    
    plt.savefig(filepath_images+i+'.png')



plt.show()

