# Ronde 2, stap A: grijze delen (vleugels, staart, dij, poten) opnieuw uit het model: vlaktint = gemiddelde
# niet-lijnkleur van het natieve vlak (dichtstbijzijnde grijs), binnenlijn alleen waar een echte modellijn
# (component >= 5 natieve px, lijnen.py) doorheen loopt; spikkels uit het model worden vlak.
import numpy as np
from gemeen import *
k=np.load('kaal.npy'); hit=np.load('lijnhit.npy'); mc=np.load('meanc.npy'); s=k.copy(); Hh,Ww=k.shape
GR=[5,8,9,10]
def grijs(c): return min(GR,key=lambda i:((P[i]-c)**2).sum())
Y,X=np.mgrid[0:Hh,0:Ww]
kop=(Y<=11)&(X<=16)
zone=(k>0)&~kop&((np.isin(k,GR))|((k==1)&(mc.mean(2)>85)))
# lijnpixels in de zone die omringd zijn door grijs ook meenemen
for y,x in zip(*np.nonzero((k==1)&~kop)):
    nb=k[max(y-1,0):y+2,max(x-1,0):x+2]; 
    if np.isin(nb,GR).sum()>=3 and mc[y,x].mean()>85: zone[y,x]=True
lum=mc.mean(2); vals=lum[zone&(hit==0)]
q=np.quantile(vals,[0.2,0.5,0.8]); print('toondrempels',q.round(1))
def toon(l): return 5 if l<q[0] else 8 if l<q[1] else 9 if l<q[2] else 10
for y,x in zip(*np.nonzero(zone)):
    s[y,x]=1 if hit[y,x]>=1 else toon(lum[y,x])
np.save('grijs.npy',s); np.save('zone.npy',zone)
print('zone px',zone.sum(),'gewijzigd',int((s!=k).sum()))
# buitenlijn: randpixel van de zone, onderdeel >=3 px dik -> omlijning; 2 px dik -> alleen de schaduwkant (rechts/onder) omlijning
t=lambda y,x: (y<0 or x<0 or y>=Hh or x>=Ww or s[y,x]==0)
s2=s.copy()
for y,x in zip(*np.nonzero(zone)):
    for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
        if not t(y+dy,x+dx): continue
        if t(y-dy,x-dx): continue
        if not t(y-2*dy,x-2*dx): s2[y,x]=1; break
        if (dy,dx) in ((1,0),(0,1)): s2[y,x]=1; break
s=s2
np.save('grijs.npy',s)
print('na buitenlijn gewijzigd t.o.v. kaal',int((s!=k).sum()))
