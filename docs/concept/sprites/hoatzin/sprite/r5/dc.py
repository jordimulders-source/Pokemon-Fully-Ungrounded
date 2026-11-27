# Hoatzin r5: Dragonfly Cave-eindkeuring op r4 (alleen uitvoering: belijning + tinten). Silhouet blijft gelijk (alpha-diff 0).
# DC-gids r. 80-170/340-470: per onderdeel een outline base in de eigen donkerste tint, zwart alleen als outline shadow aan de
# schaduwkant, 1 px, outline highlights binnen de lijn. Gemeten maatstaf (rand.py): buitenlijn rechts/onder vrijwel geheel zwart
# (skinguin 190/201, dundragoon 159/159, awki 120/170); links/boven selout in eigen tint (Murkrow: lijftinten 58-122).
import numpy as np, sys, os
from PIL import Image
HIER=os.path.dirname(os.path.abspath(__file__))
R4=HIER+'/../r4/'
LIJF={2,3,4}; GG={5,6,7}; BL={8,9}; RO={10,11}
DONKER={'L':2,'G':5,'B':8,'R':10}
def groep(v):
    return 'L' if v in LIJF else 'G' if v in GG else 'B' if v in BL else 'R' if v in RO else None
N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy,dx)!=(0,0)]
N4=((-1,0),(1,0),(0,-1),(0,1))
def tr(a,y,x): return y<0 or x<0 or y>=64 or x>=64 or a[y,x]==0
def bewerk(a):
    o=a.copy(); tel={}
    def t(k,n=1): tel[k]=tel.get(k,0)+n
    for y in range(64):
        for x in range(64):
            v=a[y,x]
            if v==0: continue
            if not any(tr(a,y+dy,x+dx) for dy,dx in N4): continue      # alleen de buitenrand (4-buren)
            ny=sum(dy for dy,dx in N8 if tr(a,y+dy,x+dx)); nx=sum(dx for dy,dx in N8 if tr(a,y+dy,x+dx))
            dun=(tr(a,y-1,x) and tr(a,y+1,x)) or (tr(a,y,x-1) and tr(a,y,x+1))
            licht=(nx+ny<0) or (nx+ny==0 and ny<0)       # normaal (8-buren) wijst naar het licht linksboven (bij gelijkspel: boven)
            g=groep(v)
            if g is None:   # zwarte randpixel: groep uit de binnenburen
                c=[groep(a[y+dy,x+dx]) for dy,dx in N4 if not tr(a,y+dy,x+dx)]
                c=[q for q in c if q]
                g=max(sorted(set(c),key=lambda q:q!='L'),key=c.count) if c else None   # gelijkspel: lijf
            if g=='G' and dun:
                # dunne zuurpunt (1 px breed): blijft zuur, maar geen lichtste tint op de rand -> midden
                if v==7: o[y,x]=6; t('zuurpunt dun l->g')
                continue
            if licht and g:
                nv=DONKER[g]
            else:
                nv=1
            if nv!=v:
                o[y,x]=nv; t(f'{"selout" if licht else "zwart"} {g}')
    # afwisseling op één rand voorkomen (SPRITE_KERN: nooit zwart en selout om en om): losse randpixels die van al hun
    # randburen verschillen volgen de rand (onder-links = zwart, linkerteenpunt = selout).
    for (x,y,nv) in [(23,42,1),(20,57,2),(37,59,1),(34,61,1)]:
        if o[y,x]!=nv: o[y,x]=nv; t('rand eenduidig')
    return o,tel
if __name__=='__main__':
    a=np.array(Image.open(R4+'hoatzin_r4.png'))
    o,tel=bewerk(a); print(tel, (o!=a).sum())
    ch='.KDMLolgbBxR'
    for y in range(64): print('%2d '%y+''.join((ch[o[y,x]].upper() if o[y,x]!=a[y,x] and o[y,x]>1 else ('k' if o[y,x]!=a[y,x] else ch[o[y,x]])) for x in range(64)))
