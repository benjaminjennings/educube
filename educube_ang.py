import numpy as np 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Low ambient conditions.

angs = np.arange(0,360,45)

angs_educube = np.array([0,49,90,132,180,220,271,335])

def line(x,m,c):

	return m*x + c

fit = curve_fit(line,angs,angs_educube)

fig = plt.figure(figsize=(12,8))

plt.title('EduCube Light-sensor Angle vs. Measured Angle (Low Ambient)',fontsize=20)
plt.plot(angs,angs_educube,'r+',markersize=15,label='Data Points')
plt.plot(angs,line(angs,1,0),'k',linewidth=0.8,label='Expected Relation')
plt.plot(angs,line(angs,*fit[0]),'b',linewidth=0.8,label='Data Relation')
plt.ylabel(r'EduCube Angle [$^\circ$]',fontsize=16)
plt.xlabel(r'Measured Angle [$^\circ$]',fontsize=16)
plt.grid()
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=18)
fig.show()

fig.tight_layout()

fig.savefig('anglowambient.png',dpi=300)




#High ambient conditions.

angs_educubeh = np.array([1,170,104,157,178,176,255,353])

fit2 = curve_fit(line,angs,angs_educubeh)

fig2 =plt.figure(figsize=(12,8))

plt.title('EduCube Light-sensor Angle vs. Measured Angle (High Ambient)',fontsize=20)
plt.plot(angs,angs_educubeh,'r+',markersize=15,label='Data Points')
plt.plot(angs,line(angs,1,0),'k',linewidth=0.8,label='Expected Relation')
plt.plot(angs,line(angs,*fit2[0]),'b',linewidth=0.8,label='Data Relation')
plt.ylabel(r'EduCube Angle [$^\circ$]',fontsize=16)
plt.xlabel(r'Measured Angle [$^\circ$]',fontsize=16)
plt.grid()
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=18)
fig2.show()

fig2.tight_layout()

fig2.savefig('anghighambient.png',dpi=300)