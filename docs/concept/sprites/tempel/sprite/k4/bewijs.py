import sys, os, numpy as np
sys.path.insert(0,'../k1')
from gereedschap import *
a0,pal0=laad(); a,pal=laad('tempel.png')
out=[bewijs(a,pal,a0,pal0)]
out.append('palet gelijk aan af: %s'%(pal==pal0))
out.append('buitenlijn (index 1) posities gewijzigd: %d'%((a==1)!=(a0==1)).sum())
mos=lambda q: np.isin(q,[8,9,13])
out.append('mos gewijzigd: %d'%((mos(a)|mos(a0))&(a!=a0)).sum())
zones={'gevel G1 (x22-29,y19-26)':(22,19,29,26),'gevel G2 (x35-41,y20-26)':(35,20,41,26),'gevel G3 (x32-36,y9-14)':(32,9,36,14),
 'bovenste blok, gevelplaten + zijvlak (x41-51,y6-9)':(41,6,51,9),
 'bergwand + zijvlakken + bovenvlak blok (x40-61,y11-60)':(40,11,61,60),
 'voeg naast de deur rechts (x26-31,y49-59)':(26,49,31,59)}
d=(a!=a0); tot=0; gedekt=np.zeros_like(d)
for n,(x0,y0,x1,y1) in zones.items():
    m=np.zeros_like(d); m[y0:y1+1,x0:x1+1]=True; m&=~gedekt; c=(d&m).sum(); gedekt|=m; out.append('  %s: %d px'%(n,c)); tot+=c
out.append('wijzigingen buiten deze zones: %d'%(d&~gedekt).sum())
ys,xs=np.where(d&~gedekt); out.append('  '+str(list(zip(xs.tolist(),ys.tolist()))))
open('bewijs.txt','w').write('\n'.join(out)+'\n'); print('\n'.join(out))
