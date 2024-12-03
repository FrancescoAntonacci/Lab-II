import pylab
import numpy
from scipy.optimize import curve_fit

Directory='/home/studentelab2/doppi_fra/Lab2_03122024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
f,sigma_f,V_i,sigma_Vi, V_out, sigma_Vout, delta_t = pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns
# scatter plot with error bars

# scatter plot with error bars
pylab.errorbar(f,V_out/V_i,sigma_Vi,sigma_f,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel('f [Hz]',fontsize=18)
pylab.ylabel('G',fontsize=18)
pylab.minorticks_on()

# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())

# make the array with initial values (to be carefully adjusted!)
init=(340.4, 1)

# set the error (to be modified if effective errors have to be accounted for)
sigma=sigma_Vi/pylab.sqrt(3)
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
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

# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.logspace( pylab.log10(min(f)) , pylab.log10(max(f)),num=500)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.xscale('log')
pylab.yscale('log')
pylab.plot(xx,ff(xx,*pars), color='red')
pylab.grid()

# show the plot
pylab.show()

### Fit con una retta usando i primi tre punti
def line(f, m, q):
    return m * f + q

G = V_out/V_i
_init = (-1, -10000)
pars1,covm=curve_fit(line,f[:3],pylab.log10(G[:3]),_init,sigma[:3],absolute_sigma=True)
kappa2 = ((w[:3]*( G[:3] -line(f[:3],*pars1))**2)).sum()

# determine the ndof
ndof=len(f[:3])-len(_init)

# print results on the console
print("Parametri di bestfit stimati dal fit")
print(pars1)
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
# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.logspace( pylab.log10(min(f[:3])) , pylab.log10(max(f[:3])),num=500)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.figure(2)
pylab.errorbar(f[:3],G[:3],sigma_Vi[:3],sigma_f[:3],linestyle = '', color = 'black', marker = '.')
pylab.plot(xx,line(xx,*pars1), color='red')
pylab.grid()

# show the plot
pylab.show()

### Fit con una retta usando gli ultimi tre punti
_init = (-1, -10000)
pars2,covm=curve_fit(line,f[-3:],pylab.log10(G[-3:]),_init,sigma[-3:],absolute_sigma=True)
kappa2 = ((w[-3:]*( G[-3:] -line(f[-3:],*pars))**2)).sum()

# determine the ndof
ndof=len(f[-3:])-len(_init)

# print results on the console
print("Parametri di bestfit stimati dal fit")
print(pars2)
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
# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.logspace( pylab.log10(min(f[-3:])) , pylab.log10(max(f[-3:])),num=500)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.figure(3)
pylab.errorbar(f[-3:],G[-3:],sigma_Vi[-3:],sigma_f[-3:],linestyle = '', color = 'black', marker = '.')
pylab.plot(xx,line(xx,*pars2), color='red')
pylab.grid()

# show the plot
pylab.figure(4)
xx=numpy.logspace( pylab.log10(min(f)) , pylab.log10(max(f)),num=500)
pylab.errorbar(f[:3], G[:3], sigma_Vi[:3], sigma_f[:3], linestyle='', color='purple', marker='.')
pylab.errorbar(f[-3:], G[-3:], sigma_Vi[-3:], sigma_f[-3:], linestyle='', color='purple', marker='.')
pylab.plot(xx, line(xx, *pars1))
pylab.plot(xx, line(xx, *pars2))
pylab.show()


