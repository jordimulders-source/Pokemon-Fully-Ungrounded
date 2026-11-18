# Shuppets: silhouet = model (shupmask.py, dekking >= 0,5); delen (kop+hoorn, armpjes, voetje, romp) met ellipsen gepast
# op het model, alleen om te bepalen waar binnenlijnen (deel vóór deel) en tinten vallen. Volgorde: achter -> voor.
import numpy as np
from matplotlib.path import Path
def ell(cx,cy,rx,ry): return lambda x,y:((x-cx)/rx)**2+((y-cy)/ry)**2<=1
def tri(a,b,c):
    P=Path([a,b,c]); return lambda x,y:P.contains_point((x,y))
SH={
 'L':dict(box=(1,36,17,58),hoorn=tri((8.3,37.6),(6.6,42.8),(10.8,42.8)),
          delen=[('voet',[ell(12.3,55.4,1.4,1.0)]),('arm_l',[ell(7.0,52.3,1.4,1.0)]),('arm_r',[ell(13.7,52.2,2.0,2.0)]),
                 ('kop',[ell(9.5,46.0,5.6,4.3),tri((8.3,37.6),(6.6,42.8),(10.8,42.8))])]),
 'R':dict(box=(44,40,63,63),hoorn=tri((52.4,41.6),(50.2,48.2),(55.6,48.2)),
          delen=[('arm_l',[ell(49.6,57.3,2.1,1.3)]),('arm_r',[ell(58.4,57.7,1.6,1.4)]),
                 ('kop',[ell(53.0,51.0,6.0,4.1),tri((52.4,41.6),(50.2,48.2),(55.6,48.2))])]),
}
