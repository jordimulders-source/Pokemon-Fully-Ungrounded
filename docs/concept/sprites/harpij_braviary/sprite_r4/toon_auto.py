import numpy as np; from pal import *
l=np.load('lijn.npy'); avg=np.load('avg.npy'); Lm=avg.mean(2); z=lees('zones.txt')
g=np.full(l.shape,'.')
T={'k':[(45,'K'),(75,'a'),(112,'b'),(999,'c')],'w':[(45,'K'),(75,'a'),(112,'b'),(999,'c')],
   'h':[(70,'K'),(165,'g'),(205,'h'),(999,'i')],'s':[(45,'K'),(80,'s'),(150,'t'),(999,'u')],
   'n':[(40,'n'),(999,'n')],'b':[(45,'K'),(110,'a'),(170,'h'),(222,'i'),(999,'W')],'p':[(45,'K'),(85,'s'),(160,'t'),(999,'u')]}
for y,x in zip(*np.nonzero(l)):
    zz=z[y,x]
    if zz=='.': continue
    if l[y,x]==1 and zz!='n': g[y,x]='K'; continue
    for t,c in T[zz]:
        if Lm[y,x]<t: g[y,x]=c; break
schrijf('stap_tonen.txt',g)
