import sys, numpy as np
sys.path.insert(0,'../k1'); sys.path.insert(0,'../k5')
from gereedschap import *
from clusters import tel
from collections import Counter
a8,_=laad('../k8/tempel.png'); a9,pal9=laad('../k9/tempel.png'); a,pal=laad('tempel.png')
o=[bewijs(a,pal,a9,pal9).replace('t.o.v. af','t.o.v. k9')]
o.append('palet gelijk aan k9: %s'%(pal==pal9))
wand=np.zeros(a.shape,bool); wand[15:57,48:62]=True
latei=np.zeros(a.shape,bool); latei[45:50,25:28]=True
d9=a!=a9
o.append('wijzigingen t.o.v. k9 buiten bergwand (x48-61,y15-56) en lateioverstek (x25-27,y45-49): %d'%(d9&~wand&~latei).sum())
poort=np.zeros(a.shape,bool); poort[43:62,10:27]=True
o.append('poort (x10-26,y43-61) t.o.v. k9 buiten de overstek: %d'%(d9&poort&~latei).sum())
d8=a!=a8
o.append('bergwand t.o.v. k8: %d px, alle binnen 6/f/e (oud en nieuw): %s'%((d8&wand).sum(),bool(np.isin(a[d8&wand],[6,14,15]).all() and np.isin(a8[d8&wand],[6,14,15]).all())))
o.append('  overgangen k8->k10 in de wand: '+', '.join('%d->%d: %d'%(k[0],k[1],v) for k,v in sorted(Counter(zip(a8[d8&wand].tolist(),a[d8&wand].tolist())).items())))
o.append('mos/voeg(7)/buitenlijn(1) in de wand gewijzigd t.o.v. k8: %d'%(d8&wand&np.isin(a8,[1,2,7,8,9,13])).sum())
o.append('lateioverstek: '+', '.join('(%d,%d) %d->%d'%(x,y,a9[y,x],a[y,x]) for y,x in zip(*np.where(d9&latei))))
o.append('alpha diff t.o.v. k9: %d (overstek valt binnen het silhouet)'%((a!=0)!=(a9!=0)).sum())
for x0,lab in [(0,'hele sprite'),(40,'x>=40')]:
    r=['%d/%d'%(tel(p,x0)[0],tel(p,x0,8)[0]) for p in ['../k6/tempel.png','../k8/tempel.png','../k9/tempel.png','tempel.png']]
    o.append('clusters <3 px %s (4-/8-samenhang): k6 %s | k8 %s | k9 %s | k10 %s'%(lab,*r))
print('\n'.join(o)); open('bewijs.txt','w').write('\n'.join(o)+'\n')
