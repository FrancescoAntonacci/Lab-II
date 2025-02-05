RD = 363
VG=104e-3
vd=5.84e-3
etav = 52e-3
Iq=2.26e-3
s_Iq=0.03e-3
s_vd=vd*0.05
s_VG=0.003
s_RD=4
Vq=0.648
s_Vq=Vq*0.03


id = (VG - vd)/RD
rd = vd/id
rdatt=etav/Iq
s_id=((s_VG+s_vd)/(-vd+VG)+s_RD/RD)*id
s_rd=(s_vd/vd+s_id/id)*rd
Reff=(Vq/Iq)
s_Reff=(s_Vq/Vq+s_Iq/Iq)*Reff
print("Reff=",Reff,"+-",s_Reff)
print("rd=",rd,"+-",s_rd)
print("rd_att=",rdatt)
print("id=",id,"+-",s_id)

import matplotlib.pyplot as plt
import numpy as np

IQQ=[23.1,14.1,18.7,8.04,5.14,3.69,2.26]
VQQ=[0.82,0.760,0.760,0.760,0.720,0.720,0.648]

plt.figure()
plt.plot(VQQ,IQQ,'.')
plt.show()

