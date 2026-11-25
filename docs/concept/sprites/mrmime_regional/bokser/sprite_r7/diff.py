# diff.py: alle gewijzigde pixels t.o.v. r6-meer per zone; bewijst 0 buiten de zones
import numpy as np
a=np.load('bokser.npy'); b=np.load('../sprite_r6/var/meer.npy')
Z={'1 hoofd':(31,2,43,5),'7 ogen':(31,9,39,13),'6 schouder':(17,10,33,23),'2 V':(30,17,39,28),'5 vuist gestrekt':(10,8,20,17),'5 vuist borst':(37,19,47,27),'4 kruis':(30,35,46,43),'3 benen':(33,45,47,57)}
rest=np.ones(a.shape,bool)
for k,(x0,y0,x1,y1) in Z.items():
    m=np.zeros(a.shape,bool); m[y0:y1,x0:x1]=1; m&=rest; rest&=~m
    ys,xs=np.where((a!=b)&m); print(k,len(ys),' '.join(f'({x},{y}):{b[y,x]}>{a[y,x]}' for y,x in zip(ys,xs)))
print('BUITEN ZONES:',int(((a!=b)&rest).sum()),'| totaal',int((a!=b).sum()),'| kleuren',len(set(a.ravel()))-1)
