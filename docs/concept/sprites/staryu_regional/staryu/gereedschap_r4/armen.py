# armen.py SPRITE.png: armhoeken en -lengtes vanaf het juweelmidden, model (natief, omgerekend naar spritecoördinaten) tegen sprite.
import sys, math; sys.path.insert(0,'gereedschap_r4'); from gemeen import *; from klassen import klassen
a,c,L=klassen()
def tips(pts,cx,cy):
    # 5 armtippen = lokale maxima van de afstand per hoeksector van 72 graden rond de grootste afstand
    d=[(math.hypot(x-cx,y-cy),(math.degrees(math.atan2(-(y-cy),x-cx)))%360,x,y) for x,y in pts]
    best=max(d); res=[]
    for k in range(5):
        h0=(best[1]+72*k)%360
        sec=[t for t in d if min(abs(t[1]-h0),360-abs(t[1]-h0))<=30]
        res.append(max(sec))
    return sorted(res,key=lambda t:t[1])
jm=np.argwhere(c==4); jv,ju=jm.mean(0)
cxm=(ju+.5-U0)*S+X0; cym=(jv+.5-V0)*S+Y0
mp=[((u+.5-U0)*S+X0,(v+.5-V0)*S+Y0) for v,u in np.argwhere(c>0)]
o=np.asarray(Image.open(sys.argv[1])).astype(int)
sj=np.argwhere((o>=9)&(o<=13)); cys,cxs=sj.mean(0)+.5
sp=[(x+.5,y+.5) for y,x in np.argwhere(o>0)]
print('juweelmidden model (%.1f,%.1f) sprite (%.1f,%.1f)'%(cxm,cym,cxs,cys))
for (dm,hm,xm,ym),(ds,hs,xs,ys) in zip(tips(mp,cxm,cym),tips(sp,cxs,cys)):
    print('arm hoek model %5.1f sprite %5.1f (verschil %+.1f) | lengte model %4.1f sprite %4.1f (%+.1f px) | tip model (%.1f,%.1f) sprite (%.1f,%.1f)'%(hm,hs,hs-hm,dm,ds,ds-dm,xm,ym,xs,ys))
