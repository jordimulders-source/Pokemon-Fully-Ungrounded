# Meet Poliwhirls spiraal (gba): banden in poolcoordinaten rond het midden; fit Archimedes r = r0 + p*phi/(2pi) met draairichting.
import numpy as np; from PIL import Image
a=np.array(Image.open('../../../../../graphics/pokemon/poliwhirl/anim_front_gba.png'))[:64]
yy,xx=np.mgrid[0:64,0:64]
disc=(yy>=21)&(yy<=41)&(xx>=19)&(xx<=42)&np.isin(a,[1,2,3,4,8,9,15])
band=disc&np.isin(a,[8,9,15])
def meet(cx,cy):
    pts=[]
    for deg in range(0,360,10):
        t=np.deg2rad(deg); run=[]
        for r in np.arange(0,11.01,0.25):
            x=int(round(cx+r*np.cos(t))); y=int(round(cy-r*np.sin(t)))
            if not disc[y,x]: break
            if band[y,x]: run.append(r)
            elif run: pts.append((deg,np.mean(run),run[-1]-run[0])); run=[]
        if run: pts.append((deg,np.mean(run),run[-1]-run[0]))
    return pts
best=None
for cx in np.arange(29.5,33.01,0.5):
    for cy in np.arange(30,34.01,0.5):
        pts=[p for p in meet(cx,cy) if p[1]>=1.5]
        for d in (1,-1):
            for p in np.arange(3,5.01,0.1):
                for ph in np.arange(0,360,5):
                    err=0
                    for deg,r,_ in pts:
                        u=(d*(deg-ph))%360/360*p     # straal van de arm in fase
                        k=np.round((r-u)/p); err+=min(abs(r-u-k*p),1.5)
                    e=err/len(pts)
                    if best is None or e<best[0]: best=(e,cx,cy,d,p,ph)
print('fit: fout %.3f midden (%.1f,%.1f) richting %d (1 = straal groeit tegen de klok in) spoed %.2f fase %d'%best)
e,cx,cy,d,p,ph=best
pts=meet(cx,cy)
# binnen- en buiteneinde: kleinste/grootste armstraal met band
rs=[(deg,r) for deg,r,_ in pts]
print('binnenste bandpunt',min(rs,key=lambda q:q[1]),'buitenste',max(rs,key=lambda q:q[1]))
np.save('pw_fit.npy',np.array([cx,cy,d,p,ph]))
# unwrapped fase per bandpunt -> binnen- en buiteneinde (graden langs de arm)
phis=[]
for deg,r,_ in pts:
    u=(d*(deg-ph))%360; k=np.round((r-u/360*p)/p); phis.append(u+360*k)
print('fase binnen %.0f buiten %.0f graden (%.2f windingen)'%(min(phis),max(phis),(max(phis)-min(phis))/360))
np.save('pw_fit.npy',np.array([cx,cy,d,p,ph,min(phis),max(phis)]))
