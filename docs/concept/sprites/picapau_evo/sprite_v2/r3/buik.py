# 4 buik: losse zwarte pixels in de onderbuik weg (modelbuik loopt door tot rij 44, pootbovenkant (22,44) uit het model),
# schaduw als sikkel rechtsonder (licht linksboven), 3 tinten C/c/k; selout k langs de linkerrand blijft.
import numpy as np
def run(o):
    n=o.copy()
    for x,y in [(24,42),(22,43),(23,43),(25,43)]: n[y,x]=7          # zwarte losse pixels -> buik (model: D)
    n[44,22]=1                                                      # pootbovenkant links (model (22,44) zwart onderaan), gat dicht
    Z=lambda x,y: 11<=x<=31 and 23<=y<=44
    B=lambda x,y: n[y,x] in (5,6,7)
    sel=set()
    for y in range(23,45):
        for x in range(11,32):
            if B(x,y) and n[y,x-1]==0: sel.add((x,y))                 # selout linkerrand
            if B(x,y) and n[y,x-1]==0 and x+1<64 and n[y,x+1]==7 and n[y-1,x]==0: sel.add((x+1,y))
    out=n.copy()
    for y in range(23,45):
        for x in range(11,32):
            if not B(x,y) or (x,y) in sel: continue
            def uit(dx,dy): return not B(x+dx,y+dy)
            if uit(1,1) and uit(0,1) and y>=39: t=7
            elif any(uit(dx,dy) for dx,dy in [(3,1),(2,2),(3,0),(2,3),(3,2),(1,2)]): t=6
            else: t=5
            out[y,x]=t
    for y in range(23,45):                                           # losse tintpixel (alle buikburen anders) -> meerderheid
        for x in range(11,32):
            if out[y,x] in (5,6,7) and (x,y) not in sel:
                nb=[out[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if out[y+dy,x+dx] in (5,6,7)]
                if len(nb)>=3 and out[y,x] not in nb: out[y,x]=max(set(nb),key=nb.count)
    for x in (25,26,27): out[41,x]=6                                # C-tong in de onderste sikkel dicht
    for x in range(21,31): out[43,x]=7                               # donkerste rand onderaan: 1 rij k boven de zwarte buitenlijn
    out[42,30]=7
    return out
if __name__=='__main__':
    o=np.load('_tmp/s3.npy'); n=run(o); np.save('_tmp/s4.npy',n); print('buik px',(n!=o).sum())
