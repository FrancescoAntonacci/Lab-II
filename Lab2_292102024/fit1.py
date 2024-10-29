import pylab
import numpy
from scipy.optimize import curve_fit


Directory='/home/studentelab2/doppi_fra/29_10_2024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'misure_voltaggi.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
V_d,sigma_V_d,V_v, sigma_V_v=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

# scatter plot with error bars
pylab.errorbar(V_d,V_v,sigma_V_v,sigma_V_d,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel(r'$V_{dig}$ [digit]',fontsize=18)
pylab.ylabel(r'$V_v$ [V]',fontsize=18)
pylab.minorticks_on()

# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())


# make the array with initial values (to be carefully adjusted!)
init=(0, 5e-4,0)

# set the error (to be modified if elineective errors have to be accounted for)
sigma=sigma_V_v
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def parabola(x, a, b, c):
    return a*x**2 + b*x + c

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(parabola,V_d,V_v,init,sigma,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option
pars_h = pylab.copy(pars)
covm_h = pylab.copy(covm)
corr_h = pylab.copy(covm) # create a *not* shadow copy of covm
corr_h = covm / np.outer(np.sqrt(np.diag(covm)), np.sqrt(np.diag(covm)))
# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = (w*(V_v-parabola(V_d,*pars))**2).sum()

# determine the ndof
ndof=len(V_d)-len(init)

# print results on the console


##
print("\n\nFIT SENZA ERRORI EFFICACI")
print(f"Parametri di best fit {pars}")
print("Errori sui parametri di best-fit",np.sqrt(np.diag(covm)))
print("Matrice di covarianza:\n",covm)
print ("k2  ndof",kappa2, ndof)
print(f"Matrice di correlazione \n {corr_h}")


# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(V_d),max(V_d),5000)


for i in range(100):
    sigma=np.sqrt((2 * pars[0]* V_d * sigma_V_d + pars[1] * sigma_V_d)**2+(sigma_V_v)**2)
    pars,covm=curve_fit(parabola,V_d,V_v,init,sigma,absolute_sigma=False)

pars1=pylab.copy(pars)
covm1=pylab.copy(covm)

w=1/sigma**2
kappa2 = (w*(V_v-parabola(V_d,*pars1))**2).sum()


corr1= pylab.copy(covm1)
corr1 = covm1 / np.outer(np.sqrt(np.diag(covm1)), np.sqrt(np.diag(covm1)))
##
print("\n\nFIT CON ERRORI EFFICACI")
print(f"Parametri di best fit {pars1}")
print("Errori sui parametri di best-fit",np.sqrt(np.diag(covm1)))
print("Matrice di covarianza:\n",covm1)
print ("k2  ndof",kappa2, ndof)
print(f"Matrice di correlazione \n {corr1}")


# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.plot(xx,parabola(xx,*pars), color='red',label="Fit")
pylab.plot(xx,parabola(xx,*pars1),color='black',label="Fit con errori efficaci")




pylab.legend()

pylab.tight_layout() # reuired to properly adjust the plot window size

# show the plot
pylab.show()
