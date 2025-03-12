import numpy as np
h=0.5
r=+ 50
c=0.1e-6

tau=2*h/r
omega=np.sqrt(-(tau)**(-2) + (c * h)**(-1))

dphi = np.pi/2 - np.arctan(1/(omega*tau))
print(dphi)

print(omega)
print( tau)