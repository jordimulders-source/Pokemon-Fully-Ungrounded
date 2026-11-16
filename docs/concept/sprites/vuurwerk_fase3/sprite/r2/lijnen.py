# r2: ruis (vlekjes < 3 px, niet aan de rand) + lijnregels (punt 5) op r2_vlak.npy -> r2_lijn.npy
import numpy as np, json; from PIL import Image
from collections import Counter
a=np.load('r2_vlak.npy'); H,W=a.shape
Y,X=np.mgrid[:64,:64]; KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))
FAM={3:'kop',4:'kop',5:'kop',7:'roze',8:'roze',11:'rood',12:'rood',10:'rood',13:'geel',14:'geel',15:'geel',6:'donker'}
log=Counter()
def clusters(m,acht=True):
    seen=np.zeros_like(m,bool); r=[]
    for y in range(H):
        for x in range(W):
            if not m[y,x] or seen[y,x]: continue
            st=[(y,x)]; seen[y,x]=1; c=[]
            while st:
                p=st.pop(); c.append(p)
                for dy in (-1,0,1):
                    for dx in (-1,0,1):
                        if not acht and dy and dx: continue
                        q=(p[0]+dy,p[1]+dx)
                        if 0<=q[0]<H and 0<=q[1]<W and m[q] and not seen[q]: seen[q]=1; st.append(q)
            r.append(c)
    return r
def rand(y,x): return any(not(0<=y+dy<H and 0<=x+dx<W) or a[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))
def nbs(y,x): return [a[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W]
groot=max(clusters(a>0),key=len); inl=np.zeros_like(a,bool)
for p in groot: inl[p]=1
for ronde in range(3):
    for kk in range(3,16):
        if kk in (9,): continue
        for c in clusters(a==kk):
            if len(c)>=3 or not inl[c[0]]: continue
            for (y,x) in c:
                if rand(y,x): continue
                nb=[v for v in nbs(y,x) if v>2 and v!=9 and v!=kk]
                same=[v for v in nb if FAM.get(v)==FAM.get(kk)]
                nb=same or nb
                if nb: a[y,x]=Counter(nb).most_common(1)[0][0]; log['ruis']+=1
# lijnen
b=a.copy()
SEL={'kop':3,'roze':6,'donker':6,'rood':10,'geel':14}
def famnb(y,x):
    nb=[v for v in nbs(y,x) if v>2 and v!=9]
    if not nb: return None,None
    v=Counter(nb).most_common(1)[0][0]; return FAM.get(v),v
for y in range(H):
    for x in range(W):
        v=a[y,x]
        if v not in (1,2) or not inl[y,x]: continue
        t=lambda dy,dx: not(0<=y+dy<H and 0<=x+dx<W) or a[y+dy,x+dx]==0
        f,vv=famnb(y,x)
        if rand(y,x):
            licht=(t(-1,0) or t(0,-1)) and not (t(1,0) or t(0,1))
            if licht and f and v==1: b[y,x]=SEL[f]; log['lichtkant selout']+=1
        else:
            randbuur=any(a[y+dy,x+dx] in (1,2) and rand(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W)
            if KZ[y,x]: continue                      # kop: bruine modellijnen blijven (gezicht apart)
            if randbuur and vv: b[y,x]=vv; log['dubbele lijn -> vlak']+=1
            elif f: nv=10 if f=='rood' else 9; b[y,x]=nv; log['binnenlijn donkere tint']+=1
# vlakpixels op de buitenrand (dik deel) -> lijn; schaduwkant 1/2, lichtkant selout
c=b.copy()
for y in range(H):
    for x in range(W):
        v=b[y,x]
        if v<=2 or v==9 or not inl[y,x]: continue
        t=lambda dy,dx: not(0<=y+dy<H and 0<=x+dx<W) or b[y+dy,x+dx]==0
        if not(t(-1,0) or t(1,0) or t(0,-1) or t(0,1)): continue
        dik=all((not t(-dy,-dx)) and b[y-dy,x-dx]>0 for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)) if t(dy,dx) and 0<=y-dy<H and 0<=x-dx<W)
        if not dik: continue
        f=FAM.get(v); licht=(t(-1,0) or t(0,-1)) and not(t(1,0) or t(0,1))
        nv=SEL[f] if licht else (2 if f=='kop' else 1)
        if nv!=v: c[y,x]=nv; log['buitenrand']+=1
# kop-rand: kleur per pixel uit de modelrand (gemiddelde van de natieve randpixels in het blok -> dichtstbij van 2/6/3/7)
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); q=np.asarray(Image.open('natief_q_dg.png')); bgn=q==0
rn=np.zeros_like(bgn)
rn[1:-1,1:-1]=~bgn[1:-1,1:-1]&(bgn[:-2,1:-1]|bgn[2:,1:-1]|bgn[1:-1,:-2]|bgn[1:-1,2:])
P=np.array(json.load(open('palet_r2.json')),float)
S=12/5.12; OX=(106-4.25)/5.12-0.5; OY=(120-4.25)/5.12-0.5
for y in range(H):
    for x in range(W):
        if not KZ[y,x] or c[y,x]==0 or not inl[y,x]: continue
        if not any(not(0<=y+dy<H and 0<=x+dx<W) or c[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
        ys=slice(int(OY+y*S),int(np.ceil(OY+(y+1)*S))+1); xs=slice(int(OX+x*S),int(np.ceil(OX+(x+1)*S))+1)
        m=rn[ys,xs]
        if m.sum()==0: continue
        col=n[ys,xs][m].mean(0); ks=[2,6,3,7]; nv=ks[int(((P[ks]-col)**2).sum(1).argmin())]
        if nv!=c[y,x]: c[y,x]=nv; log['kop-rand uit model']+=1
# losse binnenlijnstipjes (9/10, 1 px, raakt geen andere lijn) zijn geen lijn: vlakkleur van de buren (buiten de pijl)
for y in range(1,H-1):
    for x in range(1,W-1):
        if c[y,x] in (9,10) and not (y>=44 and x<47):
            nb=[c[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
            if not any(v in (1,9,10) for v in nb):
                vl=[v for v in nb if v>2]; 
                if vl: c[y,x]=Counter(vl).most_common(1)[0][0]; log['los lijnstipje -> vlak']+=1
np.save('r2_lijn.npy',c); print(dict(log))
