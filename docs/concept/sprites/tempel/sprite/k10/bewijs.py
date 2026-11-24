import sys, numpy as np
sys.path.insert(0,'../k1'); sys.path.insert(0,'../k5')
from gereedschap import *
from clusters import tel
a8,pal8=laad('../k9/tempel.png'); a,pal=laad('tempel.png'); a6,_=laad('../k6/tempel.png')
o=[]
o.append(bewijs(a,pal,a8,pal8).replace('t.o.v. af','t.o.v. k9'))
o.append('palet gelijk aan k9: %s'%(pal==pal8))
d=a!=a8
mos=np.isin(a8,[8,9,13]); o.append('mos gewijzigd: %d'%(d&mos).sum())
o.append('goud gewijzigd: %d'%(d&np.isin(a8,[10,11])).sum())
o.append('voeglijnen (7) in k9 gewijzigd: %d'%(d&(a8==7)).sum())
o.append('buitenlijn (1) in k9 gewijzigd: %d'%(d&(a8==1)).sum())
wand=np.zeros_like(d); wand[15:57,48:62]=True
poort=np.zeros_like(d); poort[43:62,10:27]=True
o.append('wijzigingen bergwand (x48-61,y15-56): %d, alle binnen 6/f/e: %s'%((d&wand).sum(), bool(np.isin(a[d&wand],[6,14,15]).all() and np.isin(a8[d&wand],[6,14,15]).all())))
from collections import Counter
o.append('  overgangen wand: '+', '.join('%d->%d: %d'%(k[0],k[1],v) for k,v in sorted(Counter(zip(a8[d&wand].tolist(),a[d&wand].tolist())).items())))
o.append('wijzigingen poortlijnen (x10-26,y43-61): %d; '%(d&poort).sum()+', '.join('%d->%d: %d'%(k[0],k[1],v) for k,v in sorted(Counter(zip(a8[d&poort].tolist(),a[d&poort].tolist())).items())))
o.append('wijzigingen elders: %d'%(d&~wand&~poort).sum())
for x0,lab in [(0,'hele sprite'),(40,'x>=40')]:
    r=[]
    for p in ['../k6/tempel.png','../k9/tempel.png','tempel.png']:
        r.append('%d/%d'%(tel(p,x0)[0],tel(p,x0,8)[0]))
    o.append('clusters <3 px %s (4-/8-samenhang): k6 %s | k9 %s | k10 %s'%(lab,*r))
print('\n'.join(o)); open('bewijs.txt','w').write('\n'.join(o)+'\n')
