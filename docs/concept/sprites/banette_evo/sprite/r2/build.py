# Volgorde: python3 build.py (r1.npy -> cur.npy + banette_evo.png, drukt pixels per zone af) -> python3 vel.py cur.npy vel.png; controle: python3 controle.py cur.npy
# Meetgereedschap: zie.py (sprite|model met rooster), cls.py / fijn.py / cov.py (modelklassen per spritepixel), draadpos.py (draadposities), shupmask.py (Shuppet-silhouetten), dump.py
# Banette-evolutie r2: verder op r1 (r1.npy = r1/cur.npy). Per benoemde reparatie een zone; vormen en plekken uit het model
# (raster.py / fijn.py / cov.py), tinten naar Gen 3. Volgorde: python3 build.py -> cur.npy, banette_evo.png; vel.py cur.npy vel.png
import numpy as np
from matplotlib.path import Path
g=np.load('r1.npy').copy(); r1=g.copy()
LOG={}
def put(name,pts):
    n=0
    for (x,y),v in pts:
        if not(0<=x<64 and 0<=y<64): continue
        if g[y,x]!=v: n+=1
        g[y,x]=v
    LOG[name]=LOG.get(name,0)+n
def grid(name,x0,y0,rows,key):
    pts=[]
    for dy,row in enumerate(rows):
        for dx,ch in enumerate(row):
            if ch in ' _': continue
            pts.append(((x0+dx,y0+dy),key[ch]))
    put(name,pts)
def seg(p,a,b):
    p,a,b=map(np.array,(p,a,b)); t=np.clip(np.dot(p-a,b-a)/np.dot(b-a,b-a),0,1); return np.linalg.norm(p-(a+t*(b-a)))
def cov(fn,box,ss=6):
    x0,y0,x1,y1=box; c=np.zeros((64,64))
    for j in range(y0,y1):
        for i in range(x0,x1):
            n=0
            for a in range(ss):
                for b in range(ss):
                    n+=fn(i+(a+.5)/ss,j+(b+.5)/ss)
            c[j,i]=n/ss/ss
    return c
K=1; GL,GM,GD=2,3,4; RING,RM,RD,MOND,GEEL=5,6,7,8,9; BL,BM,BD,WIT,NAV,RL=10,11,12,13,14,15
ROOD={RING,RM,RD,RL}

# ===== 0. zones leegmaken (kruizen, armen, bellen, draden, Shuppets worden opnieuw opgebouwd) =====
pts=[]
for j in range(64):
    for i in range(64):
        v=g[j,i]
        if v==0: continue
        L=(i<=9 and 15<=j<=25) or (i<=6 and 15<=j<=36) or (i<=14 and 37<=j<=58) or (i<=9 and 16<=j<=42) or (10<=i<=12 and 25<=j<=42)
        R=(i>=46 and j>=13 and v not in ROOD) or (i==45 and 13<=j<=33 and v not in ROOD)
        if L or R: pts.append(((i,j),0))
put('leeg',pts)

# ===== 2. kruizen: twee balken (hartlijnen gemeten op het model), bovenvlak licht, dikte (onderzijde) donker, zwarte omlijning =====
def kruis(naam,bars,w,dik,box,clip=lambda i,j:True,achter=()):
    top=cov(lambda x,y:any(seg((x,y),a,b)<=w/2 for a,b in bars),box)
    zij=cov(lambda x,y:any(seg((x,y-dik),a,b)<=w/2 for a,b in bars),box)
    m=(np.maximum(top,zij)>=0.5)
    for j in range(64):
        for i in range(64):
            if m[j,i] and not clip(i,j): m[j,i]=False
    P=np.pad(m,1); pts=[]
    for j,i in zip(*np.where(m)):
        if g[j,i] in achter: continue
        rand=not(P[j,i+1] and P[j+2,i+1] and P[j+1,i] and P[j+1,i+2])
        if rand: v=K
        elif top[j,i]>=0.5 and top[j+1,i]>=0.5: v=GL
        elif top[j,i]>=0.5: v=GM
        else: v=GD
        pts.append(((i,j),v))
    put(naam,pts); return m

# ===== generieke Gen 3-tinten voor een rond deel: licht linksboven, schaduwsikkel rechtsonder, omlijning (selout lichtkant) =====
from scipy import ndimage as nd
def tinten(m,licht,mid,donker,sel,tl=0.10,td=0.07,sig=1.6,achter=None):
    bl=nd.gaussian_filter(m.astype(float),sig); gy,gx=np.gradient(bl)
    out={}
    P=np.pad(m,1)
    for j,i in zip(*np.where(m)):
        u,d,l,r=not P[j,i+1],not P[j+2,i+1],not P[j+1,i],not P[j+1,i+2]
        nx,ny=-gx[j,i],-gy[j,i]
        s=(-nx-ny)/1.414
        if u or d or l or r:
            out[(i,j)]=sel if (s>0.02 and not (d or r)) or ((u or l) and not (d or r)) else K
        elif s>tl: out[(i,j)]=licht
        elif s<-td: out[(i,j)]=donker
        else: out[(i,j)]=mid
    return out

# ===== 6. Shuppets: silhouet = model, kop vóór lijf, armpjes met eigen omlijning, tinten Gen 3, ogen uit het model =====
from shupgeo import SH
def shuppet(z):
    d=SH[z]; box=d['box']
    sil=np.load('shup_%s.npy'%z)>=0.5
    sil|=cov(d['hoorn'],box)>=0.5
    rest=sil.copy(); delen=[]
    for naam,fs in d['delen']:
        m=sil&(cov(lambda x,y:any(f(x,y) for f in fs),box)>=0.5); delen.append((naam,m))
    alle=np.zeros_like(sil)
    for n,m in delen: alle|=m
    romp=sil&~alle
    # romp loopt achter alle delen door: masker = romp + delen die erop liggen (zodat de romp geen eigen lijn onder een arm krijgt)
    for naam,m in [('romp',romp|alle&~delen[-1][1])]+delen:
        o=tinten(m,BL,BM,BD,NAV); put('shuppet_'+z+'_'+naam,list(o.items()))
    return sil

# ===== 3. armen: polygonen uit het model (cls.py 42 11 64 34); lichte buitenkant, donkere strook aan de binnenkant =====
def poly(pts,box=(0,0,64,64)):
    P=Path(pts); return cov(lambda x,y:P.contains_point((x,y)),box,ss=4)>=0.5
def arm(naam,m,vouw,leeg_only=False):
    # vouw(j) = eerste kolom van de donkere strook in rij j
    P=np.pad(m,1); pts=[]
    for j,i in zip(*np.where(m)):
        if leeg_only and g[j,i]!=0: continue
        u,d,l,r=not P[j,i+1],not P[j+2,i+1],not P[j+1,i],not P[j+1,i+2]
        if l and not d: v=GD                    # lichtkant: selout
        elif u or d or l or r: v=K
        elif i>=vouw(j): v=GD
        elif l is False and not P[j+1,i-1+1-1]: v=GL
        else: v=GL if (not P[j+1,i-1] or not P[j+1,i]) else GM
        pts.append(((i,j),v))
    put(naam,pts)
AR=poly([(48.3,16.6),(49.9,16.6),(50.6,18.5),(51.0,22.0),(51.6,25.5),(51.4,28.2),(49.6,29.8),(48.0,31.6),(46.6,33.2),(45.4,34.4),(45.0,34.4),
         (45.2,31.0),(45.8,28.0),(46.3,25.0),(46.6,22.0),(47.2,19.4)],(44,15,53,36))
# r1 had het rode hoofd tot x 44 (rij 22-33); arm ligt erachter: alleen waar het hoofd niet is
for j in range(64):
    for i in range(64):
        if AR[j,i] and g[j,i] in ROOD|{K} and i<=45: AR[j,i]=False
arm('arm_rechts',AR,lambda j:49 if j<=23 else (48 if j<=28 else 47))
KR=kruis('kruis_rechts',[((50.8,26.2),(60.6,17.4)),((52.3,17.6),(62.2,25.2))],3.1,1.1,(46,13,64,30))

# ===== 3b. links: mutspunt (cls.py 0 22 15 40) en linkerarm die erachter vandaan naar het kruis loopt =====
KEY={'k':K,'m':GM,'d':GD,'l':GL,'w':WIT,'.':0}
grid('mutspunt_links',7,25,[
 "kmmdddk",
 "kmmdddk",
 "kmmddkk",
 "kmmdkdk",
 "kmdkkkk",
 "kmdk..k",
 "kmdk..k",
 "kdk___k",
 ],KEY)
# kruis links: hartlijnen gemeten op het model (zie.py 0 14 18 40), loopt achter de muts (x >= 10) door
# kruis links: per pixel op de modelvorm (zie.py 0 14 18 40: tippen UL (4,4;18,5), LL (0,9;25,5), UR achter de muts;
# inkepingen boven (7,6;20,4), links (5,2;21,8), onder (6,8;24,3)); bovenvlak licht, onderzijde donker, zwarte rand
grid('kruis_links',0,17,[
 "...kk....k",
 "..kllk..kl",
 "..kmllk.kl",
 "...kmllkll",
 "....kmllld",
 "...kkllmmd",
 "..klllllmd",
 "kkllmmmddd",
 "klmddkkkkk",
 "kddk______",
 "kkk_______",
 ],KEY)
# muts-rand naast het kruis: één zwarte lijn (kruis ligt erachter)
put('muts_rand',[((10,j),K) for j in range(17,25)])
# linkerarm: spiegeling van de rechterarm (selout, licht, mid), komt onder het kruis uit en gaat achter de mutspunt
grid('arm_links',3,26,[
 "_dll",
 "_dlm",
 "_dlm",
 "_dlm",
 "_klm",
 "__kk",
 ],KEY)
# ===== 4. bellen: één sjabloon, rond, los van het kruis (zwarte rand rondom); hangen vóór kruis, arm en draden =====
BEL=["_kkkk_",
     "kwwllk",
     "kwllmk",
     "klkkmk",
     "kmdkdk",
     "_kkkk_"]
grid('bel_links',5,33,BEL,KEY)
grid('bel_rechts',49,17,BEL,KEY)
# rode mutspunt rechts: de krul eindigt op het belletje (fijn.py 38 4 55 18)
RK={'k':K,'r':RM,'R':RD,'.':0,'h':RL}
grid('krul_rechts',43,13,[
 "_kk..krrRk",
 "k.....krRk",
 "k......krRk",
 "k......krRk",
 "_______kk__",
 ],RK)


# ===== 5. ogen: uit het model (zie.py/cls.py 14 23 38 33): zwarte oogkas, donkere kas, rode ring, gele iris, zwarte spleet =====
OK={'k':K,'D':MOND,'O':RING,'Y':GEEL}
grid('oog_links',15,25,[
 "k____k__",
 "_kkkkDk_",
 "_kDOODk_",
 "_kOYkOk_",
 "_kOYkODk",
 "_kDOODDk",
 "__kkkkkk"],OK)
grid('oog_rechts',26,23,[
 "__________k",
 "___kkkkkkkk",
 "___kDOODDDk",
 "___kOYkODk_",
 "__kDOYkODk_",
 "_kDDOYkODk_",
 "kDDDDOODDk_",
 "kkkkkkkkkk_"],OK)

# ===== 6b. mond: zigzag als polygoon over de modelranden (3 boventanden, 3 ondertanden), zwarte omlijning, donkere binnenkant =====
# hoekpunten op het model (zie.py 12 30 46 46); tandpunten iets doorgetrokken zodat ze na het rasteren een scherpe punt houden
MP=[(14.8,33.0),(16.4,35.2),(18.5,38.8),(20.4,35.8),(21.4,35.8),(24.0,40.0),(25.9,35.9),(30.0,39.4),(33.2,33.6),(34.2,33.2),
    (35.4,33.9),(37.8,33.9),(39.6,31.6),(41.6,27.9),(42.6,26.6),(43.4,27.2),(43.0,30.9),(41.4,35.2),(39.6,38.7),(38.6,40.0),
    (37.0,39.4),(34.6,36.4),(32.6,40.8),(31.0,42.2),(28.5,39.0),(26.2,43.0),(24.6,43.9),(23.2,42.6),(21.5,38.7),(19.6,42.0),
    (17.4,41.0),(15.6,38.2),(14.6,34.4)]
MM=poly(MP,(12,24,46,46))
HUID={2,3,4,6,7,15}
pts=[]
for j in range(28,46):
    for i in range(13,45):
        if MM[j,i] or r1[j,i] not in (MOND,K): continue
        if j<=31 and i<=37: continue      # ogen
        # oude mondpixel buiten de nieuwe mond: huid van de buren in r1
        nb=[r1[y,x] for y in range(j-2,j+3) for x in range(i-2,i+3) if r1[y,x] in HUID]
        P=np.pad(r1>0,1)
        if nb and P[j,i+1] and P[j+2,i+1] and P[j+1,i] and P[j+1,i+2] and not (r1[j,i]==K and sum(r1[y,x]==0 for y in range(j-1,j+2) for x in range(i-1,i+2))):
            pts.append(((i,j),max(set(nb),key=nb.count)))
put('mond_terug',pts)
P=np.pad(MM,1); pts=[]
for j,i in zip(*np.where(MM)):
    rand=not(P[j,i+1] and P[j+2,i+1] and P[j+1,i] and P[j+1,i+2])
    pts.append(((i,j),K if rand else MOND))
put('mond',pts)
# Shuppets
# Shuppets: per pixel op het modelsilhouet (shupmask.py, dekking >= 0,5; kop rond met hoorn, armpjes, voetje),
# stijl en oog van de Gen 3 Shuppet (zwarte rand schaduwkant, marine selout lichtkant, lichtblauw oog met donkere pupil)
SK={'k':K,'n':NAV,'L':BL,'M':BM,'D':BD,'W':WIT,'N':NAV,'.':0}
grid('shuppet_L',3,38,[
#  3456789012345
 "____nk_______",   # 38 hoorn
 "____nLk______",   # 39
 "____nLk______",   # 40
 "___nLMMkk____",   # 41
 "__nLLMMMMkk__",   # 42
 "__nLLMMMMMk__",   # 43
 "__nLMMMMMMDk_",   # 44
 "_nkLMMMkkMDk_",   # 45
 "_kWkMMkWNkDk_",   # 46
 "_kkMMMkWNkDk_",   # 47
 "__kMMMMkkDk__",   # 48
 "___kkkkkkk___",   # 49
 "_____kDDknnk_",   # 50
 "____nMMMkLMMk",   # 51
 "___nLDMMkMMDk",   # 52
 "____kMMMkMDDk",   # 53
 "____kMMDDkkkk",   # 54
 "_____kDDDk___",   # 55
 "_______kkk___",   # 56
 ],SK)
grid('shuppet_R',46,42,[
#  678901234567890
 "______k________",   # 42 hoorn
 "_____nk________",   # 43
 "_____nLk_______",   # 44
 "_____nLk_______",   # 45
 "____nLMk_______",   # 46
 "____nLMMkk_____",   # 47
 "___nLLMMMMk____",   # 48
 "__nLLMkkkkDk___",   # 49
 "__nkLkWWNWkDk__",   # 50
 "_kWkMkWWNWkDk__",   # 51
 "__kkMMkkkkDk___",   # 52
 "__kMMMMMDDk____",   # 53
 "___kDDDDDk_____",   # 54
 "____kkkkkk_____",   # 55
 "___nnkDDDDnk___",   # 56
 "__nLMkMMMDkMk__",   # 57
 "__kkk.nMMDDkDk_",   # 58
 "______nMDDDkk__",   # 59
 "_____kMMDDDDk__",   # 60
 "_____kkk.kkkk__",   # 61
 ],SK)
# ===== 7. kraag, rode punt en grijs stompje onder de kin: vormen uit het model (cls.py 20 38 48 58), nette lijnen =====
# k zwart, d kraag/stomp donker, g stomp mid, l stomp licht, r rood, R rood donker, . leeg
CK={'k':K,'d':GD,'g':GM,'l':GL,'r':RM,'R':RD,'h':RL,'.':0}
RIJEN={
 46:[(24,25,'.'),(26,32,'k'),(33,37,'r'),(38,40,'R'),(41,41,'k'),(42,44,'.')],
 47:[(24,24,'.'),(25,25,'k'),(26,31,'d'),(32,32,'k'),(33,35,'r'),(36,36,'R'),(37,41,'k'),(42,44,'.')],
 48:[(24,25,'.'),(26,26,'k'),(27,27,'d'),(28,28,'k'),(29,31,'d'),(32,32,'k'),(33,35,'r'),(36,36,'R'),(37,37,'k'),(38,39,'g'),(40,40,'k'),(41,44,'.')],
 49:[(24,26,'.'),(27,27,'k'),(28,28,'.'),(29,32,'k'),(33,33,'k'),(34,34,'r'),(35,35,'R'),(36,36,'k'),(37,38,'g'),(39,40,'d'),(41,41,'k'),(42,44,'.')],
 50:[(24,28,'.'),(29,29,'k'),(30,31,'l'),(32,32,'g'),(33,33,'k'),(34,34,'r'),(35,35,'R'),(36,36,'k'),(37,37,'g'),(38,41,'d'),(42,42,'k'),(43,44,'.')],
 51:[(24,28,'.'),(29,29,'k'),(30,30,'l'),(31,33,'g'),(34,35,'k'),(36,37,'g'),(38,41,'d'),(42,42,'k'),(43,44,'.')],
 52:[(24,28,'.'),(29,29,'k'),(30,30,'l'),(31,36,'g'),(37,42,'d'),(43,43,'k'),(44,44,'.')],
 53:[(24,28,'.'),(29,29,'k'),(30,35,'g'),(36,42,'d'),(43,43,'k'),(44,44,'.')],
 54:[(24,28,'.'),(29,29,'k'),(30,31,'g'),(32,42,'d'),(43,43,'k'),(44,44,'.')],
 55:[(24,29,'.'),(30,32,'k'),(33,38,'d'),(39,39,'k'),(40,42,'d'),(43,43,'k'),(44,44,'.')],
 56:[(24,32,'.'),(33,33,'k'),(34,37,'d'),(38,38,'k'),(39,39,'.'),(40,42,'k'),(43,44,'.')],
 57:[(24,33,'.'),(34,37,'k'),(38,44,'.')],
}
pts=[]
for j,rr in RIJEN.items():
    for a,b,c in rr:
        for x in range(a,b+1): pts.append(((x,j),CK[c]))
put('kraag_punt_stomp',pts)

# ===== 8. grijze muts: Gen 3-licht als vlek linksboven (geen band langs de rand), naad grijs/rood als nette donkere lijn =====
pts=[]
for j in range(8,18):
    for i in range(10,26):
        if g[j,i] in (GL,GM):
            pts.append(((i,j),GL if ((i-15.0)/4.6)**2+((j-11.2)/2.7)**2<=1 else GM))
put('muts_licht',pts)
NAAD={}
pts=[]
for j in range(12,37):
    xs=[i for i in range(16,32) if g[j,i] in (RM,RD,RL) and g[j,i-1] in (GL,GM,GD)]
    if not xs: continue
    s0=xs[0]; NAAD[j]=s0
    pts.append(((s0-1,j),GD))
    if g[j,s0-2]==GD and j>=17 and g[j,s0-3] in (GM,GL): pts.append(((s0-2,j),GM))   # geen dubbele donkere strook
put('naad',pts)
# ===== 9. steken: twee korte steken dwars over de naad (model: rij 17,4 en 22,3) =====
put('steken',[((NAAD[17]-2,17),K),((NAAD[17]-1,17),K),((NAAD[17],17),K),((NAAD[22]-2,22),K),((NAAD[22]-1,22),K),((NAAD[22],22),K)])
# ===== 10. ruis: tintvlakjes < 3 px (8-buren) in grijs/rood nemen de buurtint aan (niet in bellen, ogen, steken) =====
VRIJ=set()
for x0,y0 in ((5,33),(49,17)):
    for y in range(y0,y0+6):
        for x in range(x0,x0+6): VRIJ.add((x,y))
for ronde in range(2):
    pts=[]
    for c in (GL,GM,GD,RM,RD,RL):
        lab,n=nd.label(g==c,structure=np.ones((3,3)))
        for k in range(1,n+1):
            m=lab==k
            if m.sum()>=3: continue
            for j,i in zip(*np.where(m)):
                if (i,j) in VRIJ: continue
                nb=[g[y,x] for x in range(i-1,i+2) for y in range(j-1,j+2) if (x,y)!=(i,j) and 0<=x<64 and 0<=y<64]
                cand=[v for v in nb if v in (GL,GM,GD,RM,RD,RL) and v!=c and (v in (RM,RD,RL))==(c in (RM,RD,RL))]
                if cand: pts.append(((i,j),max(set(cand),key=cand.count)))
    put('ruis',pts)

# ===== 1. draden: één doorlopende 1 px lijn per draad in één kleur (NAV), plek per rij uit het model (draadpos.py),
#           min. 1 px lucht tussen draden; alleen op lege pixels (achter alles), omhoog doorgetrokken tot het kruis =====
DRAAD=NAV
def draad(naam,segs):
    # segs: [(x, rij_van, rij_tot)], doorlopend van boven naar onder
    pts=[]
    x0,j0,_=segs[0]
    j=j0-1
    while j>0 and g[j,x0]==0: pts.append(((x0,j),DRAAD)); j-=1
    for x,a,b in segs:
        for j in range(a,b+1):
            if g[j,x]==0: pts.append(((x,j),DRAAD))
    put(naam,pts)
# links (kruis links -> Shuppet links)
draad('draad_L1',[(2,27,31),(3,32,37),(4,38,40),(5,41,41)])     # model 2,6 -> 5,0 ; eindigt op de kop
draad('draad_L3',[(11,30,32)])                                    # model 11,8 (tussen mutspunt en lijf)
draad('draad_L3b',[(11,36,41)])                                   # model 11,9-12,0 onder de bel -> kop
draad('draad_L4',[(13,35,49)])                                    # model 13,7 -> arm rechts van de Shuppet
# rechts (kruis rechts -> Shuppet rechts)
draad('draad_R1',[(50,29,46)])                                    # model 50,1 -> kop
draad('draad_R2',[(52,28,42)])                                    # model 51,9-52,5 -> hoorn
draad('draad_R3',[(57,27,36),(56,37,40)])                         # model 58,2 -> 56,7 (kort, hangt los); 1 px naar links voor lucht
draad('draad_R4',[(59,27,40),(58,41,46),(57,47,47)])              # model 59,5 -> 57,3 -> kop
draad('draad_R5',[(61,27,34),(60,35,46),(59,47,51),(58,52,55)])   # model 61,4 -> 58,4 -> arm
np.save('cur.npy',g)
np.save('cur.npy',g)
from view import png
png(g,'banette_evo.png')
if __name__=='__main__':
    print(LOG)
    kaal=np.load('../r1/kaal.npy')
    zones={'hoofd/muts (x13-44,y4-46)':(13,4,45,47),'kruis+arm+bel links (x0-12,y15-40)':(0,15,13,41),'kruis+arm+bel rechts (x44-63,y11-36)':(44,11,64,37),
           'Shuppet links (x0-16,y37-58)':(0,37,17,59),'Shuppet rechts (x44-63,y40-63)':(44,40,64,64),'kraag/punt/stomp (x22-44,y46-58)':(22,46,45,59)}
    for n,(x0,y0,x1,y1) in zones.items():
        a=g[y0:y1,x0:x1]; print('%-40s anders dan r1: %4d   anders dan kale reductie: %4d'%(n,(a!=r1[y0:y1,x0:x1]).sum(),(a!=kaal[y0:y1,x0:x1]).sum()))
