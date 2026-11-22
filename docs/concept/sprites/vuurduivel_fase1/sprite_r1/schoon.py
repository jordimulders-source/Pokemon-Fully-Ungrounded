# schoon.py: automatische technische opschoning van kaal_01.png -> raster_auto.txt
# 1) amber -> geel naast geel, anders oranje; 2) losse pixels (geen enkele 4-buur van dezelfde klasse, niet # W p M) -> meest
# voorkomende 8-buur; 3) silhouetrand -> omlijning '#'
import numpy as np; from PIL import Image
from collections import Counter
CH='.#dmlRrOYbBkpWMa'
o=np.asarray(Image.open('kaal_01.png')).astype(int).copy()
H,W=o.shape
for y,x in zip(*np.where(o==15)):
    nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1)]
    o[y,x]=8 if 8 in nb else 7
o[o==15]=7
for it in range(2):
    p=o.copy()
    for y in range(1,H-1):
        for x in range(1,W-1):
            k=p[y,x]
            if k in (0,1,13,12,14): continue
            if all(p[y+dy,x+dx]!=k for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))):
                nb=Counter(p[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and p[y+dy,x+dx] not in (0,))
                if nb: o[y,x]=nb.most_common(1)[0][0]
# vlamvlekjes: losse stukjes r/O/Y < 3 px in het haar (y<=30) opgaan in de meest voorkomende vlam-buur (ruis weg, model-streken blijven)
def stukken(m):
    seen=np.zeros_like(m); out=[]
    for y,x in zip(*np.where(m)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=1; c=[]
        while st:
            a,b=st.pop(); c.append((a,b))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                p,q=a+dy,b+dx
                if 0<=p<H and 0<=q<W and m[p,q] and not seen[p,q]: seen[p,q]=1; st.append((p,q))
        out.append(c)
    return out
for it in range(2):
    for k in (6,7,8):
        m=(o==k); m[31:]=False
        for c in stukken(m):
            if len(c)>=3: continue
            nb=Counter(o[a+dy,b+dx] for a,b in c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[a+dy,b+dx] in (5,6,7,8) and o[a+dy,b+dx]!=k)
            # een geel puntje aan de rand (vlampunt) laten staan
            if k==8 and any(o[a+dy,b+dx]==0 for a,b in c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
            if nb:
                for a,b in c: o[a,b]=nb.most_common(1)[0][0]
fg=o>0
for y in range(1,H-1):
    for x in range(1,W-1):
        if fg[y,x] and (not fg[y-1,x] or not fg[y+1,x] or not fg[y,x-1] or not fg[y,x+1]):
            # vlammen hebben in het model geen zwarte lijn: rand = een tint donkerder dan de vlamkleur (gekleurde lijn), de rest zwart
            o[y,x]={8:7,7:6,6:5,5:5}[o[y,x]] if o[y,x] in (5,6,7,8) else 1
open('raster_auto.txt','w').write('\n'.join(''.join(CH[v] for v in r) for r in o)+'\n')
