from fit import *
def show(name,c0,r0,angs):
    c,R,n,mx=fit(np.array(c0,float),r0,angs); print(name,np.round(c,2),round(R,2),n,'maxres',round(mx,2))
show('voor',(60,127),20,[(160,300)])
show('voor2',(60,127),20,[(150,320)])
show('ver',(184,36),14,[(0,140)])
show('oogL',(72.5,63.5),10,[(100,260)])
show('oogR',(189,91.5),11,[(-80,80),(280,360)])
show('oogR2',(189,91.5),11,[(270,360),(0,60)])
