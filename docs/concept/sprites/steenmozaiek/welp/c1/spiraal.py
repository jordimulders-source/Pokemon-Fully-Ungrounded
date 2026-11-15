# Hulp: rastert een Archimedische spiraal (1-px lijn, 8-verbonden) als tekstraster om daarna met de hand te bewerken.
import numpy as np, sys
def spiraal(rmax, spacing=3.0, rmin=0.8, turns_extra=0.0, cw=True, start=0.0, sx=1.0, sy=1.0):
    b=spacing/(2*np.pi); th_max=(rmax-rmin)/b
    pts=[]
    for th in np.linspace(0, th_max, 4000):
        r=rmin+b*th; a=start+(th if cw else -th)
        pts.append((r*np.cos(a)*sx, r*np.sin(a)*sy))
    P=np.array(pts); P=np.round(P).astype(int); P-=P.min(0)
    W,H=P.max(0)+1; g=np.zeros((H,W),bool)
    for x,y in P: g[y,x]=True
    return g
def toon(g):
    for r in g: print(''.join('g' if v else '.' for v in r))
if __name__=='__main__':
    for rm in (4,5,6):
        for st in (0,np.pi/2,np.pi,3*np.pi/2):
            print('rmax',rm,'start',round(st,2)); toon(spiraal(rm,start=st)); print()
