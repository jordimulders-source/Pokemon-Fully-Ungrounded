# Pixeldiff r6 t.o.v. r4 per zone (bevroren zones moeten 0 zijn).
from PIL import Image; import numpy as np
a=np.array(Image.open('sprite_r6/sprite.png')).astype(int); r=np.array(Image.open('sprite_r4/sprite.png')).astype(int)
pa=np.array(Image.open('sprite_r6/sprite.png').getpalette()[:42]); pr=np.array(Image.open('sprite_r4/sprite.png').getpalette()[:39])
print('palet idx0-12 gelijk:',(pa[:39]==pr).all(),'| nieuw idx13 =',pa[39:42])
d=a!=r
Y,X=np.mgrid[0:64,0:64]
G=np.isin(r,[2,3,4,5,6])
zones={'gezicht x0-23 y29-48':(X<=23)&(Y>=29)&(Y<=48),
       'wolken (r4 bleekgroen 4 + groen x>=40, y>=15)':(Y>=15)&((r==4)|(G&(X>=40))),
       'geestwielen (groen x>=24 y>=40)':G&(Y>=40)&(X>=24),
       'kleine geest (y0-14)':Y<=14,
       'koeienvanger (x0-23 y49-60)':(X<=23)&(Y>=49)&(Y<=60),
       'lijf/kieren (x24-39 y16-44)':(X>=24)&(X<=39)&(Y>=16)&(Y<=44)&~(G&(Y>=40))}
for k,m in zones.items(): print('%-48s %4d px anders'%(k,(d&m).sum()))
alles=np.zeros_like(d)
for m in zones.values(): alles|=m
print('buiten alle zones anders:',(d&~alles).sum(), list(zip(*np.where(d&~alles)))[:10])
print('kleuren:',len(np.unique(a)),'(incl. transparant)')
