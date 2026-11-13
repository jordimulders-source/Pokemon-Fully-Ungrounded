# maak_r3.py: regionale Abra r3. Gebruik (vanuit kleur_r3/): python3 maak_r3.py
# Uitgangspunt r2 (silhouet bevroren, kop bevroren). Onderhelft opnieuw uit het model (../kleur_r1/natief.png):
#  1. modelpixels -> klasse (K, platen 1/2/3, huid s/b/h); m (AA-overgang) en geisoleerde modelpixels nemen de buurtklasse aan
#  2. binnenlijn alleen waar het model een echte lijn heeft: blok met >=2 zwarte modelpixels; 1 zwarte alleen als brug; verdund tot 1 px
#  3. vulling = meerderheid in het blok; daarna per lichaamsdeel (gebied tussen lijnen) een meerderheidsfilter -> rustige banden
#     (vlekjes die het model echt heeft blijven: >=3/4 modelpixels in die tint)
#  4. lijnkleur: lichtkant buitenrand L, schaduwkant K, binnenlijn op huid L, tegen platen K; bovenrand staart T (lichte selout)
#  5. handwerk als data (EDITS), elk met reden in LOG.md
import sys; sys.path.insert(0,'../kleur_r2')
import numpy as np; from PIL import Image
from auto import PAL,NAAM,K,L,P1,P2,P3,S2,S,M,B,H,nlum,nbg,ndrk
from lijnen import verdun
T=S2; PAL=list(PAL); PAL[T]=(104,98,126)   # idx 6 (was ongebruikt 'd'): lichte selout waar het model aan de lichtkant geen zwarte rand heeft (bovenrand staart, bovenkant voet)
I=11; PAL.append((92,86,114))             # binnenlijn op de huid: donkere huidtint i.p.v. de omlijningskleur
NAAM=dict(NAAM); NAAM[T]='T'; NAAM[I]='I'; CH={v:k for k,v in NAAM.items()}
r2=np.array(Image.open('../kleur_r2/abra_r2.png')).astype(int)
fig=r2>0; Hh,Ww=fig.shape
# kop bevroren uit r2: per rij de hoogste x van de kop (tot en met zijn rechterlijn)
KOP={15:40,16:40,17:40,18:40,19:40,20:40,21:40,22:40,23:40,24:40,25:39,26:38,27:39,28:38,29:36,30:35,31:33,32:31,33:30,34:30,35:29,36:28}
kop=np.zeros_like(fig)
for y,x1 in KOP.items(): kop[y,:x1+1]=True
kop&=fig
# 1. modelklassen
def kl(l):
    for th,c in ((35,K),(60,P1),(80,P2),(102,P3),(146,S),(170,M),(195,B)):
        if l<th: return c
    return H
NH,NW=nlum.shape
nk=np.zeros((NH,NW),int)
for y in range(NH):
    for x in range(NW):
        nk[y,x]=0 if nbg[y,x] else kl(nlum[y,x])
def glad_natief(nk):
    o=nk.copy()
    for it in range(2):
        for y in range(1,NH-1):
            for x in range(1,NW-1):
                v=o[y,x]
                if v in (0,K): continue
                nb=[o[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and o[y+dy,x+dx] not in(0,K)]
                if not nb: continue
                same=sum(n==v for n in nb)
                if v==M or same==0:
                    c=[n for n in nb if n!=M]
                    if c: vv,cc=np.unique(c,return_counts=True); o[y,x]=vv[cc.argmax()]
    return o
nk2=glad_natief(nk)
def blok(x,y): return (slice(2*y-14,2*y-12),slice(2*x-1,2*x+1))
ndk=np.zeros((64,64),int)
for y in range(7,64):
    for x in range(1,64):
        sl=blok(x,y)
        if sl[0].stop<=NH and sl[1].stop<=NW: ndk[y,x]=ndrk[sl].sum()
def erode4(m):
    p=np.pad(m,1); return m&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
rand=fig&~erode4(fig)
def ncomp8(w):
    seen=np.zeros_like(w); n=0
    for y,x in zip(*np.where(w)):
        if seen[y,x]: continue
        n+=1; st=[(y,x)]; seen[y,x]=True
        while st:
            cy,cx=st.pop()
            for dy in(-1,0,1):
                for dx in(-1,0,1):
                    yy,xx=cy+dy,cx+dx
                    if 0<=yy<w.shape[0] and 0<=xx<w.shape[1] and w[yy,xx] and not seen[yy,xx]: seen[yy,xx]=True; st.append((yy,xx))
    return n
# 2. binnenlijnen
lijn=fig&(rand|(ndk>=2))
for it in range(3):
    add=[]
    for y,x in zip(*np.where(fig&~lijn&(ndk==1))):
        w=lijn[y-1:y+2,x-1:x+2].copy(); w[1,1]=False
        if ncomp8(w)>=2: add.append((y,x))
    for p in add: lijn[p]=True
    if not add: break
lijn=verdun(lijn,rand,ndk)
for y,x in zip(*np.where(lijn&~rand)):
    if lijn[y-1:y+2,x-1:x+2].sum()==1: lijn[y,x]=False
# 3. vulling
o=np.zeros((Hh,Ww),int)
def vul(x,y):
    sl=blok(x,y); c=[v for v in nk2[sl].ravel() if v not in(0,K)]
    if not c:
        w=nk2[max(0,2*y-15):2*y-11,max(0,2*x-2):2*x+2].ravel(); c=[v for v in w if v not in(0,K)] or [S]
    vv,cc=np.unique(c,return_counts=True); best=vv[cc==cc.max()]
    if len(best)>1:   # gelijkspel: de klasse die in de ruimere omgeving (4x4 rond het blok) het meest voorkomt
        w=nk2[max(0,2*y-15):2*y-11,max(0,2*x-2):2*x+2].ravel(); best=max(best,key=lambda v:(w==v).sum())
    else: best=best[0]
    return best
for y,x in zip(*np.where(fig)):
    o[y,x]=K if lijn[y,x] else vul(x,y)
# echte modelvlek: >=3 van de 4 modelpixels (ongeglad) in die tint
def echt(y,x,v):
    sl=blok(x,y); return (nk[sl]==v).sum()>=3
def gebieden(o):
    lab=np.zeros_like(o); n=0
    for y0,x0 in zip(*np.where(o>=P1)):
        if lab[y0,x0]: continue
        n+=1; st=[(y0,x0)]; lab[y0,x0]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<Hh and 0<=xx<Ww and not lab[yy,xx] and o[yy,xx]>=P1: lab[yy,xx]=n; st.append((yy,xx))
    return lab
def plaat(v): return P1<=v<=P3
# vlekjes en streepjes die het model echt heeft (lijst uit kleur_r2/LOG.md): blijven staan zolang het model ze ook in r3 bevestigt
VLEK=set([(12, 48), (16, 51), (17, 51), (17, 52), (18, 52), (19, 47), (19, 51), (20, 24), (20, 45), (20, 47), (20, 49), (21, 32), (21, 33), (21, 50), (21, 51), (21, 52), (22, 21), (22, 31), (22, 33), (22, 53), (24, 53), (25, 37), (25, 38), (25, 39), (26, 37), (26, 59), (29, 36), (30, 22), (30, 35), (31, 49), (32, 17), (32, 50), (33, 49), (33, 61), (34, 17), (34, 49), (34, 51), (36, 55), (39, 26), (39, 36), (39, 61), (40, 36), (40, 37), (40, 38), (40, 39), (40, 40), (41, 35), (41, 44), (41, 61), (42, 43), (42, 44), (42, 46), (42, 61), (43, 46), (43, 53), (44, 31), (44, 46), (44, 60), (45, 31), (45, 60), (45, 61), (47, 60), (48, 59), (49, 59), (50, 58), (51, 50), (52, 58), (53, 53), (53, 54), (53, 57)])
GLAD=1; MINCL=4   # meerderheidsfilter: pixel met <=GLAD gelijke buren (in zijn gebied) neemt de meerderheid aan; clusters < MINCL px
gehouden=set()
for it in range(6):
    lab=gebieden(o); ch=0; new=o.copy()
    for y,x in zip(*np.where((o>=P1)&~kop)):
        v=o[y,x]
        nb=[o[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<Hh and 0<=x+dx<Ww and lab[y+dy,x+dx]==lab[y,x] and plaat(o[y+dy,x+dx])==plaat(v)]
        if len(nb)<3: continue
        same=sum(n==v for n in nb)
        vv,cc=np.unique([n for n in nb if n!=v] or [v],return_counts=True); maj=vv[cc.argmax()]
        if maj!=v and same<=GLAD and cc.max()>=GLAD+2:
            if echt(y,x,v) and same>=1 and (x,y) in VLEK: gehouden.add((x,y)); continue
            new[y,x]=maj; ch+=1
    o=new
    # kleine clusters (< 4 px, 4-buren) binnen hetzelfde gebied: buurtint, tenzij een echte modelvlek
    lab=gebieden(o); seen=np.zeros_like(fig)
    for y0,x0 in zip(*np.where((o>=P1)&~kop)):
        if seen[y0,x0]: continue
        v=o[y0,x0]; comp=[(y0,x0)]; seen[y0,x0]=True; k=0
        while k<len(comp):
            cy,cx=comp[k]; k+=1
            for dy,dx in((0,1),(1,0),(0,-1),(-1,0)):
                yy,xx=cy+dy,cx+dx
                if 0<=yy<Hh and 0<=xx<Ww and not seen[yy,xx] and o[yy,xx]==v and not kop[yy,xx]: seen[yy,xx]=True; comp.append((yy,xx))
        if len(comp)>=MINCL: continue
        if all(echt(cy,cx,v) and (cx,cy) in VLEK for cy,cx in comp):
            for q in comp: gehouden.add((q[1],q[0]))
            continue
        nb=[o[cy+dy,cx+dx] for cy,cx in comp for dy,dx in((0,1),(1,0),(0,-1),(-1,0)) if 0<=cy+dy<Hh and 0<=cx+dx<Ww and o[cy+dy,cx+dx]>=P1 and o[cy+dy,cx+dx]!=v and plaat(o[cy+dy,cx+dx])==plaat(v) and lab[cy+dy,cx+dx]==lab[cy,cx]]
        if nb:
            vv,cc=np.unique(nb,return_counts=True)
            for q in comp: o[q]=vv[cc.argmax()]
            ch+=1
    if not ch: break
# 4. lijnkleur
o2=o.copy()
for y,x in zip(*np.where(o==K)):
    n={nm:(o[y+dy,x+dx] if 0<=y+dy<Hh and 0<=x+dx<Ww else 0) for dy,dx,nm in((-1,0,'b'),(0,-1,'l'),(1,0,'o'),(0,1,'r'))}
    if any(P1<=v<=P2 for v in n.values()): continue
    if n['o']==0 or n['r']==0: continue
    if n['b']==0 or n['l']==0: o2[y,x]=T if (ndk[y,x]==0 and not kop[y,x]) else L; continue
    vul_=[v for v in n.values() if v>=P3]
    if vul_ and max(vul_)>=S: o2[y,x]=L if (rand[y,x] or kop[y,x]) else I
o=o2
o[kop]=r2[kop]
# romp en schouders (y < 40) bevroren uit r2: geen opdracht, en de gladfilter verloor daar modeltonen (plaat 1, armlicht b)
romp=fig&~kop&(np.arange(Hh)[:,None]<40)
o[romp]=r2[romp]

# 5. onderhelft per lichaamsdeel, per spritepixel van het 2x2-modelblok gelezen (cel.py, mzoom.py), banden in plaats van losse pixels.
#    tekens: K zwart, L omlijning/hoofdlijn, I plooi (vinger/teen), T lichte selout, 1/2/3 plaat, s/m/b/h huid, '.' leeg, '_' = regelstap laten
RASTER=[  # (x0, y0, rijen)
 (8,40,"""
...............LssK..KK_
..............TsssK...._
..............ThssK...T_
.............LhhssK...T_
............LKhhssLLLL__
..........LL3KhhssLmmm__
..........L31KhhssLssm__
....TTT...LssLbbbbLsss__
..LThhhT..LbbLbbbbLsss__
.LhbIIsT..LbbLbbbbbLss__
KhKssssbTTbbLbbbbKKKKK__
.KKKKsssbbbsLbIbI..K.T__
.....KsssbsK.LIbsK...K__
......KsssK..KsKsK....__
.......KssK...KKKK....__
........KsK...........__
.......K2sK...........__
........KK............__"""),
 (29,41,"""
..LsssssKssKKKK...
.TsssssssssK22K...
.TbbsssshhsKssK...
LbbbbbshhssKssK...
sbbbbbhhssLsLLLK..
LsbbbhhsssLLsbbsLL
sLbsbhsssLsmmKKKsK
sLsbIsssLssmK3333K
sLbshssLssbbKK3331
KbIhhILhLbbbbsK111
TbIhIsshLbbbssK111
KbKIsIssLsssssK1KK
.K.LssILshLsss3KK.
..TssssLshKKKKK...
..TsssIssK........
.TssKKKKK.........
.TKK.............."""),
]
def raster(o):
    log=[]
    for x0,y0,rows in RASTER:
        for dy,r in enumerate(rows.strip('\n').split('\n')):
            for dx,c in enumerate(r):
                if c=='_': continue
                x,y=x0+dx,y0+dy; v=CH[c]
                if (v==0)!=(o[y,x]==0): raise SystemExit('silhouet wijkt af: %d,%d (%s)'%(x,y,c))
                if kop[y,x]: raise SystemExit('kop: %d,%d'%(x,y))
                if o[y,x]!=v: log.append(('raster',x,y,NAAM[o[y,x]],c)); o[y,x]=v
    return log
EDITS="""
# zone y x0 tekens ('_' = laten)
# staart: model (48-49,60) 'ss/KK' = lijn op de grens met rij 61 (al rand): geen tweede lijn erboven
st 60 48 ss
# staartonderkant: model 's' boven een lichte '3'-rand; de afwisseling s/3 was reductieruis
st 62 37 sssss
# rechterhand: losse plooipixel (33,48) wordt schaduw (model 'K1/bh': donker streepje, geen doorlopende lijn)
hr 48 33 s
"""
def edits(o):
    log=[]
    for r in EDITS.strip().splitlines():
        if r.startswith('#') or not r.strip(): continue
        z,y,x0,t=r.split(); y=int(y); x0=int(x0)
        for k,c in enumerate(t):
            if c=='_': continue
            x=x0+k; v=CH[c]
            if (v==0)!=(o[y,x]==0) : raise SystemExit('silhouet: %s %d,%d'%(z,x,y))
            if o[y,x]!=v: log.append((z,x,y,NAAM[o[y,x]],c)); o[y,x]=v
    return log
if __name__=='__main__':
    auto=o.copy(); log=raster(o)
    # 6. zwart alleen waar het moet: in de onderhelft wordt een binnenlijn zonder plaat ernaast L, en een randpixel die alleen
    #    naar boven/links open is (lichtkant) L; zwart blijft aan de schaduwkant (onder/rechts) en tegen de platen
    for y,x in zip(*np.where((o==K)&~kop)):
        if y<41: continue
        n={nm:(o[y+dy,x+dx] if 0<=y+dy<Hh and 0<=x+dx<Ww else 0) for dy,dx,nm in((-1,0,'b'),(0,-1,'l'),(1,0,'o'),(0,1,'r'))}
        if any(P1<=v<=P3 for v in n.values()): continue
        if n['o']==0 or n['r']==0: continue
        log.append(('zwart',x,y,'K','L')); o[y,x]=L
    log+=edits(o)
    im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette([v for c in PAL for v in c]+[0]*(768-3*len(PAL))); im.save('abra_r3.png',transparency=0)
    tot=(o>0).sum()
    print('kleuren',len(set(o.ravel()))-1,'| zwart %.1f%% | L %.1f%% | T %.1f%% | edits %d'%(100*(o==K).sum()/tot,100*(o==L).sum()/tot,100*(o==T).sum()/tot,len(log)))
    print('diff t.o.v. r2:',int((o!=r2).sum()))
    import json; json.dump({'gehouden':[[int(a),int(b)] for a,b in sorted(gehouden)],'edits':[[str(q) for q in e] for e in log]},open('_maak_r3.json','w'))
