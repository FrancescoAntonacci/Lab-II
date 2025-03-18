import pylab
import numpy as np
from scipy.optimize import curve_fit

Directory='/home/studentelab2/doppi_fra/Lab2_18032025/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data_guad.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
f,sf,vout,vin=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

svout=0.03*vout
svin=0.03*vin

G= vout/vin
sG=np.sqrt((svout/vin)**2+(svin*vout/vin**2)**2)

# scatter plot with error bars
pylab.errorbar(f,G,sG,sf,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel('$f$  [Hz]',fontsize=18)
pylab.ylabel('G',fontsize=18)
pylab.minorticks_on()

# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())

# make the array with initial values (to be carefully adjusted!)
init=(653, 2 * np.pi * 671e-7, 2 * np.pi*760e-7)

# set the error (to be modified if effective errors have to be accounted for)
sigma=sG
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(f,f0,RC,RtC):
    n=RC*f
    d=np.sqrt((1-(f/f0)**2)**2+(f*RtC)**2)
    return n/d



# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,f,G,p0=init,sigma=sG,absolute_sigma=True) # <<<< NOTE THE absolute_sigma option

res = G - ff(f, *pars)
# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = ((w*(G-ff(f,*pars))**2)).sum()

# determine the ndof
ndof=len(f)-len(init)

# print results on the console
print("I parametri di best-fit sono i seguenti: ")
print(pars)
print("Gli errori sui parametri di best-fit sono: ")
print(np.sqrt(covm.diagonal()))
print (kappa2/ndof, ndof)
corr=np.copy(covm)
for i in range(len(pars)):
    for j in range(len(pars)):
        corr[i, j] = covm[i, j]/np.sqrt(covm[i, i] * covm[j, j])


# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)

xx=np.linspace(min(f),max(f),2000)

pylab.figure(1)
# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.plot(xx, ff(xx, *init), color='green', label='Guessed curve')
pylab.title("Grafico di best-fit")
pylab.plot(xx,ff(xx,*pars), color='red', label='Best-fit curve')
pylab.legend()
pylab.show()

pylab.figure(2)
pylab.rc('font',size=16)
pylab.xlabel('$f$  [Hz]',fontsize=18)
pylab.ylabel('G',fontsize=18)np.s
pylab.minorticks_on()
pylab.title("Residui normalizzati")
pylab.axhline(y=0, color='black')
pylab.errorbar(f, res/sG,linestyle='', marker='.', color='blue')
# show the plot
pylab.show()
