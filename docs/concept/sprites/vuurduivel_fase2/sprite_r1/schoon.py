# schoon.py: automatische technische opschoning van kaal_00.png -> raster_auto.txt
# 1) middenrood -> oranjerood naast oranje(rood), anders rood; 2) losse pixels (geen 4-buur van dezelfde klasse) -> meest
# voorkomende 8-buur (oog en crème niet); 3) vlamvlekjes <3 px binnenin opgaan in de vlam-buur (punten aan de rand blijven);
# 4) silhouetrand -> zwart; vlammen een tint donkerder (model heeft daar geen zwarte lijn)
import numpy as np; from PIL import Image
from collections import Counter
CH='.#dgHhBcCRrOAYm'
# . transp # zwart d grijs1 g grijs2 H hoorn/bruin1 h bruin2 B bruin3 c crème-schaduw C crème R donkerrood r rood O oranjerood A oranje Y geel
o=np.asarray(Image.open('kaal_00.png')).astype(int).copy()
H,W=o.shape
for y,x in zip(*np.where(o==14)):
    nb=[o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1)]
    o[y,x]=11 if (11 in nb or 12 in nb) else 10
for it in range(2):
    p=o.copy()
    for y in range(1,H-1):
        for x in range(1,W-1):
            k=p[y,x]
            if k in (0,1,7,8): continue
            if all(p[y+dy,x+dx]!=k for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))):
                nb=Counter(p[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and p[y+dy,x+dx]!=0)
                if nb: o[y,x]=nb.most_common(1)[0][0]
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
FIRE=(9,10,11,12,13)
for it in range(2):
    for k in (10,11,12,13):
        for c in stukken(o==k):
            if len(c)>=3: continue
            if any(o[a+dy,b+dx]==0 for a,b in c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
            nb=Counter(o[a+dy,b+dx] for a,b in c for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[a+dy,b+dx] in FIRE and o[a+dy,b+dx]!=k)
            if nb:
                for a,b in c: o[a,b]=nb.most_common(1)[0][0]
fg=o>0
for y in range(1,H-1):
    for x in range(1,W-1):
        if fg[y,x] and (not fg[y-1,x] or not fg[y+1,x] or not fg[y,x-1] or not fg[y,x+1]):
            o[y,x]={13:12,12:11,11:10,10:9,9:9}[o[y,x]] if o[y,x] in FIRE else 1
open('raster_auto.txt','w').write('\n'.join(''.join(CH[v] for v in r) for r in o)+'\n')
