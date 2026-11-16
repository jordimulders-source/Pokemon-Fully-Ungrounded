# Pitahaya-draak fase 2, r1: kale reductie (python3 half3.py kaal.png 0 2 2 2; fase gekozen op oog + tanden)
# -> alleen technische opschoning, elke stap met modelmeting. Niets getekend.
#  A LIJN DUNNER: 3x-reductie met 'donkerste wint' maakt dunne modellijnen 2 px dik (les fase 1: zwart binnen de
#    figuur 13,7 %, Gen 3 1-8 %). Binnenzwart dat naast een 'sterkere' zwarte buur ligt (meer zwarte modelpx in
#    het blok) en geen verbinding breekt -> vlaktint van zijn eigen blok (gemiddelde van de niet-zwarte modelpx).
#    Oog, tanden en lip bevroren.
#  B BUITENLIJN 1 px: zwart aan de schaduwkant (normaal onder/rechts), gekleurde selout aan de lichtkant
#    (roze -> donkerste roze 2, groen -> donkerste groen 6; beide modelkleuren).
#  T TOONKAART: binnenvulling roze en groen uit de gladde modelluminantie per groep (sigma 1,5), naar de
#    dichtstbijzijnde modeltoon; blokken met een echte modellijn/naad (>= 3 px lum < 62) blijven.
#  M BEK: vruchtvleespixels (blok >= 3 witte/pit-modelpx) krijgen de toon van hun blok (grijs/licht);
#    pitjes: modelpitten per blok (massa), sterkste eerst, geen twee pitjes 8-naast elkaar, niet op de vleesrand.
#  C RUIS: losse vulpixel (8-verbonden cluster van 1) -> meest voorkomende buurtint uit dezelfde kleurgroep.
import sys,numpy as np; from PIL import Image; from collections import Counter
from groepen import laad
K=Image.open('kaal.png'); kaal=np.asarray(K).astype(int); pal=K.getpalette()
OY,OX,ymin,xmin,y0,x0=np.load('kaal_info.npz')['geo']; a,lum,g=laad()
o=kaal.copy(); log=[]
def zet(y,x,v,stap):
    if o[y,x]!=v: log.append((stap,y,x,o[y,x],v)); o[y,x]=v
def blok(Y,X):
    ny=OY+3*(Y-y0+ymin); nx=OX+3*(X-x0+xmin); return slice(max(ny,0),ny+3),slice(max(nx,0),nx+3)
P=np.array(pal[:3*13]).reshape(13,3)
GRP={1:'zwart',2:'roze',3:'roze',4:'roze',5:'roze',6:'groen',7:'groen',8:'groen',9:'groen',10:'wit',11:'wit',12:'pit'}
TON={'roze':[2,3,4,5],'groen':[6,7,8,9],'wit':[10,11]}
GN={2:'roze',4:'groen',6:'wit'}
def vlaktint(Y,X):
    sl=blok(Y,X); gb=g[sl]; cnt={k:(gb==k).sum() for k in (2,4,6)}; k=max(cnt,key=cnt.get)
    if cnt[k]==0: return None
    c=a[sl][gb==k].mean(0); t=TON[GN[k]]; return t[int(((P[t]-c)**2).sum(1).argmin())]
OOG=lambda y,x: 12<=x<=18 and 37<=y<=42
MOND=lambda y,x: 4<=x<=19 and 40<=y<=55
nzw=np.zeros((64,64),int)
for y,x in zip(*np.where(o>0)): nzw[y,x]=(g[blok(y,x)]==1).sum()
m=o>0; pad=np.pad(m,1); rand=m&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
# A
def simpel(y,x):   # verwijderen breekt geen 8-verbinding tussen de zwarte buren (ring van 8: 1 overgang)
    ring=[(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
    v=[o[y+dy,x+dx]==1 for dy,dx in ring]
    if sum(v)<2: return False                       # eindpunt of los: laten
    tr=sum(1 for i in range(8) if v[i] and not v[(i+1)%8])
    return tr==1
for rnd in range(3):
    kand=sorted([(nzw[y,x],y,x) for y,x in zip(*np.where((o==1)&~rand)) if not OOG(y,x) and not MOND(y,x)])
    for n,y,x in kand:
        if o[y,x]!=1 or n>3: continue
        sterk=[(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if o[y+dy,x+dx]==1 and nzw[y+dy,x+dx]>=n]
        if not sterk or not simpel(y,x): continue
        v=vlaktint(y,x)
        if v: zet(y,x,v,'A')
# A2 zwakke binnenlijn (blok met <= LZ zwarte modelpx van 9) -> donkerste tint van het eigen vlak (Gen 3: binnenlijnen
#    in een donkere tint van het vlak; zwart alleen waar vorm over vorm valt = sterke modellijn). Oog en bek bevroren.
LZ=int(sys.argv[sys.argv.index('--lz')+1]) if '--lz' in sys.argv else 2
for y,x in zip(*np.where((o==1)&~rand)):
    if OOG(y,x) or MOND(y,x) or nzw[y,x]>LZ: continue
    sl=blok(y,x); gb=g[sl]; cnt={k:(gb==k).sum() for k in (2,4)}; k=max(cnt,key=cnt.get)
    if cnt[k]: zet(y,x,2 if k==2 else 6,'A2')
# T toonkaart (binnenvulling roze/groen)
def gauss(x,s):
    r=int(3*s)+1; k=np.exp(-0.5*(np.arange(-r,r+1)/s)**2); k/=k.sum()
    y=np.apply_along_axis(lambda v: np.convolve(v,k,'same'),0,x); return np.apply_along_axis(lambda v: np.convolve(v,k,'same'),1,y)
S=1.5
TGRP=[(2,"roze"),(4,"groen")]
if "--T" in sys.argv: TGRP=[t for t in TGRP if t[1] in sys.argv[sys.argv.index("--T")+1].split(",")]
for k,naam in TGRP:
    mg=(g==k).astype(float); TK=gauss(lum*mg,S)/np.maximum(gauss(mg,S),1e-6)
    ML=np.array([P[t]@[0.299,0.587,0.114] for t in TON[naam]])
    for y,x in zip(*np.where(m&~rand)):
        if GRP.get(o[y,x])!=naam or MOND(y,x) and naam=='roze' and False: continue
        if OOG(y,x): continue
        sl=blok(y,x); gm=g[sl]==k
        if gm.sum()<3: continue
        if ((lum[sl]<62)&(g[sl]!=1)).sum()+(g[sl]==1).sum()>=3: continue
        t=TON[naam][int(np.abs(ML-TK[sl][gm].mean()).argmin())]
        # donkerste toon (selout/naad) alleen als het blok zelf echt donker is
        zet(y,x,t,'T')
# M bek
vlees=[]; pitm={}
for y in range(40,56):
    for x in range(4,20):
        if not m[y,x] or rand[y,x]: continue
        sl=blok(y,x); gb=g[sl]
        if ((gb==6)|(gb==7)).sum()>=3 and (gb==1).sum()<=2 and ((gb==6)|(gb==7)).sum()>=(gb==2).sum():
            c=a[sl][gb==6].mean(0) if (gb==6).any() else P[10]
            zet(y,x,(10,11)[int(((P[[10,11]]-c)**2).sum(1).argmin())],'M vlees'); vlees.append((y,x))
            pitm[(y,x)]=(gb==7).sum()
for y,x in zip(*np.where(o==12)):
    if (y,x) not in pitm: zet(y,x,vlaktint(y,x) or 10,'M pit buiten vlees')
VS=set(vlees); PITS=[]
for n,y,x in sorted([(-v,y,x) for (y,x),v in pitm.items() if v>=1]):
    n=-n
    if any((y+dy,x+dx) not in VS for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue    # niet op de vleesrand
    if any(abs(y-py)<=1 and abs(x-px)<=1 for py,px in PITS): continue
    if n<int(sys.argv[1]) if len(sys.argv)>1 else n<2: continue
    PITS.append((y,x))
for y,x in PITS: zet(y,x,12,'M pit')
# D tand voorin: model heeft een witte hoektand (natief x 16-18, y 89-92) die in de reductie lijn werd
TAND=sys.argv[sys.argv.index('--tand')+1] if '--tand' in sys.argv else '43,4'
ty,tx=map(int,TAND.split(',')); zet(ty,tx,11,'D tand')
# B buitenlijn
keus={}
for y,x in zip(*np.where(rand)):
    ny=sum(dy for dy in (-1,0,1) for dx in (-1,0,1) if not m[y+dy,x+dx])
    nx=sum(dx for dy in (-1,0,1) for dx in (-1,0,1) if not m[y+dy,x+dx])
    if (ny+0.6*nx)>0: keus[(y,x)]=1
    elif o[y,x] in (1,2,3,6,7): keus[(y,x)]=o[y,x]      # al zwart of een van de twee donkerste tinten: blijft (modeltint is al donker genoeg als selout)
    else: keus[(y,x)]=6 if GRP.get(o[y,x])=='groen' else 2
for (y,x),v in list(keus.items()):
    nb=[keus[(y+dy,x+dx)] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and (y+dy,x+dx) in keus]
    if nb and all((b==1)!=(v==1) for b in nb): keus[(y,x)]=Counter(nb).most_common(1)[0][0]
for (y,x),v in keus.items():
    if (y,x)==(ty,tx): continue
    if MOND(y,x) and o[y,x] in (10,11): v=2 if v!=1 else 1     # vleesrand aan de buitenkant: lip
    zet(y,x,v,'B')
# C ruis
VUL={3,4,5,7,8,9,10,11}
seen=np.zeros_like(m)
for yy0,xx0 in zip(*np.where(m)):
    if seen[yy0,xx0] or o[yy0,xx0] not in VUL: continue
    v=o[yy0,xx0]; st=[(yy0,xx0)]; cl=[]; seen[yy0,xx0]=1
    while st:
        y,x=st.pop(); cl.append((y,x))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if not seen[yy,xx] and o[yy,xx]==v: seen[yy,xx]=1; st.append((yy,xx))
    if len(cl)<2 and not OOG(*cl[0]):
        y,x=cl[0]
        nb=Counter(o[y+dy,x+dx] for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and GRP.get(o[y+dy,x+dx])==GRP[v] and o[y+dy,x+dx]!=v)
        if nb: zet(y,x,nb.most_common(1)[0][0],'C')
# E dambord: 2x2 om-en-om van twee vultinten uit dezelfde kleurgroep -> de pixel waarvan het modelblok qua
#    helderheid het dichtst bij de andere tint ligt neemt die tint aan (1 px per dambord)
def blum(y,x):
    sl=blok(y,x); gb=g[sl]; k=2 if GRP.get(o[y,x])=='roze' else 4; mm=gb==k
    return lum[sl][mm].mean() if mm.any() else None
LUMP={i:P[i]@[0.299,0.587,0.114] for i in range(1,13)}
for _ in range(4):
    gevonden=False
    for y in range(63):
        for x in range(63):
            q=o[y:y+2,x:x+2]
            if not (q>0).all() or not (q[0,0]==q[1,1] and q[0,1]==q[1,0] and q[0,0]!=q[0,1]): continue
            t1,t2=q[0,0],q[0,1]
            if t1 not in VUL or t2 not in VUL or GRP[t1]!=GRP[t2] or rand[y:y+2,x:x+2].any(): continue
            best=None
            for yy,xx in ((y,x),(y,x+1),(y+1,x),(y+1,x+1)):
                b=blum(yy,xx); 
                if b is None: continue
                ander=t2 if o[yy,xx]==t1 else t1; d=abs(b-LUMP[ander])
                if best is None or d<best[0]: best=(d,yy,xx,ander)
            if best: zet(best[1],best[2],best[3],'E dambord'); gevonden=True
    if not gevonden: break
UIT=sys.argv[2] if len(sys.argv)>2 else 'pitahaya2_r1.png'
p=Image.fromarray(o.astype('uint8'),'P'); p.putpalette(pal); p.save(UIT,transparency=0)
m2=o>0; pad=np.pad(m2,1); r2=m2&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
def zone(y,x):
    if OOG(y,x): return 'oog'
    if MOND(y,x): return 'bek'
    if x<=24 and y<=45: return 'kop'
    if y<=46 and (o[y,x] in (2,3,4,5,1) or kaal[y,x] in (2,3,4,5)) : return 'rug/lijf roze'
    if x>=48: return 'staart'
    return 'poten/groen'
cnt=Counter((s.split(' ')[0],zone(y,x)) for s,y,x,_,_ in log)
for k,v in sorted(cnt.items()): print(k,v)
print('gewijzigd',len(log),'van',m2.sum(),'silhouet-diff',(m2!=(kaal>0)).sum(),'pits',len(PITS),
      'zwart binnen %.1f%%'%(100*((o==1)&~r2).sum()/m2.sum()),'rand zwart %.0f%%'%(100*((o==1)&r2).sum()/r2.sum()),'kleuren',len(set(o.ravel()))-1)
open(UIT[:-4]+'_afwijkingen.txt','w').write('\n'.join(f'{s}\t({x},{y})\t{a_}->{b}\t{zone(y,x)}' for s,y,x,a_,b in log)+'\n')
