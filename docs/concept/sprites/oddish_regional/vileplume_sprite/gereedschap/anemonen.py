# Anemonen in het natieve model: mondjes en schijfmaten gemeten op natief.png met raster (12x, lijnen per 5 px).
# Eigenaar = kleinste elliptische afstand tot het mondje (ellips met eigen straal links/rechts/boven/onder,
# want het mondje zit niet midden op de schijf). Volgorde voor -> achter: VL, VR, L, R, T.
import numpy as np
#        naam  cx    cy   links rechts boven onder voor
AN=[('VL',  82.5, 77.5, 21.0, 29.0, 18.0, 21.0, True),
    ('VR', 126.0, 72.0, 17.0, 22.0, 15.0, 22.0, True),
    ('L',   59.5, 58.5, 26.0, 33.0, 20.0, 30.0, False),
    ('R',  139.0, 53.5, 29.0, 24.0, 19.0, 29.0, False),
    ('T',  105.0, 41.0, 23.0, 23.0, 13.0, 12.0, False)]
# mondjes (ovaaltjes in het model): cx, cy, halve breedte, halve hoogte (natief, incl. donkere ring)
# buitenmaat van de ring gemeten op de klassenkaart: VL x78-88 y75-80, VR x120-132 y70-75, L x53-66 y56-61, R x133-145 y51-56, T x99-111 y39-43
MOND=[(83.5,78.0,6.0,3.5),(126.5,73.0,7.0,3.5),(60.0,59.0,7.0,3.5),(139.5,54.0,7.0,3.5),(105.5,41.5,7.0,3.0)]
# mondje in spritepixels (bbox van de modelring omgerekend: x=4+(u-36)*0,43, y=1+(v-28)*0,43): x0,x1,y0,y1
MONDBOX=[(22,26,21,23),(40,45,19,21),(11,16,13,15),(46,51,11,13),(31,36,5,7)]
def dnorm(i,u,v):
    n,cx,cy,l,r,b,o,f=AN[i]; dx=(u-cx)/(l if u<cx else r); dy=(v-cy)/(b if v<cy else o); return dx,dy
def afstand(i,u,v):
    dx,dy=dnorm(i,u,v); return float(np.hypot(dx,dy))
def hoek(i,u,v):
    dx,dy=dnorm(i,u,v); return float(np.arctan2(dy,dx))
def eigenaar(u,v):
    d=[afstand(i,u,v) for i in range(len(AN))]
    voor=[i for i in range(len(AN)) if AN[i][7] and d[i]<1]
    if voor: return min(voor,key=lambda i:d[i])
    return int(np.argmin(d))
def in_mond(i,u,v,extra=0.0):
    cx,cy,rx,ry=MOND[i]; return ((u-cx)/(rx+extra))**2+((v-cy)/(ry+extra))**2<=1
