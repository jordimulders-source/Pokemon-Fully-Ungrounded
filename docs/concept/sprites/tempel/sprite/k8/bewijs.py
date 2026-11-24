import sys, numpy as np
sys.path.insert(0,'../k1'); sys.path.insert(0,'../k5')
from gereedschap import *
from clusters import tel
p=sys.argv[1] if len(sys.argv)>1 else 'tempel.png'
a0,pal0=laad('../k6/tempel.png'); a,pal=laad(p)
out=[bewijs(a,pal,a0,pal0)]
out[0]=out[0].replace('t.o.v. af','t.o.v. k6')
out.append('palet gelijk aan k6: %s'%(pal==pal0))
for naam,idx in [('buitenlijn (1)',[1]),('donkere lijn (2)',[2]),('voeglijn (7)',[7]),('mos (8,9,13)',[8,9,13]),('goud (10,11)',[10,11]),('deur (12)',[12])]:
    m0=np.isin(a0,idx); m=np.isin(a,idx)
    out.append('%s: posities gewijzigd %d, pixels gewijzigd binnen %d'%(naam,(m!=m0).sum(),((m|m0)&(a!=a0)).sum()))
out.append('bergwand/gevelschaduw (e,f in k6) gewijzigd: %d'%((np.isin(a0,[14,15]))&(a!=a0)).sum())
d=a!=a0
STAP=[3,4,5,6,15]
sprong=0
for y,x in zip(*np.where(d)):
    if abs(STAP.index(a[y,x])-STAP.index(a0[y,x]))!=1: sprong+=1
out.append('gewijzigde pixels: %d, waarvan meer dan 1 toonstap van k6: %d'%(d.sum(),sprong))
from collections import Counter
out.append('overgangen (k6->nieuw): '+', '.join('%d->%d: %d'%(k[0],k[1],v) for k,v in sorted(Counter(zip(a0[d].tolist(),a[d].tolist())).items())))
for x0,lab in [(0,'hele sprite'),(40,'x>=40')]:
    n0,_=tel('../k6/tempel.png',x0); n1,_=tel(p,x0); m0,_=tel('../k6/tempel.png',x0,8); m1,_=tel(p,x0,8)
    out.append('clusters <3 px (%s): k6 %d -> nieuw %d (4-samenhang) | k6 %d -> nieuw %d (8-samenhang)'%(lab,n0,n1,m0,m1))
print('\n'.join(out)); open(p.replace('.png','')+'_bewijs.txt' if p!='tempel.png' else 'bewijs.txt','w').write('\n'.join(out)+'\n')
p2=[(int(x),int(y)) for y,x in zip(*np.where(d)) if abs(STAP.index(a[y,x])-STAP.index(a0[y,x]))>1]
r='  waarvan buiten de steen onderblok (x37-49,y45-52): %d'%sum(1 for x,y in p2 if not(37<=x<=49 and 45<=y<=52))
print(r); open('bewijs.txt','a').write(r+'\n')
