import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


Directory='/home/studentelab2/doppi_fra/29_10_2024/data_ard/' # <<<<<< now looking at a file in the datifit directory
NomeFile = 'data8.txt'   # <<<<<< now looking at a file called data00.txt
Filename=(Directory+NomeFile)
# data load
t,V=pylab.loadtxt(Filename,unpack=True)  # <<<<< the file is assumed to have 4 columns

# scatter plot with error bars
count,bin,bars=plt.hist(V, bins=int(4096/16))
# bellurie
plt.rc('font',size=16)
plt.xlabel('V_dig  [digit]',fontsize=18)
plt.ylabel('counts',fontsize=18)
plt.minorticks_on()

levels=4096
probability= count/len(V)
# AT THE FIRST STEP (data plot only) YOU MUST COMMENT FROM HERE TO THE LAST LINE (pylab.show())


# make the array with initial values (to be carefully adjusted!)
init=(2225,10)

# set the error (to be modified if effective errors have to be accounted for)
# sigma=Dy
# w=1/sigma**2

# define the model function (a straight line in this example)
# note how parameters are entered
# note the syntax
def ff(x,mu,sigma):
    p=(1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return p
#
b=bin[1:]
pars, covm = curve_fit(ff, bin[1:], probability, init, absolute_sigma=True)
xx = np.linspace(min(b), max(b), num=5000)
plt.figure(2)
#plt.plot(bin[1:], probability)
plt.plot(xx, 8192*ff(xx, *pars))
plt.xlabel("$V_{dig}$[digits]")
plt.ylabel("Occorrenze")
count,bin,bars=plt.hist(V, bins=int(4096/16))

plt.show()
