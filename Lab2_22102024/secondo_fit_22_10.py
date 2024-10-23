import pylab
import numpy
from scipy.optimize import curve_fit


V_0 = 4.95
sigma_V = 0.03
R_a = 6.73e3
sigma_R_a = 0.06e3
R_b = 723
sigma_R_b = 6
V_out = V_0 * (R_a/(R_a + R_b))
sigma_V_out = ((sigma_V/V_0) + (sigma_R_a/R_a) + (sigma_R_b/R_b)) * V_0
R_th = (R_a * R_b)/(R_a + R_b)
sigma_R_th = R_th * (2 * (sigma_R_a/R_a) + (sigma_R_b/R_b))
print(f"R_th = {R_th} +- {sigma_R_th}")
print(f"V_out = {V_out} +- {sigma_V_out}")
Directory='/home/studentelab2/doppi_fra/' # <<<<<< now looking at a file in the datifit directory

##
NomeFile = 'dati22_10_1.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load

x,Dx,y,Dy=pylab.loadtxt(Filename,unpack=True,skiprows=3)  # <<<<< the file is assumed to have 4 columns
x = x[:11]
Dx = Dx[:11]
y = y[:11]
Dy = Dy[:11]
# scatter plot with error bars
pylab.errorbar(x,y, xerr=Dx,yerr=Dy,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)
pylab.xlabel('$R_j$  [$\Omega$]',fontsize=18)
pylab.ylabel('I  [A]',fontsize=18)
pylab.minorticks_on()
pylab.xscale("log")
pylab.yscale("log")
# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())



# make the array with initial values (to be carefully adjusted!)
init=(0,0,0)

# set the error (to be modified if effective errors have to be accounted for)
sigma=Dy
w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(x, V_th,R_th, b):
    return ((V_th/(R_th+x)) + b)


# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,x,y,init,sigma,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option
for i in range(100):
    sigma= pylab.sqrt(Dy**2 + (pars[0]*(1/(x + pars[1])**2) * Dx)**2)
    w=1/sigma**2
    pars,covm=curve_fit(ff,x,y,init,sigma,absolute_sigma=False)

corr = pylab.copy(covm) # create a *not* shadow copy of covm
for i in range(len(covm)):
    for j in range(len(covm)):
        corr[i, j] = covm[i,j]/(pylab.sqrt(covm[i, i] * covm[j, j]))


# calculate the kappasquare for the best-fit funtion
# note the syntax for the pars array
kappa2 = ((w*(y-ff(x,*pars))**2)).sum()

# determine the ndof
ndof=len(x)-len(init)

# print results on the console
print(f"Parametri best-fit: {pars}")
print(f"Matrice di correlazione: \n")
print(corr)
print (f"k quadro: {kappa2}, con gradi di libertà {ndof}, dunque k2 normalizzato {kappa2/ndof}")

# AT THE SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(x),max(x),5000000)

# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND STEP, YOU MUST REPLACE *pars WITH *init
pylab.plot(xx,ff(xx,*pars), color='red')



# show the plot
pylab.show()
