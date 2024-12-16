import pylab
import numpy
from scipy.optimize import curve_fit


Directory='/home/studentelab2/datifit/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'RC.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
x,Dx,y,Dy=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

x  = x[:400]
Dx = Dx[:400]
y = y[:400]
Dy = Dy[:400]
# scatter plot with error bars
pylab.errorbar(x,y,Dy,Dx,fmt=".")

# bellurie
pylab.rc('font',size=16)
pylab.xlabel('$t$ [s]',fontsize=18)
pylab.ylabel('$\Delta $V  [mV]',fontsize=18)
pylab.minorticks_on()

# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())
# make the array with initial values (to be carefully adjusted!)
init=(4000,0.0005,0,0)

# set the error (to be modified if effective errors have to be accounted for)
sigma=Dy
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(x, a, b, a0, t0):
    return a * (1-pylab.exp(-b * (x-t0)))+a0

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,x,y,init,sigma,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option

# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = ((w*(y-ff(x,*pars))**2)).sum()

# determine the ndof
ndof=len(x)-len(init)

# print results on the console
print(pars)
print(covm)
print (kappa2, ndof)


# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(x),max(x),500)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.plot(xx,ff(xx,*pars), color='red')


# show the plot
pylab.show()
