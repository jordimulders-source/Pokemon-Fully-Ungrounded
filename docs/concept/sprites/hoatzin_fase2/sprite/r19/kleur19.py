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
 (0xA8,0x90,0x9F),  # 5 lichte strepen (model #BDA2B5, helderheid 174 -> 150)
 (0x69,0x3D,0x32),  # 6 kuif midden (model #693D32)
 (0x92,0x56,0x49),  # 7 kuif licht (model #704239 lichter; bruiner dan r16-oranje)
 (0x2E,0x35,0x6A),  # 8 blauw donker (model #282E5C)
 (0x5D,0x6F,0xBC),  # 9 blauw (model #5D6FBC)
 (0xB0,0x54,0x84),  # 10 oog (model iris #B05484-ish)
 (0x4C,0x28,0x60),(0x7C,0x44,0x98),(0xB4,0x7C,0xD6),  # 11-13 buik variant D (besproken)
 (0x5F,0x5B,0x6B),  # 14 grijs (model poot/snavel #5B5765-#676371)
 (0x8E,0x8A,0x9C)]  # 15 grijs licht (model, helderheid uit elkaar)
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
        v=2 if (t<95 or d>=4) else 3
    elif p=='nek':        # nek in eigen lichte tinten; donkere modelstrepen -> 2
        v=2 if lijn else (4 if t>=98 else 3)
    elif p=='kuif':
        if c['bruin']>=3: v=7 if c['Lbruin']>=t7 else (2 if c['Lbruin']<t2 else 6)
        elif x<=10: v=6
        else: v=2 if d>=4 else 6
    elif p=='poot':
        v=1 if lijn else 14
    else: continue
    zet(x,y,v,'vulling '+p)
# vleugelstrepen: modelpixels met >=2/9 licht (L>=140) -> 5, en 4-verbonden gemaakt (diagonale stap krijgt de hoekpixel
# met de meeste lichte modelcellen), zodat elke streep een doorlopende trap is zonder dambord.
WV=(P==N['vleugel'])&A&~BEV
ST=np.zeros((64,64),bool); LC=np.zeros((64,64),int)
for y,x in zip(*np.where(WV)):
    LC[y,x]=cel(x,y)['licht']; ST[y,x]=LC[y,x]>=STD and not any(not A[yy,xx] for yy,xx in nb4(y,x))
for it in range(3):
    for y,x in zip(*np.where(ST)):
        for dy in (-1,1):
            for dx in (-1,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<64 and 0<=xx<64 and ST[yy,xx] and not ST[y,xx] and not ST[yy,x]:
                    a,b=(y,xx),(yy,x); c_=a if LC[a]>=LC[b] else b
                    if WV[c_] and V[c_]!=1 or WV[c_]: ST[c_]=True
for y,x in zip(*np.where(ST)): zet(x,y,5,'streep')
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
        zet(x,y,1,'buitenlijn')
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
np.save('kleur_stap1.npy',out)
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
im=Image.fromarray(out.astype('uint8'),'P'); im.putpalette([c for t in PAL for c in t]); im.save('hoatzin.png',transparency=0)
im.resize((512,512),Image.NEAREST).save('hoatzin_8x.png')
open('normal.pal','w').write('JASC-PAL\r\n0100\r\n16\r\n'+''.join('%d %d %d\r\n'%t for t in PAL))
np.save('r19.npy',out)
from collections import Counter; print(Counter(l[0].split(' ')[0] for l in log)); print('alpha anders dan vorm',((out>0)!=A).sum()); open('kleurlog.txt','w').write('\n'.join(map(str,log)))
