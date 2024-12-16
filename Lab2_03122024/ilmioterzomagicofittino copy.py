import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

Directory='/media/candido/Extreme SSD/Unipi/Secondo anno/Lab 2/Lab2_03122024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data3.txt'   # <<<<<< now looking at a file called data00.txt
NomeFile1='data2.txt'

Filename=(Directory+NomeFile)
# data load
f,sigma_f,V_out, banda = np.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

V_in=np.full_like(V_out,4)
sigma_Vin=V_in/333
sigma_Vout=V_out/333

plt.rc('font',size=16)
plt.xlabel('f [Hz]',fontsize=18)
plt.ylabel('G[dB]',fontsize=18)
plt.minorticks_on()



init=(340.4, 1)


sigma=sigma_Vout/np.sqrt(3)
w=1/sigma**2




def ff(f, ft, A):
    return (A/(np.sqrt(1 + (f/ft) ** 2)))




pars,covm=curve_fit(ff,f,V_out/V_in,init,sigma,absolute_sigma=True) # <<<< NOTE THE absolute_sigma option



kappa2 = ((w*( (V_out/V_in) -ff(f,*pars))**2)).sum()



ndof=len(f)-len(init)


print("Parametri di bestfit stimati dal fit")
print(pars)
print("Errori")
print(np.sqrt(np.diag(covm)))
print("Matrice di covarianza")
print(covm)
print("kappa2:")
print(kappa2, ndof)
corr = np.copy(covm) # create a *not* shadow copy of covm
for i in range(len(covm)):
    for j in range(len(covm)):
        corr[i, j] = covm[i,j]/(np.sqrt(covm[i, i] * covm[j, j]))
print("Matrice di correlazione")
print(corr)
"""# show the plot
plt.show()
# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
plt.xscale('log')
plt.yscale('log')
plt.plot(xx,ff(xx,*pars), color='red')
plt.grid()
"""



##


xx=np.logspace( np.log10(min(f)) , np.log10(max(f)),num=500)

x_bode=np.log10(xx)
y_bode=20*np.log10(ff(xx,*init))


def line(x,m,q):
    return m*x+q

plt.figure(1)


retta1,_=curve_fit(line,x_bode[:5],y_bode[:5])
retta2,_=curve_fit(line,x_bode[-5:],y_bode[-5:])
A=np.array([[-retta1[0],1],[-retta2[0],1]])
B=np.array([retta1[1],retta2[1]])
retta3=np.linalg.solve(A,B)
print(retta3)

yy=np.linspace(min(y_bode),max(y_bode),1000)
xx=np.full_like(yy,10**retta3[0])

plt.plot(10**x_bode,y_bode,label="Best fit")
plt.plot(10**x_bode,line(x_bode,*retta1),label="Asinto sinistro")
plt.plot(10**x_bode,line(x_bode,*retta2),label="Asinto destro")
plt.errorbar(f,20*np.log10(V_out/V_in),sigma_Vin,sigma_f,linestyle = '', color = 'black', marker = '.')
plt.xscale('log')
plt.plot(xx,yy)
plt.grid()
plt.legend()


# show the plot
plt.show()





