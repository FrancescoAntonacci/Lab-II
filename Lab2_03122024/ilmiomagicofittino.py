import pylab
import numpy as np
from scipy.optimize import curve_fit

Directory='/home/studentelab2/doppi_fra/Lab2_03122024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
f,sigma_f,V_i,sigma_Vi, V_out, sigma_Vout, delta_t = pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns
# scatter plot with error bars
"""
# scatter plot with error bars
pylab.errorbar(f,V_out/V_i,sigma_Vi,sigma_f,linestyle = '', color = 'black', marker = '.')
"""
# bellurie
pylab.rc('font',size=16)
pylab.xlabel('f [Hz]',fontsize=18)
pylab.ylabel('G[dB]',fontsize=18)
pylab.minorticks_on()

# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())

# make the array with initial values (to be carefully adjusted!)
init=(340.4, 1)

# set the error (to be modified if effective errors have to be accounted for)
sigma=sigma_Vi/pylab.sqrt(3)
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax10
def ff(f, ft, A):
    return (A/(pylab.sqrt(1 + (f/ft) ** 2)))

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,f,V_out/V_i,init,sigma,absolute_sigma=True) # <<<< NOTE THE absolute_sigma option

# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = ((w*( (V_out/V_i) -ff(f,*pars))**2)).sum()

# determine the ndof
ndof=len(f)-len(init)

# print results on the console
print("Parametri di bestfit stimati dal fit")
print(pars)
print("Errori")
print(np.sqrt(np.diag(covm)))
print("Matrice di covarianza")
print(covm)
print("kappa2:")
print(kappa2, ndof)
corr = pylab.copy(covm) # create a *not* shadow copy of covm
for i in range(len(covm)):
    for j in range(len(covm)):
        corr[i, j] = covm[i,j]/(pylab.sqrt(covm[i, i] * covm[j, j]))
print("Matrice di correlazione")
print(corr)
"""# show the plot
pylab.show()
# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.logspace( pylab.log10(min(f)) , pylab.log10(max(f)),num=500)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.xscale('log')
pylab.yscale('log')
pylab.plot(xx,ff(xx,*pars), color='red')
pylab.grid()
"""



##

x_bode=np.log10(xx)
y_bode=20*np.log10(ff(xx,*init))
# show the plot
pylab.show()

def line(x,m,q):
    return m*x+q

pylab.figure(1)


retta1,_=curve_fit(line,x_bode[:5],y_bode[:5])
retta2,_=curve_fit(line,x_bode[-5:],y_bode[-5:])

pylab.plot(10**x_bode,y_bode,label="Best fit")
pylab.p
pylab.plot(10**x_bode,line(x_bode,*retta1),label="Asinto sinistro")
pylab.plot(10**x_bode,line(x_bode,*retta2),label="Asinto destro")
pylab.errorbar(f,V_out/V_i,sigma_Vi,sigma_f,linestyle = '', color = 'black', marker = '.')
pylab.xscale('log')

pylab.grid()
pylab.legend()


# show the plot
pylab.show()