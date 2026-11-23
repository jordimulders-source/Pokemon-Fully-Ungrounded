# meet.py: per spritepixel modelmetingen binnen het eigen onderdeel (zone_af.npy): vlakhelderheid zonder lijnen (gem, p15, p85),
# aandeel donkere modellijn (zwart) en aandeel lichte ijsbarst (helderheid > lokale mediaan + 45) -> meet.npz
import numpy as np; from scipy import ndimage as nd
from reductie_gedeeld import bron
from reductie_ice import laad
a,FG=laad(); f=np.load('model_fam.npz')['f'].astype(int); Z=np.load('model_zone.npz')['z'].astype(int)
L=0.30*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
med=nd.median_filter(L,size=15); BARST=(L>med+45)&(f>1); DONK=(f==1)|((L<med-50)&(f>1))
zone=np.load('zone.npy')
G=np.full((64,64),np.nan); p15=G.copy(); p85=G.copy(); BR=np.zeros((64,64)); DK=np.zeros((64,64))
for Y,X in zip(*np.where(zone>0)):
    vs=[];ws=[];tw=0;b=0;d=0
    for u,v,w in bron(X,Y):
        tw+=w; b+=w*BARST[v,u]; d+=w*DONK[v,u]
        if f[v,u]>1 and Z[v,u]==zone[Y,X]: vs.append(L[v,u]); ws.append(w)
    BR[Y,X]=b/tw; DK[Y,X]=d/tw
    if vs:
        vs=np.array(vs); ws=np.array(ws); G[Y,X]=(vs*ws).sum()/ws.sum(); p15[Y,X]=np.percentile(vs,15); p85[Y,X]=np.percentile(vs,85)
np.savez('meet.npz',G=G,p15=p15,p85=p85,BR=BR,DK=DK)
print('klaar', np.nanmean(G))
