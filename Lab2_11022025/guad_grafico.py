import matplotlib.pyplot as plt
import numpy as np
##Data
filename = "/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Lab2_11022025/data8"
f,sf,vin,svin, vout,svout = np.loadtxt(filename, unpack=True)
Re=328
sRe=5
Rc=991
sRc=9
Rb=560
sRb=5
Ce=4.7e-6
sCe=Ce*0.2
etaVt=30e-3
##Calculating gain
G = vout/vin
sG = [(svin/vin) + (svout/vout)]*G
##
def Gatt(f,bf,rb):
    #(Rc/(Rb+etaVt/I))*(Re/(1+(Re*2*np.pi*f*Ce)**2))
    return (bf+1)*Re/(Rb+rb+)
##p0
p0=(22e-6)
##Best fit


##plot
xx=np.linspace(min(f),max(f),1000)
plt.figure(1)
plt.errorbar(f, G,sG,sf,fmt='o',label='G(f)')
plt.plot(f,Gatt(f,p0),label='Modello teorico')
plt.xlabel('f [Hz]')
plt.ylabel('G(f)')
plt.legend()
plt.grid()
plt.show()
