"""Capykart r16. Basis r15b (silhouet, hoepels, gezicht, toren-vorm). Stappen:
 1 hout: tint per pixel uit de modelhelderheid (lum.py, sigma 6) -> 4 houttinten; 2 vacht idem -> E/2/D/4;
 3 omlijning kop naar Gen 3 (lichtkant 4, schaduwkant 1); 4 toren ingekleurd per kubus; 5 clusters <3 px weg."""
import os, sys, json, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__)); os.chdir(H)
src=np.array(Image.open('../r15b/capykart_creme.png')); im=Image.open('../r15b/capykart_creme.png'); pal=im.getpalette()
G=src.copy().astype(int)
LUM=np.load(os.environ.get('LUMF','lum_s4.npy'))
# ---- palet (16 incl. transparant) ----
PAL={1:(32,20,28),2:(216,158,116),3:(240,200,72),4:(122,72,50),5:(246,170,102),6:(214,128,76),7:(178,44,56),8:(88,96,128),
     9:(252,232,150),10:(100,156,232),11:(60,140,72),12:(240,92,84),13:(176,106,74),14:(236,186,146),15:(96,180,84)}
for i,c in PAL.items(): pal[3*i:3*i+3]=c
FUR={2,3,14}; WOOD={5,6,13}
def toren(x,y): return x>=44 and y<=32 and not (x<=46 and y>=29)   # blokken + dak; (44-46,29-32) = auto/nek
def nb4(a,x,y): return [a[y+b,x+a_] for a_,b in ((1,0),(-1,0),(0,1),(0,-1))]
def nb8(a,x,y): return [a[y+b,x+a_] for a_ in (-1,0,1) for b in (-1,0,1) if (a_ or b)]
FACE=set([(x,y) for x in range(28,32) for y in range(16,22)]+[(x,y) for x in range(17,24) for y in range(30,34)]
         +[(21,15),(22,15),(23,15),(21,16),(22,16),(23,16),(15,22),(16,22),(18,28),(19,28)]+[(x,30) for x in range(25,29)])
HOOP={8,9}
# ---- zones uit r15b ----
kop=np.zeros((64,64),bool)   # vachtpixels (kop+nek) = vacht-indices + 4 dat aan vacht grenst en niet aan hout
for y in range(1,63):
    for x in range(1,63):
        v=src[y,x]
        if v==0 or toren(x,y): continue
        if v in FUR: kop[y,x]=True
kop2=kop.copy()
for y in range(1,63):
    for x in range(1,63):
        if src[y,x]==4 and not toren(x,y) and y<=33 and any(kop[y+b,x+a] for a in (-1,0,1) for b in (-1,0,1)) and not any(n in WOOD for n in nb8(src,x,y)): kop2[y,x]=True
kop=kop2
hout=np.zeros((64,64),bool)
for y in range(1,63):
    for x in range(1,63):
        v=src[y,x]
        if v==0 or toren(x,y) or kop[y,x] or 0 in nb4(src,x,y): continue
        if v in WOOD: hout[y,x]=True
        elif v==4 and y>=31 and any(n in WOOD for n in nb8(src,x,y)): hout[y,x]=True
# hout groeit over aaneengesloten 4-vlakken (donkere holte onder de borst, r15b-plak) vanaf rij 33
for _ in range(20):
    add=[(x,y) for y in range(33,63) for x in range(1,63) if src[y,x]==4 and not hout[y,x] and not kop[y,x] and not toren(x,y)
         and 0 not in nb4(src,x,y) and any(hout[y+b,x+a] for a,b in ((1,0),(-1,0),(0,1),(0,-1)))]
    if not add: break
    for x,y in add: hout[y,x]=True
# ---- 1 hout ----
# natieve modelpixel per spritecel (voor lijnen): r15b-lijnpixel (4) blijft 4 als het model daar zelf een donkere lijn heeft
M=np.asarray(Image.open('../../referenties/model_r5.png').convert('RGB')).astype(float); NP,PH=20.48,19.5
def natlum(x,y):
    p=12.064516129032258; mx=133+(x-1+.5)*p; my=860-62*p+(y+.5)*p
    j,i=int((my-PH-1)//NP),int((mx-PH-1)//NP); cx,cy=PH+1+NP/2+i*NP,PH+1+NP/2+j*NP
    return float(np.median(M[int(cy-2):int(cy+3),int(cx-2):int(cx+3)].reshape(-1,3),0)@[.299,.587,.114])
LIJN=[]
QH=[float(v) for v in os.environ.get('QH','18,45,82').split(',')]
TH=tuple(np.nanpercentile(LUM[hout],QH)); print("TH",[round(t) for t in TH])
for y,x in zip(*np.nonzero(hout)):
    v=LUM[y,x]
    if np.isnan(v): continue
    if src[y,x]==4 and natlum(x,y)<100 and ((src[y,x-1]!=4 and src[y,x+1]!=4) or (src[y-1,x]!=4 and src[y+1,x]!=4)): LIJN.append((x,y)); continue
    G[y,x]=4 if v<TH[0] else 13 if v<TH[1] else 6 if v<TH[2] else 5
# ---- 2 vacht ----
QF=[float(v) for v in os.environ.get('QF','12,40,85').split(',')]
TF=tuple(np.nanpercentile(LUM[kop],QF))
rand=lambda x,y: 0 in nb4(src,x,y)
for y,x in zip(*np.nonzero(kop)):
    if os.environ.get('VACHT','r15b')=='r15b': break   # vacht: tinten van r15b houden (modelkop past niet op de vergrote spritekop)
    if (x,y) in FACE or rand(x,y): continue
    v=LUM[y,x]
    if np.isnan(v): continue
    G[y,x]=4 if v<TF[0] else 13 if v<TF[1] else 2 if v<TF[2] else 14
# ---- 3 omlijning kop: buitenrand lichtkant (lucht links/boven) = 4, schaduwkant (lucht rechts/onder) = 1 ----
for y,x in zip(*np.nonzero(kop)):
    if (x,y) in FACE or not rand(x,y): continue
    licht=src[y,x-1]==0 or src[y-1,x]==0; donker=src[y,x+1]==0 or src[y+1,x]==0
    G[y,x]=1 if (donker and not (src[y-1,x]==0 and src[y,x+1]!=0)) else 4
G[(G==3)&~np.array([[toren(x,y) for x in range(64)] for y in range(64)])]=13
LUM4=np.nan_to_num(np.load('lum_s4.npy'),nan=255)
exec(open('kop.py').read())
exec(open('toren.py').read())
exec(open('opschonen.py').read())
o=Image.fromarray(G.astype('uint8'),'P'); o.putpalette(pal); o.save('capykart.png',transparency=0)
o.convert('RGBA').resize((512,512),Image.NEAREST).save('capykart_8x.png')
np.save('kop_mask.npy',kop); np.save('hout_mask.npy',hout)
with open('ops.txt','w') as f:
    f.write(f'houtdrempels (kwantielen {QH} van modelhelderheid sigma {os.environ.get("LUMF","lum_s4.npy")}): {[round(t) for t in TH]}\n')
    f.write(f'r15b-lijnpixels 4 behouden (model heeft daar zelf een donkere lijn, 1 px dik): {len(LIJN)} {LIJN}\n')
    f.write(f'opschonen clusters <3 px: {len(OPS)} {OPS}\n'); f.write(f'dubbele lijn langs hoepels weg: {len(HOOPOPS)} {HOOPOPS}\n')
    f.write('kop:\n  '+'\n  '.join(KOPLOG)+'\n')
