# Swablu (onweerswolk) r2: "swablu is nog wat blurry" (Jordi over r1).
# Basis = r1 (silhouet bevroren, alpha-diff 0). Oorzaak blur gemeten: r1 koos per spritepixel de tint bij de GEMIDDELDE modelkleur,
# daardoor werden randen tussen modelvlakken middentinten (verloop). r2 telt per spritepixel de modeltonen (stemming per natieve pixel,
# oppervlaktegewogen) en neemt de meest voorkomende: heldere vlakken zoals het model, dat zelf al in 3 tonen per materiaal staat.
import sys, numpy as np
from PIL import Image
sys.path.insert(0,'gereedschap'); from klassen import klassen
import gemeen as G
from gemeen import overlap, label, S
a,c,L=klassen()
# --- palet r2: wolk 5 tonen (2 materialen à 3 + selout), stappen ±30-45; vogel 3; geel feller; wit 2 ---
PAL=[(152,208,160),(13,17,24),
     (68,78,96),(96,108,126),(126,138,156),(164,176,192),(210,216,228),   # 2 wolk diep, 3 donker, 4 midden, 5 licht, 6 wit
     (68,90,110),(106,130,152),(150,174,194),                            # 7 vogel donker, 8 midden, 9 licht
     (200,158,40),(248,214,64),(255,246,160),                            # 10 oker, 11 geel, 12 lichtgeel
     (214,220,230),(250,251,253)]                                        # 13 snavelwit, 14 glans
G.PAL=PAL; G.CH='.K01234abcoyYwW'
WOLK={2,3,4,5,6}; VOGEL={7,8,9}; GEEL={10,11,12}; WIT={13,14}
# r1 -> r2 indexvertaling (zelfde betekenis, nieuw palet)
R1={0:0,1:1,2:2,3:3,4:4,5:4,6:5,7:6,8:7,9:8,10:9,11:10,12:11,13:12,14:13,15:14}
r1=np.asarray(Image.open('sprite_r1/swablu_r1.png')).astype(int); o=np.vectorize(R1.get)(r1)
start=o.copy()
tel={}
def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]
# --- 1. toonstemming per spritepixel (modeltonen per natieve pixel) ---
def wolktoon(l): return 6 if l>=188 else 5 if l>=152 else 4 if l>=124 else 3 if l>=97 else 2   # modelbanden ~200/~165/~138/~112/~84
def vogeltoon(l): return 9 if l>=145 else 8 if l>=105 else 7
STEM=np.zeros((64,64,15)); FK=np.zeros((64,64)); FD=np.zeros((64,64)); FN=np.zeros((64,64))
for Y in range(64):
    for X in range(64):
        for u,v,w in overlap(X,Y):
            k=c[v,u]
            if k==1: FK[Y,X]+=w
            if k in (1,3) and L[v,u]<70: FD[Y,X]+=w        # donkere lijn (zwart of donkergrijze bultnaad)
            if k in (1,3) and L[v,u]<124: FN[Y,X]+=w       # naad in een lichte bol (model: grijze lijn L<124 tussen de bollen)
            if k==3: STEM[Y,X,wolktoon(L[v,u])]+=w
            elif k==2: STEM[Y,X,vogeltoon(L[v,u])]+=w
v=o.copy()
for Y,X in zip(*np.where(np.isin(o,list(WOLK|VOGEL)))):
    grp=WOLK if o[Y,X] in WOLK else VOGEL
    s=STEM[Y,X]; ks=sorted(grp); t=[s[k] for k in ks]
    if max(t)>0: o[Y,X]=ks[int(np.argmax(t))]
stap('toonstemming (vlakken i.p.v. verloop)',v)
# --- 2. naden tussen de bollen: waar het model een donkere lijn heeft (zwart of donkergrijs, L<70) die door de gemiddelde-kleurregel wegviel.
#        Rug-regel: >=15% lijn en meer lijn dan de buren dwars op de lijn -> zwart als het model daar zwart is, anders wolk diep. Alleen binnen de figuur, niet op de rand. ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(np.isin(o,list(WOLK|VOGEL)))):
    if any(not fg[Y+dy,X+dx] for dy,dx in N4): continue
    f=FD[Y,X]
    if f<0.15: continue
    h=f>=FD[Y,X-1] and f>=FD[Y,X+1]; vv=f>=FD[Y-1,X] and f>=FD[Y+1,X]
    if h or vv: o[Y,X]=1 if FK[Y,X]>=0.5*f else 2
stap('naden tussen bollen',v)
# --- 2b. naden binnen de lichte bollen: het model scheidt de bollen met een grijze lijn (L<124, 1-2 natieve px). Waar een lichte pixel (licht/wit)
#         >=20% van zo'n lijn heeft en de rug van de lijn is -> wolk midden (de selouttint van de lichte bollen) ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(np.isin(o,[5,6]))):
    if any(not fg[Y+dy,X+dx] for dy,dx in N4): continue
    f=FN[Y,X]
    if f<0.20: continue
    h=f>=FN[Y,X-1] and f>=FN[Y,X+1]; vv=f>=FN[Y-1,X] and f>=FN[Y+1,X]
    if h or vv: o[Y,X]=4
stap('naden in lichte bollen',v)
# --- 3. buitenlijn (zelfde regel als r1): achtergrond rechts/onder -> zwart (staat al); lichtkant -> selout: lichte bol -> wolk midden, onderwolk/vleugel -> wolk diep, vogel -> vogel donker ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(fg)):
    k=o[Y,X]
    if k==1 or k in GEEL|WIT: continue
    bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
    if not(bL or bR or bU or bD): continue
    if bR or bD: n=1
    elif k in VOGEL: n=7
    else: n=4 if any(o[Y+dy,X+dx] in (5,6) for dy,dx in N4) else 2
    o[Y,X]=n
stap('buitenlijn',v)
# --- 4. ontkorrelen: tintvlekjes < 3 px in wolk/vogel -> meest voorkomende buurtint van dezelfde groep (randpixels en naden blijven) ---
def ontkorrel():
    fg=o>0
    for k in (3,4,5,6,8,9):
        lab,n=label(o==k,acht=False)
        for i in range(1,n+1):
            m=lab==i
            if m.sum()>=3: continue
            ys,xs=np.where(m)
            if any(not fg[y+dy,x+dx] for y,x in zip(ys,xs) for dy,dx in N4): continue
            grp=WOLK if k in WOLK else VOGEL
            buur=[o[y+dy,x+dx] for y,x in zip(ys,xs) for dy,dx in N4 if o[y+dy,x+dx] in grp and o[y+dy,x+dx]!=k]
            if buur: o[m]=max(set(buur),key=buur.count)
v=o.copy(); ontkorrel(); ontkorrel(); stap('ontkorrelen',v)
# --- 5. voelsprieten bevroren: de r1-reparaties (sprieten per gemeten pixel) blijven; stap 1-4 mochten daar niets veranderen ---
SPR=(slice(0,24),slice(23,42)); v=o.copy(); o[SPR]=start[SPR]; stap('sprieten terug naar r1',v)
def zet(lijst,naam):
    v=o.copy()
    for X,Y,k in lijst: o[Y,X]=k
    stap(naam,v)
# --- 6. r1-reparaties bewaren die stap 1-4 overschreven (oog, kruin, snavelrand, staartje: gemeten modelplekken uit r1) ---
R1REP=[(28,27),(28,28),(29,28),(28,29),(29,29),(27,28),(28,24),(21,29),(21,30)]+[(x,46) for x in range(45,49)]
zet([(X,Y,start[Y,X]) for X,Y in R1REP],'r1-reparaties terug')
# staartje (45-48,45): model natief L~85 = zelfde band als de onderwolk eromheen -> wolk diep (r1: donker)
zet([(x,45,2) for x in range(45,49)],'staartje toon')
# --- 7. snavelbovenrand: drie tinten door elkaar (model: dunne donkere rand + lichtgrijze snaveltop, natief rij 50-51) -> één tint wolk midden, zoals r1 ---
zet([(22,27,4),(23,27,4),(24,27,4)],'snavelbovenrand')
# --- 8. hooglicht op de kop (Gen 3, licht linksboven; model is daar vlak midden): de 3 lichte modelpixels (26,24) (25,25) (26,25) uitgebreid tot een klein vlak op de bolling ---
zet([(27,25,9),(25,26,9),(26,26,9)],'hooglicht kop')
# --- 9. vonken feller, minder oker: oker alleen op de buitenhoek rechtsonder (achtergrond rechts én onder), lichtgeel waar de pixel niet aan
#        lucht grenst (geen lichte buitenrand), anders fel geel ---
v=o.copy(); fg=o>0
for Y,X in zip(*np.where(np.isin(o,list(GEEL)))):
    bL=not fg[Y,X-1]; bR=not fg[Y,X+1]; bU=not fg[Y-1,X]; bD=not fg[Y+1,X]
    o[Y,X]=10 if (bR and bD) else 11 if (bL or bU or bR or bD) else 12
stap('vonken feller',v)
G.opslaan(o,'sprite_r2/swablu_r2.png')
from PIL import Image as I
im=G.rgb(o,(255,255,255)).resize((512,512),I.NEAREST); im.save('sprite_r2/swablu_r2_8x.png')
print('stappen',tel); print('anders dan r1: %d px'%(o!=start).sum(),'| alpha-diff met r1:',int(((o>0)!=(start>0)).sum()),'| kleuren excl. transp.',len(set(o.ravel()))-1)
G.toon(o,15,50,8,52)
