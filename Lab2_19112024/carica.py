import pylab
import numpy
from scipy.optimize import curve_fit


Directory='/home/studentelab2/doppi_fra/Lab2_19112024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data_carica.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
x,Dx,y,Dy=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns
x=x[:400]
Dx=Dx[:400]
y=y[:400]
Dy=Dy[:400]

# scatter plot with error bars
# pylab.errorbar(x,y,Dy,Dx,linestyle = '', color = 'black', marker = '.')

# bellurie
pylab.rc('font',size=16)

#AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())


# make the array with initial values (to be carefully adjusted!)
init=(2900,868,537, min(x))

# set the error (to be modified if effective errors have to be accounted for)
sigma=Dy
w=1/sigma**2
# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(t, V, tau,V0, t0):
    return V*(1-pylab.exp(-(t-t0)/tau))+V0



# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,x,y,init,sigma=Dy,absolute_sigma=False) # <<<< NOTE THE absolute_sigma option
for _ in range(100):
    sigma = np.sqrt(Dy**2 + (Dx ** 2) * (pars[0] * pylab.exp(-(x-pars[-1])/pars[1])) ** 2)
    w = 1/sigma**2
    pars,covm=curve_fit(ff,x,y,init,sigma=Dy,absolute_sigma=False)
# calculate the kappasq/home/doppi_fra/Lab2_19112024/uare for the best-fit funtion
# note the syntax for the pars array
kappa2 = (w*(y-ff(x,*pars))**2).sum()


corr = pylab.copy(covm) # create a *not* shadow copy of covm
for i in range(len(covm)):
    for j in range(len(covm)):
        corr[i, j] = covm[i,j]/(pylab.sqrt(covm[i, i] * covm[j, j]))

# determine the ndof
ndof=len(x)-len(init)
# print results on the console
print(pars)
print(pylab.sqrt(covm.diagonal()))
print(corr)
print (kappa2, ndof)


# AT THE6000 SECOND STEP, COMMENT UP TO HERE
# prepare a dummy xx array (with 500 linearly spaced points)
xx=numpy.linspace(min(x),max(x),500)



# plot the fitting curve with either the initial or the optimised parameters
# AT THE SECOND ST/home/doppi_fra/Lab2_19112024/EP, YOU MUST REPLACE *pars WITH *init

fig, (ax1, ax2) = pylab.subplots(2)
fig.suptitle("Grafico carica")

ax1.plot(xx,ff(xx,*pars), color='red')
ax1.errorbar(x,y,Dy,Dx,linestyle = '', color = 'black', marker = '.')

ax2.errorbar(x, y - ff(x, *pars), marker='o', xerr=Dx, yerr=Dy)
ax2.hlines(0, xmin=min(xx), xmax=max(xx), color='orange')


ax1.set(xlabel=r'Time  [$\mu$s]', ylabel=r'Delta V [u.a.]')
ax2.set(xlabel=r'Time  [$\mu$s]', ylabel=r'Delta V [u.a.]')

# show the plot
pylab.show()
