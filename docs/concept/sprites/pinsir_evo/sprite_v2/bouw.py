# Pinsir-evolutie v2 (model_v2_r4.webp) -> frontsprite. Draaien vanuit docs/concept/sprites/pinsir_evo/:
#   python3 sprite_v2/natief_meet.py && python3 sprite_v2/bouw.py
# Alles komt uit modelcellen (natief raster 10,24 px); de enige bewerkingen zijn technisch en staan per stap benoemd.
import sys; sys.path.insert(0,'sprite_v2')
from reductie import *
from scipy import ndimage as nd
OUTDIR='sprite_v2/'

# ---------- stap 1: schoon natief raster (klasse per cel, kleur = modelgemiddelde van die klasse) ----------
MCOL={k:tuple(int(v) for v in a[K==k].mean(0)) for k in range(1,12)}
def kleur(Km,col):
    im=np.zeros(Km.shape+(3,),'uint8')+255
    for k,c in col.items(): im[Km==k]=c
    return im
Image.fromarray(kleur(K,MCOL)).save(OUTDIR+'natief.png')

# ---------- stap 2: alleen de lange modellijnen houden (natief), expliciet gekozen op het model ----------
# Elke binnenlijn van het model is een samenhangende groep zwarte (Z) of donkerbruine (B) cellen. Alleen deze groepen blijven
# (zaadcel x,y in het natieve raster -> de hele groep); al het andere (rugkrasjes, nekkrasjes, korte textuurstreepjes) vervalt.
# Het gezicht (kop/mond/ogen, FACE) houdt al zijn lijnen.
HOUD={
 'kopschildrand rechts (Z2)':(47,19),
 'rug: lijn onder de eerste rugstekels (Z6)':(57,29), 'rug: achterste plaatrand (Z14)':(76,40),
 'schouderkoepel boven (B22)':(51,38), 'schouderkoepel links (B38)':(47,48), 'schouderkoepel links-onder (Z20)':(50,46), 'schouderkoepel onder (Z23)':(56,49),
 'buik rechts + rechterarm/klauw + dijvoorkant (Z18)':(58,43), 'buik links boven (Z22)':(38,49), 'buik links onder (Z37)':(33,63), 'buik/dij onder (Z39)':(51,69),
 'linkerarm (Z30)':(26,56), 'linkerklauw vingers (Z34)':(23,59), 'linkerklauw (B55)':(18,58),
 'linkerknie boven (Z42)':(33,75), 'linkerknie (B69)':(35,70), 'linkerknie (B71)':(30,71), 'linkervoet teen (Z45)':(31,81),
 'rechterknie cirkel boven (B65)':(61,66), 'rechterknie cirkel (B73)':(61,71), 'rechterknie cirkel (Z41)':(65,74), 'rechterknie cirkel onder (Z44)':(57,76), 'rechterknie (B75)':(63,77),
 'dijvoorkant (B63)':(53,64), 'dij achterkant (B59)':(69,60), 'dij/staart grens (B64)':(75,65),
 'staartbasis boven (Z32)':(87,56), 'staartbasis (Z29)':(70,55), 'staartsegment (B57)':(74,58), 'staartsegment (B61)':(81,62), 'staartsegment (B67)':(86,68),
 'rechtervoet klauw (B77)':(58,82), 'rechtervoet klauw (B78)':(68,82),
}
OUTER=(K==1)&nd.binary_dilation(BG,np.ones((3,3)))
keep=np.zeros_like(BG)
labZ,_=nd.label((K==1)&~OUTER,np.ones((3,3))); labB,_=nd.label(K==2,np.ones((3,3)))
for naam,(x,y) in HOUD.items():
    lab_=labZ if K[y,x]==1 else labB
    assert lab_[y,x]>0, naam
    keep|=lab_==lab_[y,x]
# Lijnnetten waarvan alleen het langste doorlopende pad blijft (hoofdlijn zonder vertakkingen/krasjes):
PAD={'rug: hoofdplaatlijn uit het B19-net':(60,34)}
from collections import deque
def langste_pad(m):
    pts=list(zip(*np.where(m)))
    def bfs(src):
        dist={src:0}; prev={src:None}; q=deque([src])
        while q:
            c=q.popleft()
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    n_=(c[0]+dy,c[1]+dx)
                    if n_ in dist or not (0<=n_[0]<H and 0<=n_[1]<W) or not m[n_]: continue
                    dist[n_]=dist[c]+1; prev[n_]=c; q.append(n_)
        far=max(dist,key=dist.get); return far,prev
    a_,_=bfs(pts[0]); b_,prev=bfs(a_)
    out=np.zeros_like(m); c=b_
    while c is not None: out[c]=True; c=prev[c]
    return out
for naam,(x,y) in PAD.items():
    lab_=labZ if K[y,x]==1 else labB
    keep|=langste_pad(lab_==lab_[y,x])
keep|=FACE&(((K==1)&~OUTER)|(K==2))      # gezicht: alleen de lijncellen binnen het gezichtsvak
INNER=((K==1)&~OUTER)|(K==2)
# Buikplaatlijnen (tan op room): bruine cellen met >= 2 roomburen (4-buren) en binnen de buik; lijn met 'elke cel telt'.
BUIK=nd.binary_closing(CREAM&~EYE,np.ones((5,5)))&(xx_:=np.mgrid[0:H,0:W][1]>=30)&(np.mgrid[0:H,0:W][0]>=44)
crn=sum(np.roll(CREAM,sh,ax) for sh,ax in ((1,0),(-1,0),(1,1),(-1,1)))
BUIKLIJN=BUIK&BROWN&(crn>=2)
K2=K.copy()
weg=INNER&~keep
# weggevallen krasjes krijgen de vulklasse die rondom het meest voorkomt (iteratief, van buiten naar binnen)
todo=weg.copy()
while todo.any():
    nxt=todo.copy()
    for y,x in zip(*np.where(todo)):
        ks=[K2[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2)
            if 0<=yy<H and 0<=xx<W and not todo[yy,xx] and K2[yy,xx]>=3]
        if ks: K2[y,x]=Counter(ks).most_common(1)[0][0]; nxt[y,x]=False
    if (nxt==todo).all(): break
    todo=nxt
LIJN=keep   # binnenlijnen die blijven

# ---------- stap 2b: rug (toegestaan door Jordi): alleen grote plaatvormen ----------
# Rugzone = bruine cellen achter de nek, boven de dij/staart, zonder de arm. Hier blijven de eigen toonvlakken van het model staan,
# maar alleen in 3 tinten (hooglicht 6 -> licht 5) en na de reductie worden vlakjes < RUGMIN px opgeslokt door de buurplaat.
yy,xx=np.mgrid[0:H,0:W]
RUG=(K2>=3)&(K2<=6)&(xx>=48)&(xx<=86)&(yy>=28)&( (yy<=47) | ((xx>=60)&(yy<=56)) )
RUG&=~((xx<=58)&(yy>=46))   # arm + klauw blijven model
RUG&=~((xx<=59)&(yy>=37))   # schouderkoepel blijft model (licht)
K2[RUG&(K2==6)]=5

# ---------- stap 3: exacte puntreductie 91x78 cellen -> 64x55 px (elke spritepixel = 1, 2 of 4 modelcellen) ----------
TIE=sys.argv[5] if len(sys.argv)>5 else 'eerste'
PHX=float(sys.argv[2]) if len(sys.argv)>2 else 0.3
PHY=float(sys.argv[3]) if len(sys.argv)>3 else 0.3
cx,cy=kaart(PHX,PHY); OY=63-cy[88]
cells={}
for y in range(H):
    for x in range(W):
        sy,sx=cy[y]+OY,cx[x]
        if 0<=sx<64 and 0<=sy<64: cells.setdefault((sy,sx),[]).append((y,x))
SILF=int(sys.argv[9]) if len(sys.argv)>9 else 4   # silhouet: >= 1/2 van de cellen figuur, rugzone >= 1/SILF
def reduceer(Kin,lijn):
    spr=np.zeros((64,64),int); sil=np.zeros((64,64),bool); bron=np.zeros((64,64),int)  # bron 1 = binnenlijn
    for (sy,sx),cl in cells.items():
        fig=[(y,x) for y,x in cl if not BG[y,x]]
        f_=SILF if (sx>=34 and sy<=42) else 2        # rugstekels: stekelpunt telt al bij 1/4 modeldekking
        if len(fig)*f_<len(cl): continue
        sil[sy,sx]=True
        ln=[(y,x) for y,x in fig if lijn[y,x]]
        if ln:
            spr[sy,sx]=1 if any(FACE[y,x] and K[y,x]==1 for y,x in ln) else 2; bron[sy,sx]=1; continue
        bl=[(y,x) for y,x in fig if BUIKLIJN[y,x]]
        if bl: spr[sy,sx]=12; continue                                  # 12 = buiklijn (donkerste buiktint)
        ks=[Kin[y,x] for y,x in fig if Kin[y,x]>=3]
        if not ks: spr[sy,sx]=-1; continue                             # -1: alleen buitenlijncellen
        c=Counter(ks).most_common(); top=[k for k,v in c if v==c[0][1]]
        # gelijke stand: bij bruin wint de donkerste modeltint (dunne donkere plaatranden blijven), bij rood de lichtste (kaak is licht)
        spr[sy,sx]=min(top,key=lambda k:MCOL[k][0]+MCOL[k][1]) if TIE=='donker' else next(Kin[y,x] for y,x in fig if Kin[y,x] in top)   # gelijke stand: eerste cel (= naaste buur)
    return spr,sil,bron

# ---------- stap 4: kale reductie bewaren (model-klassen, modelkleuren, zonder lijnfilter/rug) ----------
kspr,ksil,_=reduceer(K,(K==1)&~OUTER)
ked=ksil&~nd.binary_erosion(ksil,np.array([[0,1,0],[1,1,1],[0,1,0]]),border_value=0); kspr[ked]=1; kspr[kspr==-1]=1
kim=Image.fromarray(np.dstack([kleur(kspr,MCOL),(ksil*255).astype('uint8')]),'RGBA'); kim.save(OUTDIR+'kaal.png')

# ---------- stap 5: sprite ----------
spr,sil,bron=reduceer(K2,LIJN)
N4=np.array([[0,1,0],[1,1,1],[0,1,0]])
RAND=sil&~nd.binary_erosion(sil,N4,border_value=0)
# buitenlijn 1 px, kleur uit het model: zwart als een van de cellen (of een directe buurcel naar buiten) zwart is,
# anders de donkerste tint van het onderdeel (model heeft daar een gekleurde rand: kaak donkerrood, bruin -> lijntint)
RANDKLEUR={}
for (sy,sx),cl in cells.items():
    if not RAND[sy,sx]: continue
    zw=any(K[y,x]==1 or ((K[max(y-1,0):y+2,max(x-1,0):x+2]==1).any() and BG[max(y-1,0):y+2,max(x-1,0):x+2].any()) for y,x in cl)
    if zw: spr[sy,sx]=1; continue
    ks=[K[y,x] for y,x in cl if K[y,x]>=2]
    if not ks: spr[sy,sx]=1; continue
    g=Counter('r' if k in (9,10) else ('c' if k in (7,8,11) else 'b') for k in ks).most_common(1)[0][0]
    spr[sy,sx]={'r':13,'b':2,'c':1}[g]; RANDKLEUR[(sx,sy)]=g
def buren_meerderheid(y,x,ok):
    ks=[spr[yy,xx] for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1),(y-1,x-1),(y-1,x+1),(y+1,x-1),(y+1,x+1))
        if 0<=yy<64 and 0<=xx<64 and ok(spr[yy,xx])]
    return Counter(ks).most_common(1)[0][0] if ks else None
for _ in range(3):
    for y,x in zip(*np.where(spr==-1)):        # binnenpixel met alleen dubbele buitenlijncellen -> vulkleur van de buren
        v=buren_meerderheid(y,x,lambda k:k>=3)
        if v is not None: spr[y,x]=v
spr[spr==-1]=1
# groepen voor de clusteropschoning
GROEP={3:'b',4:'b',5:'b',6:'b',7:'c',8:'c',9:'r',10:'r'}
GEZICHT=np.zeros((64,64),bool); GEZICHT[19:34,12:25]=True
MIN3=int(sys.argv[6]) if len(sys.argv)>6 else 5
def opschonen(spr,minpx=3):
    for _ in range(4):
        veranderd=0
        for k in (3,4,5,6,7,8,9,10):
            lab,n=nd.label(spr==k,N4)
            for i in range(1,n+1):
                m=lab==i
                if m.sum()>=(MIN3 if k in (3,4,5,6) else minpx): continue
                if (m&GEZICHT).any(): continue                       # gezicht = model, niet opschonen
                ring=nd.binary_dilation(m,N4)&~m
                ks=[v for v in spr[ring] if GROEP.get(v)==GROEP[k]]
                if ks: spr[m]=Counter(ks).most_common(1)[0][0]; veranderd+=1
        if not veranderd: break
    return spr
S0=spr.copy()
spr=opschonen(spr)
S1=spr.copy()
RUGMIN=int(sys.argv[4]) if len(sys.argv)>4 else 8
RUGS=np.zeros((64,64),bool)
for (sy,sx),cl in cells.items():
    if sum(RUG[y,x] for y,x in cl)*2>=len(cl): RUGS[sy,sx]=True
def opschonen_zone(spr,zone,minpx):
    for _ in range(6):
        veranderd=0
        for k in (3,4,5):
            lab,n=nd.label((spr==k)&zone,N4)
            for i in range(1,n+1):
                m=lab==i
                if m.sum()>=minpx: continue
                ring=nd.binary_dilation(m,N4)&~m
                ks=[v for v in spr[ring] if v in (3,4,5)]
                if ks: spr[m]=Counter(ks).most_common(1)[0][0]; veranderd+=1
        if not veranderd: break
    return spr
spr=opschonen_zone(spr,RUGS,RUGMIN)
S2=spr.copy()

# ---------- stap 5a: rugplaten met 3 tinten (Jordi: rug vereenvoudigen; licht linksboven, schaduw rechtsonder) ----------
# Plaat = samenhangend bruin vlak in de rugzone tussen de gehouden modellijnen/buitenlijn. Per plaat bolvormige belichting uit
# linksboven op de eigen vorm van de plaat (zwaartepunt + spreiding), gekwantiseerd in schaduw 3 / midden 4 / licht 5.
RUGPLAAT=sys.argv[8] if len(sys.argv)>8 else 'ja'
if RUGPLAAT=='ja':
    fill=(spr>=3)&(spr<=6)
    lab,n=nd.label(fill&RUGS,N4)
    Ld=np.array([-0.55,-0.65,0.52]); Ld/=np.linalg.norm(Ld)
    for i in range(1,n+1):
        m=lab==i; yy,xx=np.where(m)
        if len(yy)<6: continue
        cy_,cx_=yy.mean(),xx.mean(); ry=max(yy.std()*2.0,1.5); rx=max(xx.std()*2.0,1.5)
        u=(xx-cx_)/rx; v=(yy-cy_)/ry; r2=np.clip(u*u+v*v,0,0.98); nz=np.sqrt(1-r2)
        I=(u*Ld[0]+v*Ld[1]+nz*Ld[2])
        t=np.where(I<0.18,3,np.where(I>0.72,5,4))
        spr[yy,xx]=t

S3=spr.copy()
# ---------- stap 5b: volume per vorm (kleur mag afwijken, Jordi 17 nov) ----------
# Binnen elke bruine vorm (afgebakend door de modellijnen en buitenlijn): pixel met een lijn direct boven/links -> 1 stap lichter
# (lichtrand linksboven), pixel met een lijn direct onder/rechts -> 1 stap donkerder (schaduwsikkel rechtsonder). Geen nieuwe vormen.
VOL=sys.argv[7] if len(sys.argv)>7 else 'nee'
if VOL=='ja':
    lijnp=(spr==1)|(spr==2)|(spr==0)
    o=spr.copy()
    for y in range(1,63):
        for x in range(1,63):
            k=spr[y,x]
            if k not in (3,4,5,6): continue
            onder=lijnp[y+1,x] or lijnp[y,x+1]; boven=lijnp[y-1,x] or lijnp[y,x-1]
            if onder and not boven: o[y,x]=max(3,k-1)
            elif boven and not onder: o[y,x]=min(6 if k>=5 else 5,k+1)
    VOLDIFF=(o!=spr).sum(); spr=o

# ---------- stap 6: eindpalet (Gen 3-stappen, gemeten tegen Pinsir 213/175/127/69 en Tyranitar 221/192/143/71) ----------
PAL=[(152,208,160),          # 0 transparant
     (16,12,10),             # 1 buitenlijn / gezicht
     (46,32,22),             # 2 bruin lijntint (binnenlijnen)     L 35
     (90,70,52),             # 3 bruin schaduw   (model L 80)      L 74
     (128,104,80),           # 4 bruin midden    (model L 98)      L 107
     (170,144,112),          # 5 bruin licht     (model L 127)     L 147
     (208,188,150),          # 6 bruin hooglicht (model L 148) = buikschaduw (model L 173)  L 190
     (238,226,190),          # 7 room (buik, klauwen, tanden)      L 226
     (70,24,24),             # 8 rood donker                       L 38
     (124,48,42),            # 9 rood midden                       L 70
     (176,98,80),            # 10 rood licht                       L 115
     (248,236,160),          # 11 oog
     ]
KL2IDX={1:1,2:2,3:3,4:4,5:5,6:6,7:6,8:7,9:9,10:10,11:11,12:5,13:8}
def naar_idx(spr):
    o=np.zeros_like(spr)
    for k,v in KL2IDX.items(): o[spr==k]=v
    return o
BUIKS=np.zeros((64,64),bool)
for (sy,sx),cl in cells.items():
    if any(BUIK[y,x] for y,x in cl): BUIKS[sy,sx]=True
def details(I):
    I=I.copy()
    # gezicht (spritevak x 12-24, y 19-33): pupilstreep naast het oog zwart zoals het model; tanden (mond x 14-20, y 25-30) room
    for y in range(19,34):
        for x in range(12,25):
            if I[y,x]==2 and any(I[y+dy,x+dx]==11 for dy,dx in ((0,1),(0,-1),(1,0),(-1,0))): I[y,x]=1
            if I[y,x]==6 and 14<=x<=20 and 25<=y<=30: I[y,x]=7      # alleen tanden in de mond
    # stekels: binnenpixels van uitsteeksels (silhouet minus opening). Flanken zoals het model ('-O#': donker links, licht rechts);
    # 1 px brede stekel = lichte tint (model: lichte stekelpunt)
    s_=I>0; prot=s_&~nd.binary_opening(s_,np.ones((3,3)))
    prot=nd.binary_dilation(prot,N4)&s_
    for y,x in zip(*np.where(prot)):
        if I[y,x] not in (3,4,5,6) or y>44: continue
        l=I[y,x-1] in (0,1); r=I[y,x+1] in (0,1)
        if l and not r: I[y,x]=3
        elif r and not l: I[y,x]=6 if I[y,x]>=5 else 5
        elif l and r: I[y,x]=5
    # losse tintvlekjes < 3 px (4-buren) opruimen: bruin buiten gezicht/stekels/buik, rood overal; ze nemen de meest voorkomende
    # buurtint van dezelfde groep. Tanden, klauwen, stekelflanken en buiklijnen blijven (die horen klein te zijn).
    global VLEKWEG
    VLEKWEG=0
    for _ in range(3):
        for k,groep in ((3,(3,4,5,6)),(4,(3,4,5,6)),(5,(3,4,5,6)),(6,(3,4,5,6)),(9,(9,10)),(10,(9,10))):
            lab,n=nd.label(I==k,N4)
            for i in range(1,n+1):
                m=lab==i
                if m.sum()>=3: continue
                yy,xx=np.where(m)
                if k<=6 and ((GEZICHT&m).any() or (prot&m).any() or (BUIKS&m).any()): continue
                ring=nd.binary_dilation(m,N4)&~m
                ks=[v for v in I[ring] if v in groep and v!=k]
                if ks: I[m]=Counter(ks).most_common(1)[0][0]; VLEKWEG+=int(m.sum())
    # stekelpunt 1 px: van een platte top '##' (lucht erboven) valt de pixel weg die niet boven de stekelkern staat
    global PUNTWEG
    PUNTWEG=[]
    for _ in range(2):
        for y in range(1,63):
            for x in range(1,63):
                if I[y,x]!=1 or I[y-1,x]!=0 or not (x>=34 or y<=14): continue
                if I[y+1,x] in (0,1):
                    for q in (x-1,x+1):
                        kern_q=I[y+1,q]>=2 or (I[y+1,q]==1 and y+2<64 and I[y+2,q]>=2)
                        kern_p=I[y+1,x]>=2 or (y+2<64 and I[y+2,x]>=2)
                        if I[y,q]==1 and I[y-1,q]==0 and kern_q and not kern_p:
                            I[y,x]=0; PUNTWEG.append((x,y)); break
    return I
def opslaan(idx,naam):
    im=Image.fromarray(idx.astype('uint8'),'P'); pl=[c for t in PAL for c in t]; pl+= [0]*(768-len(pl))
    im.putpalette(pl); im.save(naam,transparency=0)

# ---------- stap 7: uitvoer ----------
if __name__=='__main__' or True:
    IDX=details(naar_idx(spr))
    assert len(np.unique(IDX))<=16
    opslaan(IDX,OUTDIR+'pinsir_evo_v2_r1.png')
    chk=Image.open(OUTDIR+'pinsir_evo_v2_r1.png'); assert chk.mode=='P' and chk.info.get('transparency')==0
    RGBA=np.array(Image.open(OUTDIR+'pinsir_evo_v2_r1.png').convert('RGBA'))
    # afwijkingen t.o.v. de kale reductie (kale klassen op hetzelfde palet), per zone
    KAAL=naar_idx(kspr); KAAL[~ksil]=0
    ZONES={'kopschild+stekels':(8,8,36,20),'gezicht':(12,19,25,34),'kaken':(0,20,12,42),'buik+arm links':(8,33,32,52),
           'rug+schouder':(28,16,58,42),'staart':(52,30,64,54),'benen':(8,48,52,64)}
    regels=[]
    for z,(x0,y0,x1,y1) in ZONES.items():
        a_=KAAL[y0:y1,x0:x1]; b_=IDX[y0:y1,x0:x1]; f_=((a_>0)|(b_>0)).sum()
        regels.append('%-18s %4d van %4d px anders (%d%%)'%(z,(a_!=b_).sum(),f_,round(100*(a_!=b_).sum()/max(f_,1))))
    sil_diff=((KAAL>0)!=(IDX>0)).sum()
    D0=naar_idx(spr); fig=IDX>0
    def n_(a,b): return int(((naar_idx(a)!=naar_idx(b))&fig).sum())
    regels+=['', 'herkomst (pixels die van de pure reductie met de gekozen lijnen afwijken, per stap):',
      ' opschonen vlakjes (< 3 px, schaduw/bruin < 5 px):  %d'%n_(S0,S1),
      ' rug: vlakjes < 8 px opgeslokt:                      %d'%n_(S1,S2),
      ' rug: plaatvulling 3 tinten (licht linksboven):      %d'%n_(S2,S3),
      ' oogrand+pupil zwart (model: zwart):               %d'%int(((D0!=1)&(IDX==1)&GEZICHT).sum()),
      ' tanden room (model: roomkleurig, hooglichtindex):   %d'%int(((D0==6)&(IDX==7)).sum()),
      ' stekelflanken + losse tintvlekjes opgeruimd:       %d'%int(((D0!=IDX)&fig&~GEZICHT&(IDX>=3)&(IDX<=6)).sum()-0),
      ' stekelpunten 1 px (transparant gemaakt):            %d'%len(PUNTWEG),
      ' buitenlijn niet-zwart (model: gekleurde rand):      %d'%int((RAND&(IDX!=1)&fig).sum())]
    open(OUTDIR+'afwijkingen.txt','w').write('\n'.join(regels)+'\nsilhouet: %d px anders dan kale reductie\nstekelpunten weggehaald: %s\nlosse tintvlekjes opgeruimd: %d px\n'%(sil_diff,PUNTWEG,VLEKWEG))
    print('\n'.join(regels)); print('silhouet',sil_diff,'punten',PUNTWEG)
    # model op dezelfde maat als de sprite (64 px = 91/S cellen)
    mod0=Image.open('referenties/model_v2_r4.webp').convert('RGB'); mod=Image.new('RGB',(1424,1424),'white'); mod.paste(mod0,(200,200))
    p_=10.24; e_=lambda i: 9.25+0.5+(i-1)*p_
    sz=64/S*p_; lx=e_(X0)-PHX/S*p_+200+0.4*sz/64; ty=e_(Y0)-(PHY+OY)/S*p_+200+0.4*sz/64   # +0,4 px: cel i begint op (i-X0)*S+PH (gemeten: silhouet-IoU 0,93)
    def modelstuk(x0,y0,x1,y1,Z):
        f=sz/64; return mod.crop((int(lx+x0*f),int(ty+y0*f),int(lx+x1*f),int(ty+y1*f))).resize(((x1-x0)*Z,(y1-y0)*Z),Image.LANCZOS)
    def spritestuk(x0,y0,x1,y1,Z,bg=(255,255,255)):
        o=Image.new('RGB',(64,64),bg); sp=Image.fromarray(RGBA,'RGBA'); o.paste(sp,(0,0),sp)
        return o.crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    from PIL import ImageDraw
    # rug_8x: alleen rug/schouder/rugstekels
    R=(26,14,60,44); Z=8
    a1=spritestuk(*R,Z); a2=modelstuk(*R,Z)
    rv=Image.new('RGB',(a1.width*2+24,a1.height+28),'white'); rv.paste(a1,(8,24)); rv.paste(a2,(a1.width+16,24))
    d=ImageDraw.Draw(rv); d.text((8,6),'sprite v2 r1 (8x)',fill=(0,0,0)); d.text((a1.width+16,6),'model v2_r4, zelfde maat',fill=(0,0,0))
    rv.save(OUTDIR+'rug_8x.png')
    # vel: sprite | model op 6x, daarna 1x en 2x naast Tyranitar/Aggron/Pinsir op wit en donker
    G='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/'
    def ref(n):
        im_=Image.open(G+n+'/anim_front_gba.png'); a_=np.asarray(im_)[:64]
        rgba=np.array(im_.convert('RGBA'))[:64]; rgba[a_==0,3]=0; return Image.fromarray(rgba,'RGBA')
    sp=Image.fromarray(RGBA,'RGBA')
    top_a=spritestuk(0,0,64,64,6); top_b=modelstuk(0,0,64,64,6)
    rij=[('nieuw',sp)]+[(n,ref(n)) for n in ('tyranitar','aggron','pinsir')]
    cw=64+128+24; W_=max(top_a.width*2+24,len(rij)*cw+16)
    vel=Image.new('RGB',(W_,top_a.height+16+2*(128+40)),'white')
    vel.paste(top_a,(8,8)); vel.paste(top_b,(top_a.width+16,8))
    for bi,bgc in enumerate([(255,255,255),(40,48,56)]):
        y0=top_a.height+16+bi*(128+40)
        vel.paste(Image.new('RGB',(W_,128+40),bgc),(0,y0))
        d=ImageDraw.Draw(vel)
        for i,(n,s_) in enumerate(rij):
            x=8+i*cw
            vel.paste(s_,(x,y0+20+64),s_); b2=s_.resize((128,128),Image.NEAREST); vel.paste(b2,(x+64+8,y0+20),b2)
            d.text((x,y0+4),n,fill=(0,0,0) if bi==0 else (230,230,230))
    vel.save(OUTDIR+'vel.png')
