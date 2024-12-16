import pylab
import numpy
from scipy.optimize import curve_fit

Directory='/home/candido/Scrivania/Unipi/Secondo anno/Lab 2/Lab2_01302024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data01.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
x,Dx,y,Dy=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

# scatter plot with error bars
pylab.errorbar(x,y,Dy,Dx,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel('$\Delta$V  [V]',fontsize=18)
pylab.ylabel('I  [mA]',fontsize=18)
pylab.minorticks_on()

# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())

# make the array with initial values (to be carefully adjusted!)
init=(0.0015,0.0019)

# set the error (to be modified if effective errors have to be accounted for)
# sigma=Dy non fixed errors
w=1/Dy**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(x, a, b):
    return a*x+b

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,x,y,init,Dy,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option

sigma=pylab.sqrt(Dy**2 + (Dx * pars[0])**2) # fixed errors

pars,covm=curve_fit(ff,x,y,init,sigma,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option

w=1/sigma**2
# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = ((w*(y-ff(x,*pars))**2)).sum()

# determine the ndof
ndof=len(x)-len(init)

# print results on the console
print(pars)
print(covm)
print(f"Uncertainties: {pylab.sqrt(covm.diagonal())}")
print (kappa2, ndof)

##
ratio=max(Dy/(Dx*pars[0])) # controllo se gli errori sono trascurabili
# print(ratio)
##
corr = pylab.copy(covm)

for i in range(len(covm)):
    for j in range(len(covm)):
        corr[i,j]= covm[i,j]/pylab.sqrt(covm[i,i]*covm[j,j])

print("Correlation matrix:\n",corr)
# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(x),max(x),500)

## plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.figure(1)
pylab.plot(xx,ff(xx,*pars), color='red')

##Plot of the residuals
norm_res=(y-pars[0]*x-pars[1])/pylab.sqrt(Dy**2+(Dx*pars[0])**2)

pylab.figure(2)
pylab.errorbar(x,norm_res, color="red", fmt='.')

##

# show the plot
pylab.show()

## Extrapolation of the value of the current
delta_v = 20
extr_i = pars[0] * delta_v + pars[1]
a=(delta_v ** 2) * covm[0, 0]
b=covm[1, 1]
c=2 * delta_v * covm[0, 1]
print(a,b,c)
sigma_i = pylab.sqrt(a + b - c)
print(f"Intensità di corrente elettrica estrapolata: {extr_i} +- {sigma_i}")