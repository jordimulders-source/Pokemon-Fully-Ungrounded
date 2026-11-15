# Rots-pass op het lijf (Gen 3-studie studie.png: Onix, Nosepass, Lunatone, Regirock):
# - belijning: gekleurd (2) aan de lichtkant, zwart (1) aan de schaduwkant; kant bepaald met een gladde normaal
#   (zwaartepunt van de lege pixels in 5x5), zodat er nooit 1 en 2 om en om op één rand staan;
# - schaduwkant 1 px dikker: schaduwvlak 3 direct binnen de zwarte buitenlijn wordt 2;
# - scherpe hooglichtrand (14) op de bovenkant van lichte facetten (5) direct onder een naar boven gerichte lichte rand;
# - donkere spleet (1) waar de dij over de voorpoot valt.
# Gezicht (bevroren rechthoek) en silhouet blijven.
import numpy as np
from basis import bevroren_kop
FACE=bevroren_kop()
SPLEET=[(37,y) for y in range(49,57)]+[(26,34),(27,34)]   # dij over voorpoot; kaak over hals
def normaal(m,y,x,r=2):
    ny=nx=0.0
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            Y,X=y+dy,x+dx
            if not (0<=Y<64 and 0<=X<64) or not m[Y,X]: ny+=dy; nx+=dx
    n=(ny*ny+nx*nx)**.5 or 1
    return ny/n,nx/n
def rand(m):
    r=np.zeros_like(m)
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)): r|=m&~np.roll(np.roll(m,dy,0),dx,1)
    return r
def rots(a):
    a=a.copy(); m=a>0; o=a.copy(); R=rand(m)
    for y,x in zip(*np.where(R)):
        if FACE[y,x] or a[y,x] not in (1,2): continue
        ny,nx=normaal(m,y,x)
        licht=(-ny-nx)/2**.5 > 0.25
        o[y,x]=2 if licht else 1
        sy,sx=int(np.sign(round(ny))),int(np.sign(round(nx)))
        Y,X=y-sy,x-sx
        if not (0<=Y<64 and 0<=X<64) or FACE[Y,X] or R[Y,X]: continue
        if licht and ny<-0.6 and a[Y,X]==5: o[Y,X]=14
        if not licht and a[Y,X]==3: o[Y,X]=2
    for x,y in SPLEET:
        if a[y,x]==2: o[y,x]=1
    return o
def palet(p): return list(p)
