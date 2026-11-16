# Technisch opschonen van de kale (ontglitterde) reductie: (a) ruis: vlekjes < 3 px van een tint (8-buren, zodat diagonale vlamstrepen blijven) krijgen de meest
# voorkomende buurtint (8-buren, geen transparant/omlijning); losse eilandjes buiten het lijf (twinkels/vlammetjes) blijven.
# (b) buitenlijn 1 px: randpixel naar de omlijning van zijn kleurgroep (schaduwkant zwart 1 / bruin 2 bij de kop;
# lichtkant boven/links: donkere tint van de groep = gekleurde selout).
import sys, json, numpy as np; from PIL import Image
from collections import Counter
PAL=json.load(open('palet.json'))
IN=sys.argv[1] if len(sys.argv)>1 else 'kaal_dg.png'; OUT=sys.argv[2] if len(sys.argv)>2 else 'opgeschoond.png'
a=np.asarray(Image.open(IN)).astype(int); H,W=a.shape
FAM={3:'kop',4:'kop',5:'kop',15:'geel',6:'roze',7:'roze',8:'roze',9:'roze',10:'rood',11:'rood',12:'rood',13:'geel',14:'geel'}
SEL={'kop':3,'roze':6,'rood':10,'geel':14}; DONK={'kop':2,'roze':1,'rood':1,'geel':1}
def clusters(a,k):
    seen=np.zeros_like(a,bool); res=[]
    for y in range(H):
        for x in range(W):
            if a[y,x]!=k or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                p=st.pop(); c.append(p)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                    q=(p[0]+dy,p[1]+dx)
                    if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and a[q]==k: seen[q]=1; st.append(q)
            res.append(c)
    return res
# eilanden (los van het grote lijf) bewaren
op=a>0; lab=np.zeros_like(a); 
isl=clusters(np.where(op,1,0),1); groot=max(isl,key=len); inlijf=np.zeros_like(op)
for p in groot: inlijf[p]=1
log=Counter()
FAMI={'kop':[3,4,5],'roze':[7,8,9],'rood':[10,11,12],'geel':[13,14,15],'donker':[6]}
def famof(v):
    for f,ks in FAMI.items():
        if v in ks: return f
    return None
def nbs(y,x):
    return [a[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W]
# (a1) kleurgroep-vlekjes < 3 px (8-buren) -> meest voorkomende buurkleur uit een andere groep
for ronde in range(2):
    for f,ks in FAMI.items():
        fm=np.isin(a,ks).astype(int)
        for c in clusters(fm,1):
            if len(c)>=3 or not inlijf[c[0]]: continue
            for (y,x) in c:
                nb=[v for v in nbs(y,x) if v>2 and famof(v)!=f]
                if nb: a[y,x]=Counter(nb).most_common(1)[0][0]; log['ruis groep']+=1
# (a2) tint-vlekjes < 3 px binnen een groep -> meest voorkomende buurtint van dezelfde groep
for ronde in range(2):
    for k in range(3,15):
        for c in clusters(a,k):
            if len(c)>=3 or not inlijf[c[0]]: continue
            for (y,x) in c:
                nb=[v for v in nbs(y,x) if v>2 and v!=k and famof(v)==famof(k)]
                if nb: a[y,x]=Counter(nb).most_common(1)[0][0]; log['ruis tint']+=1
# (a3) losse donkere streepjes (1/2, <= 2 px, nergens aan de rand) in het roze/rode lijf: modellijn onder een vlamstreep,
#      Gen 3: binnenlijn in de donkere tint van het vlak -> donkermagenta 6
for c in clusters(np.isin(a,[1,2]).astype(int),1):
    if len(c)>2: continue
    if any((a[max(0,y-1):y+2,max(0,x-1):x+2]==0).any() for (y,x) in c): continue
    if any(x<24 for (y,x) in c): continue   # kop/gezicht niet
    for p in c: a[p]=6; log['binnenlijn']+=1
b=a.copy()
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v<=2 or not inlijf[y,x]: continue
        t=lambda dy,dx: not(0<=y+dy<H and 0<=x+dx<W) or a[y+dy,x+dx]==0
        if not(t(-1,0) or t(1,0) or t(0,-1) or t(0,1)): continue
        # dun deel (1 px dik in de richting van de rand): kleur van het model houden
        dik=all((not t(-dy,-dx)) and a[y-dy,x-dx]>0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if t(dy,dx) and 0<=y-dy<H and 0<=x-dx<W)
        if not dik: continue
        f=FAM[v]; licht=(t(-1,0) or t(0,-1)) and not(t(1,0) or t(0,1))
        nv=SEL[f] if licht else DONK[f]
        if nv!=v: b[y,x]=nv; log['buitenlijn']+=1
im=Image.fromarray(b.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save(OUT,transparency=0)
print(dict(log))
