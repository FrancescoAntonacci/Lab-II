import pylab
import numpy as np
from scipy.optimize import curve_fit


Directory='/home/studentelab2/doppi_fra/Lab2_04032025/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data047uF.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
t,Dt,V,DV=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

# scatter plot with error bars
pylab.errorbar(t,V,DV,Dt, fmt='.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel(r't  [$\mu$ s]',fontsize=18)
pylab.ylabel(r'$\Delta_V$  [arb.un]',fontsize=18)
pylab.minorticks_on()

#  AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())


# make the array with initial values (to be carefully adjusted!)
init=(1500, 15000, 3.8e-3, 1,1700)

# set the error (to be modified if effective errors have to be accounted for)
sigma=DV
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(t, A, tau, omega, phi, c):
    return A * np.exp(- t/tau) * np.cos(omega * t + phi) + c

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,t,V,init,sigma,absolute_sigma=True) # <<<< NOTE THE absolute_sigma option

# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = (w*(V-ff(t,*pars))**2).sum()

# determine the ndof
ndof=len(x)-len(init)

# print results on the console
print("Array dei parametri stimati")
print(pars)
# print("Matrice di covarianza")
# print(covm)
print("Errori parametri")
print(np.sqrt(np.diag(covm)))
print("kappa2/dof")
print(kappa2/ndof)


# # AT THE SECOND STEP, COMMENT UP TO HERE
# # prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(t),max(t),500)
#
#
#
# # plot the fitting curve with either the initial or the optimised parameters
# # AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.plot(xx,ff(xx,*pars), color='red')
#
# pylab.tight_layout() # reuired to properly adjust the plot window size

# show the plot
pylab.show()

C=0.47e-6
tau=pars[1]*1e-6
omega=pars[2]*1e6
Domega=np.sqrt(covm[2,2])*1e6

print("T=",2*np.pi/omega,"DT=",2*np.pi*Domega/omega**2)

L=1/(C*((omega**2)-(1/tau**2)))
R=2/(C*tau*((omega**2)-(1/tau**2)))
print("L=",L)
print("R=",R)
