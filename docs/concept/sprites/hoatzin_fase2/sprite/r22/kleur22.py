# r19 kleur: hele sprite opnieuw ingekleurd binnen de vaste vorm (vorm.npy = r17-vorm + r19-pootvorm), per pixel uit het model gemeten.
# Palet = modeltinten per zone (helderheid uit elkaar getrokken); alleen buik (variant D) en kuif (bruiner) wijken af (Jordi).
# Onderdelen (delen.py) krijgen elk een eigen grens: binnenlijn op het achterste onderdeel, of toonsprong (kop/nek).
import numpy as np; from PIL import Image
import sys
STD=int(sys.argv[1]) if len(sys.argv)>1 else 4     # streep: >= STD/9 lichte modelcellen
SEPN=int(sys.argv[2]) if len(sys.argv)>2 else 5    # penscheiding: >= SEPN/9 modelcellen met L<65
from meet import cel; from delen import delen, NAMEN, LIJN
V=np.load('vorm.npy'); A=V>0; P=delen(V); N={n:i for i,n in enumerate(NAMEN)}
T=np.load('../r17/blad64.npy',allow_pickle=True).item()['toon']   # gladde modeltoon van de vulling (r17-pixelblad, sigma 1,5)
import importlib.util, os
spec=importlib.util.spec_from_file_location('bev','../r17/bevroren.py'); bev=importlib.util.module_from_spec(spec)
cwd=os.getcwd(); os.chdir('../r17'); spec.loader.exec_module(bev); MS=bev.maskers(); os.chdir(cwd)
GZ=bev.schuif(MS['snavel'],1,1)|bev.schuif(MS['oog'],1,1)
P[GZ&A]=N['gezicht']
PAL=[(0x98,0xD0,0xA0),
 (0x1C,0x10,0x1A),  # 1 lijn (model buitenlijn)
 (0x3C,0x2D,0x3D),  # 2 donker: model vleugel #422A3B / poot #3B3749, gedeeld schaduwtint
 (0x6A,0x4C,0x5F),  # 3 vleugel midden (model #6A4C5F)
 (0x8C,0x6B,0x7D),  # 4 nek/licht (model #8C6B7D)
 (0xA4,0x90,0xA2),  # 5 lichte strepen + licht grijs (r22: 5 #A8909F en 15 #9694AE samengevoegd, plek 15 vrij voor kuifschaduw)
 (0x69,0x3D,0x32),  # 6 kuif midden (model #693D32)
 (0xA0,0x62,0x4C),  # 7 kuif licht (plukkern; bruin, niet oranje)  was (model #704239 lichter; bruiner dan r16-oranje)
 (0x2E,0x38,0x8A),  # 8 blauw donker (r16/r17, bevroren)
 (0x62,0x7C,0xDA),  # 9 blauw (r16/r17, bevroren)
 (0xD8,0x32,0x4A),  # 10 oog rood (r16/r17, bevroren; SPEC: rood met zwart puntje)
 (0x4C,0x28,0x60),(0x7C,0x44,0x98),(0xB4,0x7C,0xD6),  # 11-13 buik variant D (besproken)
 (0x62,0x60,0x7A),  # 14 grijs (r17, snavel bevroren; poten delen hem)
 (0x47,0x22,0x1C)]  # 15 kuif donkerbruin (model #3D1815/#522B25): donkere kant van de plukken, selout kuif
out=V.copy(); log=[]
BEV=np.isin(P,[N['buik'],N['staart'],N['gezicht']])          # bevroren binnenkant (alleen palet volgt het model)
def nb4(y,x): return [(y+dy,x+dx) for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)) if 0<=y+dy<64 and 0<=x+dx<64]
def zet(x,y,v,w):
    if out[y,x]!=v: log.append((w,x,y,int(out[y,x]),v)); out[y,x]=v
# ---- vulling per onderdeel uit de modeltoon
bruinL=[cel(x,y)['Lbruin'] for y,x in zip(*np.where(P==N['kuif'])) if cel(x,y)['bruin']>=3]
t7,t2=np.quantile(bruinL,0.45),np.quantile(bruinL,0.15)
for y,x in zip(*np.where(A&~BEV)):
    p=NAMEN[P[y,x]]; c=cel(x,y); d=c['donker']; t=T[y,x]; lijn=V[y,x]==1
    if p=='vleugel':      # scheiding per pen (modellijn -> donkerste vlaktint), vulling uit de gladde toon; strepen hieronder
        v=2 if (lijn or c['sep']>=SEPN or t<62) else (3 if t<105 else 4)
    elif p=='verre':      # verre vleugel een stap donkerder
        v=2 if (lijn or d>=5 or t<75) else (3 if t<110 else 4)
    elif p=='kop':        # donkere kop achter het oog (model #462F38)
        v=2 if (t<70 or d>=6) else 3      # r20: een toon lichter waar het model lichter is (band smaller)
    elif p=='nek':        # nek in eigen lichte tinten; donkere modelstrepen -> 2
        v=2 if lijn else (4 if t>=98 else 3)
    elif p=='kuif':       # ondergrond van de kuif: bruine basis waar het model vol bruin is, anders de kruin (verre vleugel)
        v=6                               # r21: hele kuifvlak in de donkere kuiftint; licht alleen op de plukken
    elif p=='poot':
        v=1 if lijn else 14
    else: continue
    zet(x,y,v,'vulling '+p)
def lijn4(a,b):
    """4-verbonden lijn van a naar b (Bresenham; elke diagonale stap krijgt een hoekpixel)"""
    (x0,y0),(x1,y1)=a,b; pts=[]; dx=abs(x1-x0); dy=-abs(y1-y0); sx=1 if x0<x1 else -1; sy=1 if y0<y1 else -1; e=dx+dy; x,y=x0,y0
    while True:
        pts.append((x,y))
        if (x,y)==(x1,y1): break
        e2=2*e; mx=my=False
        if e2>=dy: e+=dy; x+=sx; mx=True
        if e2<=dx: e+=dx; y+=sy; my=True
        if mx and my: pts.insert(len(pts),(x-sx,y) if abs(dx)>=abs(dy) else (x,y-sy))
    return pts
# vleugelstrepen. Slagpennen (x>=39, y<=24): per pen een doorlopende lichte schacht, begin/eind afgelezen op het model (16x-raster).
PENNEN=[((37,12),(42,5)),((40,15),(48,7)),((40,16),(51,9)),((41,18),(53,11)),((41,19),(55,15)),((41,22),(49,22)),((39,23),(49,24))]
WV=(P==N['vleugel'])&A&~BEV
binnen=lambda x,y: WV[y,x] and all(A[yy,xx] for yy,xx in nb4(y,x))
ST=np.zeros((64,64),bool)
for a,b in PENNEN:
    for x,y in lijn4(a,b):
        if binnen(x,y): ST[y,x]=True
# overige vleugel (dekveren, armpennen): modelstrepen (>= STD/9 licht), 4-verbonden, alleen stukken van >= 3 px
LC=np.zeros((64,64),int); S2=np.zeros((64,64),bool)
for y,x in zip(*np.where(WV)):
    if x>=39 and y<=24: continue
    LC[y,x]=cel(x,y)['licht']; S2[y,x]=LC[y,x]>=STD and binnen(x,y)
for it in range(3):
    for y,x in zip(*np.where(S2)):
        for dy in (-1,1):
            for dx in (-1,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64 and S2[yy,xx] and not S2[y,xx] and not S2[yy,x]:
                    a_,b_=(y,xx),(yy,x); c_=a_ if LC[a_]>=LC[b_] else b_
                    if binnen(c_[1],c_[0]): S2[c_]=True
seen=np.zeros((64,64),bool)
for y,x in zip(*np.where(S2)):
    if seen[y,x]: continue
    comp=[];st=[(y,x)]
    while st:
        p_=st.pop()
        if seen[p_] or not S2[p_]: continue
        seen[p_]=True; comp.append(p_); st+=nb4(*p_)
    if len(comp)>=3:
        for p_ in comp: ST[p_]=True
for y,x in zip(*np.where(WV)):
    if out[y,x]==5 and not ST[y,x]: zet(x,y,3,'losse streep weg')
for y,x in zip(*np.where(ST)): zet(x,y,5,'streep')
# r21 slagpennen (waaier rond lijnen.C, hoek -85..12 graden, straal >= 8): vlak 3 (4 waar het model licht is),
# donkere scheidingen 2 en lichte schachten 5 als doorlopende 4-verbonden lijnen uit de polaire modelmeting (polar.py)
import lijnen as LJ
SP=np.zeros((64,64),bool)
for y,x in zip(*np.where(WV)):
    th,r=LJ.hoek(x,y)
    if -85<=th<=12 and r>=8 and binnen(x,y): SP[y,x]=True
for y,x in zip(*np.where(SP)):
    zet(x,y,3,'pen vlak'); ST[y,x]=False          # r22: rustig vlak 3
for pl in LJ.SCHEID:
    pts=[LJ.xy(p) for p in pl]
    for a_,b_ in zip(pts,pts[1:]):
        for x,y in lijn4(a_,b_):
            if SP[y,x]: zet(x,y,2,'pen scheiding')
for pl in LJ.SCHACHT:
    pts=[LJ.xy(p) for p in pl]
    for a_,b_ in zip(pts,pts[1:]):
        for x,y in lijn4(a_,b_):
            if SP[y,x]: zet(x,y,5,'pen schacht'); ST[y,x]=True
# r21 armpennen: scheidingslijnen uit het model (lijnen.VEER) in de middentint 3 over het donkere vlak 2
from lijnen import PLUK as PLUKL, VEER
VL=np.zeros((64,64),bool)
for pl in VEER:
    for (a_,b_) in zip(pl,pl[1:]):
        for x,y in lijn4(a_,b_):
            if WV[y,x] and binnen(x,y) and out[y,x]==2 and not ST[y,x]: VL[y,x]=True
# r22: veerrand (modellijn) licht 4 over het donkere vlak 2: per veer licht (rand) - donker (vlak), meer waardecontrast dan r21 (3)
for y,x in zip(*np.where(VL)): zet(x,y,4,'veerrand')
# r21 kuifplukken: polylijnen uit het model (lijnen.PLUK), kern 7, donkere kant 2 (rechts bij staande, onder bij liggende stukken);
# het dunne stuk van A tegen de lucht (y<=15) in 6 (geen lichte kleur op de buitenrand).
KZ=np.isin(P,[N['kuif'],N['verre']])&A
PL=np.zeros((64,64),bool); KERN=[]
for nm,pl in PLUKL.items():
    for (a_,b_) in zip(pl,pl[1:]):
        steil=abs(b_[1]-a_[1])>abs(b_[0]-a_[0])
        for x,y in lijn4(a_,b_):
            if not KZ[y,x] or PL[y,x]: continue
            PL[y,x]=True; KERN.append((x,y,steil,nm))
for x,y,steil,nm in KERN:
    zet(x,y,6 if (nm=='A' and y<=15) else 7,'pluk '+nm)
for x,y,steil,nm in KERN:
    sx,sy=(x+1,y) if steil else (x,y+1); tx,ty=(sx+1,sy) if steil else (sx,sy+1)
    if KZ[sy,sx] and not PL[sy,sx] and (P[sy,sx]==N['kuif'] or not PL[ty,tx]): zet(sx,sy,15,'pluk schaduw '+nm)

for y,xl in LIJN.items():            # neklijn (r19-vorm) blijft doorlopend, met de lichte vleugelvoorrand (4/5 uit r17/r19) als eigen strook ernaast
    if not BEV[y,xl]: zet(xl,y,1,'neklijn')
    x=xl+1
    while x<64 and V[y,x] in (4,5) and not BEV[y,x]: zet(x,y,int(V[y,x]),'vleugelrand'); x+=1
# poten: licht bovenkant / midden / donker onderkant; verre poot (x<=27 en niet de voorste voet) een stap donkerder
VOOR=lambda x,y: (x>=28) or (y>=57 and x>=24)
for y,x in zip(*np.where(P==N['poot'])):
    if V[y,x]==1: continue
    boven=V[y-1,x]; onder=V[y+1,x] if y<63 else 0
    top= boven in (0,1) or P[y-1,x]!=N['poot']; bodem= onder in (0,1)
    if VOOR(x,y): v=15 if top else (2 if bodem and V[y-2,x] not in (0,1) else 14)
    else: v=14 if top else (2 if bodem else 14)
    zet(x,y,v,'poot toon')
# ---- buitenlijn: elke rand tegen de lucht = lijn (niet bevroren)
for y,x in zip(*np.where(A&~BEV&(P!=N['poot']))):   # poten: lijnen staan al per pixel uit het model (bouw19)
    if any(not A[yy,xx] for yy,xx in nb4(y,x)) or y in (0,63) or x in (0,63):
        if NAMEN[P[y,x]]=='kuif' and x<=10 and out[y,x]==6 and sum(A[yy,xx] for yy,xx in nb4(y,x))<=1: continue  # losse streng blijft bruin
        if PL[y,x] and NAMEN[P[y,x]]=='kuif' and x<=10: continue
        licht=[(yy,xx) for yy,xx in nb4(y,x) if not A[yy,xx]]
        lichtkant=all(yy<y or xx<x for yy,xx in licht) and len(licht)>0      # lucht alleen boven/links: lichtkant
        sel={'kuif':15,'verre':(15 if y>=16 else 2),'vleugel':2,'kop':2,'nek':2}.get(NAMEN[P[y,x]],1)
        zet(x,y,sel if lichtkant else 1,'buitenlijn' if not lichtkant else 'selout')
# ---- grenzen tussen onderdelen: binnenlijn op het achterste deel (diepte: hoger = voor)
RANG={'vleugel':9,'buik':8,'poot':7,'kuif':6,'gezicht':6,'kop':5,'nek':4,'staart':3,'verre':2}
for y,x in zip(*np.where(A&~BEV)):
    p=NAMEN[P[y,x]]
    for yy,xx in nb4(y,x):
        if not A[yy,xx]: continue
        q=NAMEN[P[yy,xx]]
        if q==p or RANG[q]<=RANG[p]: continue
        if {p,q} in ({'kop','nek'},{'kuif','verre'},{'kuif','kop'}): continue   # toonsprong (kleurverschil is de grens)
        if {p,q}=={'kop','gezicht'} or {p,q}=={'kop','kuif'} and out[y,x]==2: continue
        if out[yy,xx] in (1,8,11): continue                       # voorste deel heeft daar al een lijn
        zet(x,y,1,'grens %s|%s'%(p,q)); break
# r21: vleugel tegen de (bevroren) staart: de staart mag geen binnenlijn krijgen, dus toonsprong aan de vleugelkant
# (model: vleugelpunten T 75-90 boven de zwarte staart) -> rand van de vleugel in 3
for y,x in zip(*np.where((P==N['vleugel'])&A&~BEV)):
    if out[y,x]==1 or any(not A[yy,xx] for yy,xx in nb4(y,x)): continue
    if any(P[yy,xx]==N['staart'] for yy,xx in nb4(y,x)) and T[y,x]>=60: zet(x,y,3,'vleugelrand tegen staart')
pass
# ---- opschonen (alleen niet-bevroren pixels, vorm blijft):
def dam():
    r=[]
    for y in range(63):
        for x in range(63):
            p,q,r_,s_=out[y,x],out[y,x+1],out[y+1,x],out[y+1,x+1]
            if p and q and p==s_ and q==r_ and p!=q: r.append((x,y))
    return r
for it in range(30):          # dambord = diagonale 1-px lijn: verbind de diagonaal orthogonaal (lichtere/lijnkleur breidt 1 px uit)
    D=dam()
    if not D: break
    for x,y in D:
        p,q=out[y,x],out[y,x+1]
        if not (out[y,x] and out[y,x+1] and out[y,x]==out[y+1,x+1] and out[y,x+1]==out[y+1,x] and p!=q): continue
        # welke kleur is de 'lijn': strepen (5) of donkere scheiding/lijn (1,2) wint; anders de lichtere
        def gewicht(v): return {5:3,1:2,2:1}.get(v,0)
        w=q if gewicht(q)>=gewicht(p) else p
        if w==q: kand=[(x,y),(x+1,y+1)]          # q staat op de anti-diagonaal; vul een p-hoek
        else: kand=[(x+1,y),(x,y+1)]
        for cx,cy in kand:
            if not BEV[cy,cx] and NAMEN[P[cy,cx]] not in ('poot',) and not (cy in LIJN and cx==LIJN[cy]):
                zet(cx,cy,int(w),'dambord'); break
        else:
            cx,cy=kand[0]
            if not BEV[cy,cx]: zet(cx,cy,int(w),'dambord')
# losse pixels (geen gelijke 8-buur, geen lijn/streep, niet bevroren) -> meest voorkomende buurkleur binnen het onderdeel
for it in range(2):
    for y in range(1,63):
        for x in range(1,63):
            v=out[y,x]
            if v in (0,1,5) or BEV[y,x] or P[y,x]==N['poot']: continue
            n8=out[y-1:y+2,x-1:x+2]; 
            if (n8==v).sum()>1: continue
            bb=[out[yy,xx] for yy,xx in nb4(y,x) if out[yy,xx] not in (0,) and P[yy,xx]==P[y,x]]
            if bb:
                vals,cn=np.unique(bb,return_counts=True); zet(x,y,int(vals[cn.argmax()]),'los')
# zwarte binnenklonten 2x2 -> rechtsonder naar 2
for y in range(63):
    for x in range(63):
        b=out[y:y+2,x:x+2]
        if (b==1).all() and A[max(0,y-1):y+3,max(0,x-1):x+3].all() and not BEV[y+1,x+1]: zet(x+1,y+1,2,'klont')
for x,y in dam():                    # rest-dambord: rechterbovenpixel krijgt de kleur van zijn diagonaal
    if not BEV[y,x+1]: zet(x+1,y,int(out[y,x]),'dambord rest')
# r22 dekverenband langs de voorrand: lichte band (4) met de modelstrepen (lijnen.BAND) in 5, i.p.v. een dicht blok 5
import lijnen as LJ2
BD=np.zeros((64,64),bool)
for y,x in zip(*np.where((P==N['vleugel'])&A&~BEV)):
    if x<=34 and 23<=y<=38 and out[y,x] in (4,5) and all(A[yy,xx] for yy,xx in nb4(y,x)): BD[y,x]=True
for y,x in zip(*np.where(BD)): zet(x,y,4,'dekverenband')
for pl in LJ2.BAND:
    for a_,b_ in zip(pl,pl[1:]):
        for x,y in lijn4(a_,b_):
            if BD[y,x] or (out[y,x] in (3,4) and P[y,x]==N['vleugel'] and all(A[yy,xx] for yy,xx in nb4(y,x)) and out[y,x]!=1): zet(x,y,5,'dekverenstreep')
# r22 nek: donkere strepen onder het gezicht (rijen 26-33, x 15-22) per pixel uit het model: L < 46 -> 2, anders nektoon
from meetpoot import meet
for y in range(26,34):
    for x in range(15,23):
        if not A[y,x] or BEV[y,x] or P[y,x] not in (N['nek'],N['kop']) or out[y,x]==1: continue
        if any(not A[yy,xx] for yy,xx in nb4(y,x)): continue
        l=meet(x,y)[1]
        if l<46: zet(x,y,2,'nekstreep')
        elif out[y,x]==2: zet(x,y,4 if T[y,x]>=98 else 3,'nek licht')
for x,y in ((20,29),(19,30),(21,30)): zet(x,y,2,'nekstreep 4-verbonden (geen dambord)')
# r22 poten (vorm uit poten22.py): grijs met zwarte omlijning alleen aan de schaduwkant; aan de lichtkant (lucht alleen boven/links)
# de donkere grijstint 14 als selout; binnen 14, met lichte rand 15 direct onder de bovenrand (alleen de voorste poot/voet);
# klauwen: alleen de laatste pixel van elke teen zwart.
PO=np.load('poot22.npy')
VER=lambda x,y: (x<=23 and y>=55) or (y<=54 and x<=28)          # verre (linker) poot en voet
for y,x in zip(*np.where(PO)):
    lucht=[(yy,xx) for yy,xx in nb4(y,x) if out[yy,xx]==0]
    if lucht:
        licht=all(yy<y or xx<x for yy,xx in lucht)
        v=(2 if any(yy<y for yy,xx in lucht) else 14) if licht else 1   # boven: selout 2; alleen links (staande teen/poot): grijs 14, zodat dunne delen 2 px grijs houden
    else:
        boven=out[y-1,x]
        v=15 if (not VER(x,y) and PO[y-1,x] and any(out[yy,xx]==0 for yy,xx in nb4(y-1,x))) else 14
    zet(x,y,v,'poot22')
for x,y in ((16,57),(25,60),(29,63),(17,58)): zet(x,y,1,'klauw')
for y,x in zip(*np.where(out==15)):
    if P[y,x] not in (N['kuif'],N['verre']): zet(x,y,5,'licht grijs -> 5 (samengevoegd)')
im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette([c for t in PAL for c in t]); im.save('hoatzin.png',transparency=0)
im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%t for t in PAL))
np.save('r22.npy',out)
from collections import Counter; print(Counter(l[0].split(' ')[0] for l in log)); print('alpha anders dan vorm',((out>0)!=A).sum()); open('kleurlog.txt','w').write('\n'.join(map(str,log)))
