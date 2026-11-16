# r18 koeienvanger: modellijnen (natief.png, skelet per lijnpixel) als doorlopende 1-px-lijnen, vulling = dichtstbijzijnde paletkleur
# van de niet-lijnpixels van het model in de voetafdruk. Silhouet (buitenlijn) van r17 blijft; groen bevroren.
from lijnen import *
from collections import Counter
GR={2,3,4,5,6,13}; FILL=[7,8,9,10,11,12]; RUST={8,9}; GREY={7,10,11,12}
def ok(y,x): return 0<=y<64 and 0<=x<64
def nb8(a,y,x): return [a[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and ok(y+dy,x+dx)]
def nb4(a,y,x): return [a[y+dy,x+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0)) if ok(y+dy,x+dx)]
# polylijnen in natieve pixelcoordinaten (nx,ny), afgelezen van het Zhang-Suen-skelet van natief.png (lum<52)
V=[(13,64),(14,66),(15,67),(16,68),(17,67),(18,66),(19,65),(20,66),(21,67),(22,68),(23,69),(24,70),(25,71),(26,70),(27,69),(28,68),
   (29,67),(30,67),(31,67),(32,68),(33,69),(34,68),(35,68),(36,67),(37,66),(38,66),(39,66),(40,66)]
NADEN={'A':[(13,71),(13,72),(13,73),(13,74),(13,75)],
       'B':[(19,71),(18,72),(18,73),(18,74),(17,75),(17,76),(17,77),(17,78)],
       'C':[(25,71),(25,72),(24,73),(24,74),(23,75),(23,76),(23,77),(22,78),(22,79),(22,80),(21,81)],
       'D':[(31,72),(30,73),(30,74),(29,75),(29,76),(29,77),(30,78)]}
GROEVEN={'Bv':[(20,72),(20,73),(21,74)],'D2':[(32,74),(32,75),(31,76),(31,77)],'E':[(36,72),(35,73),(36,74)]}
def raster(pl,step=0.05):
    cells=[]
    for (ax,ay),(bx,by) in zip(pl,pl[1:]+[pl[-1]]):
        n=max(1,int(np.hypot(bx-ax,by-ay)/step))
        for t in np.linspace(0,1,n+1):
            X,Y=n2s(ax+(bx-ax)*t+.5,ay+(by-ay)*t+.5); c=(int(np.floor(Y)),int(np.floor(X)))
            if c not in cells: cells.append(c)
    return cells
def dun(cells):
    # pixel-perfect: haal 'L-hoek'-pixels weg (8-verbonden 1-px-lijn)
    s=list(cells); i=1
    while i<len(s)-1:
        (y0,x0),(y1,x1),(y2,x2)=s[i-1],s[i],s[i+1]
        if abs(y2-y0)==1 and abs(x2-x0)==1 and (y1==y0 or x1==x0): s.pop(i)
        else: i+=1
    return s
PAL=None
def nearest(rgb):
    best=None
    for i in FILL:
        d=sum((PAL[3*i+k]-rgb[k])**2 for k in range(3))
        if best is None or d<best[0]: best=(d,i)
    return best[1]
def foot(x,y,DY=-1):
    nx0,ny0=s2n(x,y,DY); nx1,ny1=s2n(x+1,y+1,DY)
    for ny in range(int(np.floor(ny0)),int(np.ceil(ny1))):
        for nx in range(int(np.floor(nx0)),int(np.ceil(nx1))):
            w=(min(nx1,nx+1)-max(nx0,nx))*(min(ny1,ny+1)-max(ny0,ny))
            if w>0.01: yield w,ny,nx
def vul(x,y):
    c=Counter()
    for w,ny,nx in foot(x,y):
        if G[ny,nx] or WIT[ny,nx] or LUM[ny,nx]<52: continue
        c[nearest(N[ny,nx])]+=w
    return c.most_common(1)[0][0] if c else None
def bouw(r,pal):
    global PAL; PAL=pal
    a=r.copy()
    groen=np.isin(r,list(GR))
    KV=np.zeros((64,64),bool); KV[45:59,0:28]=True
    rnd=np.array([[r[y,x] in ({1}|set(FILL)) and (x==0 or 0 in nb4(r,y,x)) for x in range(64)] for y in range(64)])
    # binnenzone: ijzer in de koeienvanger, niet de buitenlijn, niet zwart dat groen raakt (grijns-/kierrand)
    g4=np.array([[any(v in GR for v in nb4(r,y,x)) for x in range(64)] for y in range(64)])
    zone=KV&np.isin(r,[1]+FILL)&~rnd
    rand_groen=zone&(r==1)&g4
    # V-lijn ligt over de band: de band (roest) zit tussen groen en V-lijn
    vcells=dun(raster(V))
    lijn=set(c for c in vcells)
    for k,pl in NADEN.items(): lijn|=set(dun(raster(pl)))
    groef=set()
    for k,pl in GROEVEN.items(): groef|=set(dun(raster(pl)))
    vmin={}
    for (y,x) in vcells: vmin[x]=min(vmin.get(x,99),y)
    for y,x in zip(*np.where(zone)):
        if rand_groen[y,x]: continue
        if (y,x) in lijn: a[y,x]=1; continue
        if x in vmin and y<vmin[x]: a[y,x]=9; continue          # band boven de V-lijn
        if (y,x) in groef: a[y,x]=12; continue
        v=vul(x,y); a[y,x]=v if v is not None else 11
    return a,zone,lijn,groef,vcells

RUSTM=(N[...,0]-N[...,2]>45)&~G&~WIT&(LUM>=52)
IJZM=~G&~WIT&(LUM>=52)
def frac(M,x,y,Ref=None):
    f=[(w,ny,nx) for w,ny,nx in foot(x,y) if (Ref is None or Ref[ny,nx])]; W=sum(w for w,_,_ in f)
    return sum(w for w,ny,nx in f if M[ny,nx])/W if W else 0
def mlum(x,y):
    f=[(w,ny,nx) for w,ny,nx in foot(x,y) if IJZM[ny,nx]]; W=sum(w for w,_,_ in f)
    return sum(w*LUM[ny,nx] for w,ny,nx in f)/W if W else None
def comps(cells):
    cells=set(cells); out=[]
    while cells:
        s=[cells.pop()]; c=list(s)
        while s:
            y,x=s.pop()
            for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                q=(y+dy,x+dx)
                if q in cells: cells.remove(q); s.append(q); c.append(q)
        out.append(c)
    return out
def bouw2(r,pal,nroest=3):
    global PAL; PAL=pal
    a=r.copy()
    KV=np.zeros((64,64),bool); KV[45:59,0:28]=True
    rnd=np.array([[r[y,x] in ({1}|set(FILL)) and (x==0 or 0 in nb4(r,y,x)) for x in range(64)] for y in range(64)])
    g4=np.array([[any(v in GR for v in nb4(r,y,x)) for x in range(64)] for y in range(64)])
    zone=KV&np.isin(r,[1]+FILL)&~rnd
    rand_groen=zone&(r==1)&g4
    vcells=[c for c in dun(raster(V)) if KV[c]]
    vset=set(vcells)
    naad=set()
    for k,pl in NADEN.items(): naad|=set(dun(raster(pl)))
    lijn=vset|naad
    groef=set()
    for k,pl in GROEVEN.items(): groef|=set(dun(raster(pl)))
    vmin={}
    for (y,x) in vcells: vmin[x]=min(vmin.get(x,99),y)
    plaat=[]
    for y,x in zip(*np.where(zone)):
        if rand_groen[y,x]: continue
        if (y,x) in lijn: a[y,x]=1; continue
        if x in vmin and y<vmin[x]:
            a[y,x]=8 if (mlum(x,y) or 0)>100 and frac(RUSTM,x,y,IJZM)>0.5 else 9; continue
        plaat.append((y,x))
    # roest: cellen met >=50% roest in het model, alleen de nroest grootste vlekken (>=3 px)
    rc=[(y,x) for y,x in plaat if frac(RUSTM,x,y,IJZM)>=0.5]
    vl=sorted([c for c in comps(rc) if len(c)>=3],key=len,reverse=True)[:nroest]
    roest=set(p for c in vl for p in c)
    for y,x in plaat:
        L=mlum(x,y) or 100
        lijnrechts=(ok(y,x+1) and ((y,x+1) in lijn or rnd[y,x+1]) and not (ok(y,x+1) and r[y,x+1] in GR))
        if (y,x) in roest: a[y,x]=8 if L>=100 else 9
        elif rnd[y,x-1] and x<=6: a[y,x]=7                       # lichte wig aan de lichtkant
        elif (y-1,x) in vset or ((y-1,x-1) in vset and (y-1,x) not in lijn and a[y-1,x]!=9): a[y,x]=7 if L>150 else 10   # lichte schuine bovenrand
        elif (y,x) in groef: a[y,x]=12
        else:
            v=vul(x,y)                                           # meerderheid dichtstbijzijnde paletkleur in het model
            if v in RUST or v is None: v=10 if L>135 else (11 if L>80 else 12)   # roest alleen in de gekozen vlekken
            a[y,x]=v
    return a,zone,lijn,groef,vcells,roest
