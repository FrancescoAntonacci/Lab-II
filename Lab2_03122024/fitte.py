import pylab
import numpy as np
from scipy.optimize import curve_fit


Directory='/home/studentelab2/doppi_fra/Lab2_03122024/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
f,sigma_f,V_i,sigma_Vi, V_out, sigma_Vout, delta_t = pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns
# scatter plot with error bars

def ff(f, ft, A):
    return (A/(np.sqrt(1+(f/ft) ** 2)))

init=(340.4, 1)

xx=pylab.logspace(pylab.log10(min(f)),pylab.log10(max(f)),num=500)
pylab.errorbar(f,V_out/V_i,sigma_Vout,sigma_f,linestyle = '', color = 'black', marker = '.')
pylab.plot(xx,ff(xx,*init))
# bellurie
pylab.rc('font',size=16)

#AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())


# make the array with initial values (to be carefully adjusted!)
# set the error (to be modified if effective errors have to be accounted for)
sigma=sigma_f
w=1/sigma**2
# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax


G=V_i/V_out

# AT THE SECOND STEP (plot of the model with initial parameters):
# YOU MUST COMMENT FROM HERE TO THE THIRD TO LAST LINE
# (AND PUT IN THAT LINE *init IN THE PLACE OF *pars)
# call the routine
pars,covm=curve_fit(ff,f,G,p0=init,sigma=sigma_Vi,absolute_sigma=True) # <<<< NOTE THE absolute_sigma option
# for _ in range(100):
#     sigma = np.sqrt(Dy**2 + (Dx ** 2) * (pars[0] * pylab.exp(-(x-pars[-1])/pars[1])) ** 2)
#     w = 1/sigma**2
#     pars,covm=curve_fit(ff,x,y,init,sigma=Dy,absolute_sigma=False)
# calculate the kappasq/home/doppi_fra/Lab2_19112024/uare for the best-fit funtion
# note the syntax for the pars array
kappa2 = (w*( (V_i/V_out)-ff(f,*pars))**2).sum()


corr = pylab.copy(covm) # create a *not* shadow copy of covm
for i in range(len(covm)):
    for j in range(len(covm)):
        corr[i, j] = covm[i,j]/(pylab.sqrt(covm[i, i] * covm[j, j]))

# determine the ndof
ndof=len(f)-len(init)
# print results on the console
print(pars)
print(pylab.sqrt(covm.diagonal()))
print(corr)
print (kappa2, ndof)


pylab.figure(2)

pylab.errorbar(f,V_out/V_i,sigma_Vout,sigma_f,linestyle = '', color = 'black', marker = '.')
pylab.plot(xx,ff(xx,*pars))


# # # AT THE6000 SECOND STEP, COMMENT UP TO HERE
# # # prepare a dummy xx array (with 500 linearly spaced points)
# xx=numpy.logspace(min(f),max(f),50000)
#
#
#
# # plot the fitting curve with either the initial or the optimised parameters
# # AT THE SECOND ST/home/doppi_fra/Lab2_19112024/EP, YOU MUST REPLACE *pars WITH *init
#
# fig, (ax1, ax2) = pylab.subplots(2)
# fig.suptitle("Grafico carica")
#
# ax1.plot(xx,ff(xx,*pars), color='red')
# #ax1.errorbar(x,y,Dy,Dx,linestyle = '', color = 'black', marker = '.')
#
# #ax2.errorbar(x, y - ff(x, *pars), marker='o', xerr=Dx, yerr=Dy)
# ax2.hlines(0, xmin=min(xx), xmax=max(xx), color='orange')
#
#
# ax1.set(xlabel=r'Time  [$\mu$s]', ylabel=r'Delta V [u.a.]')
# ax2.set(xlabel=r'Time  [$\mu$s]', ylabel=r'Delta V [u.a.]')

# show the plot
pylab.show()
