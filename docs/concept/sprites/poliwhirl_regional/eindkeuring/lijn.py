# Omlijningsronde volgens Dragonfly Cave: per buitenlijnpixel (1) het eigen materiaal en de normaal naar de lucht;
# lichtkant (licht linksboven) -> outline base van het eigen materiaal (geel 7, ijs b); schaduwkant blijft zwart.
import numpy as np
from zones import *
def materiaal(v):
    return 'Y' if v in YEL else 'I' if v in ICE else 'D' if v in DARK else 'R' if v in RED else None
def analyse(a):
    P=np.pad(a,1); res=[]
    for y in range(64):
        for x in range(64):
            if a[y,x]!=1: continue
            nx=ny=0; mats={}
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    if dx==dy==0: continue
                    v=P[y+1+dy,x+1+dx]
                    if v==0: nx+=dx; ny+=dy
                    else:
                        m=materiaal(v)
                        if m: mats[m]=mats.get(m,0)+(2 if dx==0 or dy==0 else 1)
            if nx==ny==0 and not any(P[y+1+dy,x+1+dx]==0 for dy in(-1,0,1) for dx in(-1,0,1)): continue
            own=max(mats,key=mats.get) if mats else None
            res.append((x,y,nx,ny,own,mats))
    return res
def licht(nx,ny):
    # licht linksboven: normaal met een omhoog-component, of naar links zonder omlaag-component
    return nx+ny<0
