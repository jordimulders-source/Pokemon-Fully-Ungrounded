# Technische opschoning (geen vormen getekend):
# 1. handschoen uit de modus-reductie van hetzelfde model (zelfde raster; houdt het witte vlak wit)
# 2. buitenrand: randpixels van donkere delen -> zwart; van lichte delen (144/208/248) zwart aan de schaduwkant
#    (rand onder/rechts) en 112 als selout aan de lichtkant (rand boven/links). Stok en Rime-delen al omlijnd: overslaan.
# 3. losse pixels (1-px eilandjes van een tint midden in een vlak, niet naast een lijn) -> meest voorkomende buurtint; ogen/monocle overslaan.
import numpy as np
M=np.load('kaal_mode_idx.npy')
def schoon(C,log):
    C=C.copy()
    def zet(y,x,v,zone):
        if C[y,x]!=v: C[y,x]=v; log[zone]=log.get(zone,0)+1
    for y in range(26,34):
        for x in range(10,22):
            v=M[y-3,x]
            if v!=-1: zet(y,x,v,'handschoen uit modus-reductie (hand over de stok)')
    stok=lambda y,x: x<24 and 10<=y<=46 and not (26<=y<=33 and 10<=x<=21)
    ogen=lambda y,x: 13<=y<=21 and 27<=x<=46  # r5: oogvlak rijen 13-21
    H,W=C.shape; T=lambda y,x: C[y,x] if 0<=y<H and 0<=x<W else -1
    D=C.copy()
    for y in range(H):
        for x in range(W):
            v=D[y,x]
            if v<=0 or stok(y,x): continue
            nb={(dy,dx):(D[y+dy,x+dx] if 0<=y+dy<H and 0<=x+dx<W else -1) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))}
            open_=[k for k,t in nb.items() if t==-1]
            if not open_: continue
            if v>=5:
                licht=all(k in ((-1,0),(0,-1)) for k in open_)
                zet(y,x,4 if licht else 0,'buitenrand licht deel (selout 112 / zwart)')
            else: zet(y,x,0,'buitenrand donker deel -> zwart')
    D=C.copy()
    for y in range(1,H-1):
        for x in range(1,W-1):
            v=D[y,x]
            if v<=0 or stok(y,x) or ogen(y,x): continue
            n=[D[y-1,x],D[y+1,x],D[y,x-1],D[y,x+1]]
            if v not in n and -1 not in n and 0 not in n:   # pixels naast een lijn (snorkrul, glans) blijven
                nn=[t for t in n if t>0] or n
                zet(y,x,max(set(nn),key=nn.count),'losse pixel -> buurtint')
    return C
