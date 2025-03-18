import numpy as np
f1=493.3 #f-
sf1=0.2
f2=860.6#f+
sf2=0.5
f0=653.1 #resonance freq
sf0=0.5

df=f2-f1
sdf=np.sqrt(sf2**2+sf1**2)

Qf=np.sqrt(3)*f0/df
sQf=np.sqrt(3*(sf0/df)**2+3*(sdf*f0/df**2)**2)

ff=f1*f2#f+f-
sff=np.sqrt((sf1*f2)**2+(sf2*f1)**2)


print("df",df,"+-",sdf)
print("Qf",Qf,"+-",sQf)
print("ff",ff,"+-",sff)


##Attended

R=671
sR=7
r=40.1
sr=0.7
ffatt=f0**2
sffatt=2*f0*sf0

dfatt=(np.sqrt(3)/(np.pi*2))*(r+R)/0.5


print("fatt",ffatt,"+-",sffatt)
print("dfatt",dfatt)
