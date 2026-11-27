# modus.py: per spritepixel de toonklasse met het grootste natieve oppervlak (scherp, geen gemiddelde)
import numpy as np
from reduceer import X0,Y0,s,LEFT,TOP
def toon(c):
    r,g,b=[int(v) for v in c]; L=(r+g+b)/3
    if L>245: return '.'
    if L<45: return '#'
    if r-b>60 and g>150:                       # stekelgeel
        return 4 if L>205 else 3 if L>180 else 2
    if r-b>60: return 2 if g<140 and g>110 else 14   # olijf / oranje
    if abs(r-b)<16: return 'g'
    if L>190: return 9
    if L>140: return 8
    if L>112: return 7
    if L>92: return 6
    return 5
def modus(sx,sy,nat):
    ya=Y0+(sy-TOP)*s; xa=X0+(sx-LEFT)*s; w={}
    for y in range(int(np.floor(ya)),int(np.ceil(ya+s))):
        for x in range(int(np.floor(xa)),int(np.ceil(xa+s))):
            ww=max(0,min(y+1,ya+s)-max(y,ya))*max(0,min(x+1,xa+s)-max(x,xa))
            if ww<=0: continue
            t=toon(nat[y,x]); w[t]=w.get(t,0)+ww/(s*s)
    return w
