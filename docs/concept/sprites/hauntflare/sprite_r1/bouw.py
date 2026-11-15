# Stap 2+3: herkleuren op hun plek + Haunter-gezicht. Niets getekend: elke pixel is een modelpixel
# (model64.png, uit schrap.py) met een paletkleur, of een Haunter Gen 3-pixel (gezicht).
# Gebruik (vanuit de repo-root): python3 docs/concept/sprites/hauntflare/sprite_r1/bouw.py [gezichtsschaal]
import json, sys
from PIL import Image; import numpy as np
from scipy import ndimage as nd
D='docs/concept/sprites/hauntflare/'; S=D+'sprite_r1/'
SCH=json.load(open(S+'schrap.json'))
def verklein(path):
    """zelfde bijsnijding en schrapping als schrap.py, voor een ander natief plaatje (zelfde 99x99 raster)"""
    a=np.asarray(Image.open(path).convert('RGB')).astype(int)
    X0,Y0,X1,Y1=SCH['crop']; c=a[Y0:Y1+1,X0:X1+1]
    c=np.delete(np.delete(c,[r-Y0 for r in SCH['rijen_natief']],0),[k-X0 for k in SCH['kolommen_natief']],1)
    out=np.full((64,64,3),255); ox,oy=SCH['offset']; h,w=c.shape[:2]; out[oy:oy+h,ox:ox+w]=c
    return out
M=np.asarray(Image.open(S+'model64.png').convert('RGB')).astype(int)
RC=verklein(D+'model/nat_r4_c.png')        # ring-toonverdeling
WIT=M.min(2)>=0xf0
r,g,b=M[...,0],M[...,1],M[...,2]; lum=0.299*r+0.587*g+0.114*b
yy,xx=np.mgrid[:64,:64]
# ---------- palet ----------
PAL=[(0,0,0),            # 0 transparant
 (0x24,0x16,0x1a),       # 1 omlijning
 (0x5a,0x2a,0x33),       # 2 ring donker
 (0x8a,0x4e,0x55),       # 3 ring midden (= modelkleur)
 (0xb0,0x74,0x7a),       # 4 ring licht
 (0xc8,0x43,0x5b),       # 5 bol selout/donker (= modelkleur)
 (0xf0,0x44,0x82),       # 6 bol schaduw
 (0xfa,0x76,0xa2),       # 7 bol midden
 (0xf8,0xae,0xc2),       # 8 bol licht
 (0xf9,0xcc,0xd8),       # 9 bol glans
 (0x9a,0x2a,0x22),       # 10 donkerrood (vlam/hand/mond)
 (0xd8,0x40,0x30),       # 11 vlam rood (kern)
 (0xf4,0x86,0x59),       # 12 vlam oranje (r4_a-rand)
 (0xf8,0xb8,0x50),       # 13 vlam geel-oranje (punten/randen)
 (0xff,0xff,0xff),       # 14 oogwit / tanden (Haunter)
 (0xee,0x74,0x7c)]       # 15 hand licht
P=np.array(PAL)
def near(c,idx):
    idx=list(idx); d=((P[idx]-np.array(c))**2).sum(1); return idx[int(d.argmin())]
# ---------- onderdelen ----------
zwart=(M.max(2)<0x48)&~WIT
plum=(~WIT)&(M.max(2)<0x70)&~zwart                         # donkere pruim/bruinrood randpixels
ringk=(~WIT)&(np.abs(r-0x8a)<16)&(np.abs(g-0x4e)<16)&(np.abs(b-0x55)<16)
lab,n=nd.label(~WIT,np.ones((3,3)))
rhand=lab==lab[40,58]; lhand=lab==lab[52,15]
ell=((xx-28)/18.5)**2+((yy-32.5)/17)**2<=1
bol=ell&(~WIT)&~ringk
kuif=(~WIT)&~bol&~ringk&~zwart&(yy<25)&(xx>30)&~rhand
staart=(~WIT)&~bol&~ringk&~zwart&(yy>=38)&(xx>=34)&(xx<=58)&~rhand&~lhand
# ringpruim (donkere randtinten van de ring) = alles pruim dat aan ringbruin grenst
ringdil=nd.binary_dilation(ringk,np.ones((3,3)))
ring=ringk|(plum&ringdil&~kuif&~staart&~rhand&~lhand)
out=np.zeros((64,64),int)
out[zwart]=1
# ---------- ring: tonen uit r4_c (helderheid per pixel, 3 tonen) ----------
rl0=0.299*RC[...,0]+0.587*RC[...,1]+0.114*RC[...,2]
# r4_c-helderheid gemiddeld over de 3x3-buren binnen de ring (minder ruis, zelfde verdeling licht/donker)
w=ringk.astype(float); k3=np.ones((3,3))
rl=nd.convolve(np.where(ringk,rl0,0),k3,mode='constant')/np.maximum(nd.convolve(w,k3,mode='constant'),1)
vals=rl[ringk]
t1,t2=np.percentile(vals,[30,80])
for y,x in zip(*np.where(ring)):
    if plum[y,x]: out[y,x]=2; continue
    v=rl[y,x]; out[y,x]=2 if v<t1 else (3 if v<t2 else 4)
RING_T=(float(t1),float(t2))
# ---------- bol: dichtstbijzijnde bol-tint ----------
OUDGEZICHT=np.zeros((64,64),bool)
binnen=(((xx-28)/16.5)**2+((yy-32.5)/15)**2<=1)&(xx>=14)&(xx<=31)&(yy>=22)&(yy<=40)
for y,x in zip(*np.where(bol&~ring)):
    if zwart[y,x] or plum[y,x] or (M[y,x][1]<0x60):   # donkere lijn of mondrood
        if binnen[y,x]: OUDGEZICHT[y,x]=True; continue
        if zwart[y,x]: continue
    out[y,x]=near(M[y,x],[5,6,7,8,9])
OUDGEZICHT|=binnen&(out==0)&~WIT
# oude oogwitten (licht, omsloten door de oude ooglijnen) ook weg
lw=binnen&np.isin(out,[8,9])&nd.binary_dilation(OUDGEZICHT,np.ones((3,3)),iterations=2)
OUDOOG=lw&nd.binary_fill_holes(nd.binary_dilation(OUDGEZICHT,np.ones((3,3))))
OUDGEZICHT|=OUDOOG
# ---------- vlammen: zelfde verdeling, warmer ----------
# modelklassen: donker (ba3c26/6a2622) -> 10, karmijn (cb435a) -> 11, roze-rood (e85f80) -> 12, oranje (f8856c) -> 13
VL={(0xba,0x3c,0x26):10,(0x6a,0x26,0x22):10,(0xcb,0x43,0x5a):11,(0xe8,0x5f,0x80):12,(0xf8,0x85,0x6c):13}
vk=np.array(list(VL.keys())); vv=list(VL.values())
for m_ in (kuif,staart):
    for y,x in zip(*np.where(m_)):
        if plum[y,x]: out[y,x]=10; continue
        out[y,x]=vv[int(((vk-M[y,x])**2).sum(1).argmin())]
# ---------- handen ----------
HK={(0x93,0x24,0x1d):10,(0x6a,0x1c,0x1f):10,(0xe4,0x4c,0x56):11,(0xc9,0x40,0x51):5,(0xea,0x60,0x6c):15}   # schaduwrood c94051 = bol-selout c8435b (zelfde modeltint)
hk=np.array(list(HK.keys())); hv=list(HK.values())
for m_ in (rhand,lhand):
    for y,x in zip(*np.where(m_&~zwart)):
        out[y,x]=hv[int(((hk-M[y,x])**2).sum(1).argmin())]
# ---------- oud modelgezicht weg: herkleuren met de bol-tint van de buren (van buiten naar binnen) ----------
todo=OUDGEZICHT.copy(); out[todo]=0
while todo.any():
    nieuw=[]
    for y,x in zip(*np.where(todo)):
        nb=[out[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and out[y+dy,x+dx] in (5,6,7,8,9) and not todo[y+dy,x+dx]]
        if len(nb)>=2: nieuw.append((y,x,max(set(nb),key=nb.count)))
    if not nieuw: break
    for y,x,v in nieuw: out[y,x]=v; todo[y,x]=False
# ---------- Haunter-gezicht plakken ----------
SCHAAL=sys.argv[1] if len(sys.argv)>1 else 'k4r2o'
GZ=np.load(S+'gezicht_%s.npy'%SCHAAL)
gy,gx=np.where(GZ>0)
# linksboven van het gezichtsblok = linksboven van het modelgezicht (64-raster gemeten: x14-30, y24/25-38)
dx=int(sys.argv[2]) if len(sys.argv)>2 else 14
dy=int(sys.argv[3]) if len(sys.argv)>3 else 24
dx-=int(gx.min()); dy-=int(gy.min())
GK={1:1,2:5,3:14,4:10,5:15,6:7,7:6} # K zwart, L donkere lijn -> bol-selout, W oogwit, A/N mond, tanden (huidkleur) -> bolroze
for y,x in zip(gy,gx):
    out[y+dy,x+dx]=GK[int(GZ[y,x])]
GEZ_OFF=(int(dx),int(dy))
GEZICHT=np.zeros((64,64),bool); GEZICHT[gy+dy,gx+dx]=True
# ---------- losse pixels die buiten elke groep vielen (rand kuif/ring, oranje modeltint) ----------
for y,x in zip(*np.where((~WIT)&(out==0))): out[y,x]=near(M[y,x],[10,11,12,13])
# ---------- handen: kleurgebruik van de r4_a-handen (oranje aan de onderrand van vingers/duim en de
# binnenkant van de kromming; rood lijf; lichte knokkels blijven) ----------
HANDORANJE=[]
# gat = transparante pixel onder de hand met handmateriaal erboven (<=3 px) en links en rechts (<=4 px): de boog
# tussen vingers/duim. Randpixels van de hand langs de omlijning van zo'n gat worden oranje (zoals r4_a).
for hm in (rhand,lhand):
    gat=np.zeros((64,64),bool)
    for y,x in zip(*np.where(out==0)):
        if 2<=y<62 and 2<=x<62 and hm[max(0,y-3):y,x].any() and hm[y,max(0,x-4):x].any() and hm[y,x+1:x+5].any():
            gat[y,x]=True
    lijn=nd.binary_dilation(gat,[[0,1,0],[1,1,1],[0,1,0]])&(out==1)
    rim=nd.binary_dilation(lijn,[[0,1,0],[1,1,1],[0,1,0]])&hm&np.isin(out,[5,11,15])
    rim&=~nd.binary_dilation(out==0,[[0,1,0],[1,1,1],[0,1,0]])     # niet op de buitenrand
    for y,x in zip(*np.where(rim)):
        out[y,x]=12; HANDORANJE.append((int(x),int(y)))
for hm in (rhand,lhand):
    for y,x in zip(*np.where(hm&np.isin(out,[5,11,15]))):
        onder=out[y+1,x]
        if onder==1:                        # onderrand tegen de omlijning (vingertop, binnenkant van de boog)
            out[y,x]=12; HANDORANJE.append((int(x),int(y)))
# ---------- opruimen: tintvlakjes < 3 px nemen de meest voorkomende buurtint van dezelfde groep ----------
rand=nd.binary_dilation(out==0,np.ones((3,3)))&(out!=0)
GROEP=[(ring,{2,3,4}),(bol,{5,6,7,8,9}),(kuif|staart,{10,11,12,13})]
OPGERUIMD=0
for _ in range(6):
    gewijzigd=0
    for gm,tones in GROEP:
        for t in tones:
            l,k=nd.label(gm&(out==t)&~GEZICHT)
            for i_ in range(1,k+1):
                cl=l==i_
                if cl.sum()>=3: continue
                ys_,xs_=np.where(cl)
                if rand[cl].any(): continue               # buitenrand: apart behandeld (selout)
                nb=[]
                for y,x in zip(ys_,xs_):
                    for ey in(-1,0,1):
                        for ex in(-1,0,1):
                            v=out[y+ey,x+ex]
                            if v in tones and v!=t and not GEZICHT[y+ey,x+ex]: nb.append(v)
                if nb:
                    out[cl]=max(set(nb),key=nb.count); gewijzigd+=int(cl.sum())
    OPGERUIMD+=gewijzigd
    if not gewijzigd: break
print('opgeruimd (tintvlakjes <3 px herkleurd):',OPGERUIMD,' hand-oranje:',len(HANDORANJE))
# ---------- buitenrand: geen lichte kleur op de rand; gekleurde selout (donkerder tint van het eigen vlak) ----------
rand4=nd.binary_dilation(out==0,[[0,1,0],[1,1,1],[0,1,0]])&(out!=0)
SELOUT={7:6,8:6,9:6,      # bol: lichte randpixels -> hete roze selout
        3:2,4:2,          # ring: bruin op de rand -> donkerbruin
        13:12,12:11,      # vlam: geel -> oranje, oranje -> rood
        15:10,14:1}       # hand licht -> donkerrood
SELOUTLOG=[]
for y,x in zip(*np.where(rand4)):
    v=int(out[y,x])
    if v in SELOUT and not GEZICHT[y,x]:
        if v in (12,13) and not (kuif|staart)[y,x]: 
            out[y,x]=10; SELOUTLOG.append((int(x),int(y),v,10)); continue
        out[y,x]=SELOUT[v]; SELOUTLOG.append((int(x),int(y),v,SELOUT[v]))
print('buitenrand-selout herkleurd:',len(SELOUTLOG))
# ---------- nooit zwart en donker om-en-om op een rand: losse donkere randpixel tussen twee zwarte -> zwart ----------
OMENOM=[]
for _ in range(3):
    rand4=nd.binary_dilation(out==0,[[0,1,0],[1,1,1],[0,1,0]])&(out!=0)
    for y,x in zip(*np.where(rand4&np.isin(out,[2,5,10]))):
        if GEZICHT[y,x]: continue
        nbz=[(y+ey,x+ex) for ey in(-1,0,1) for ex in(-1,0,1) if (ey or ex) and rand4[y+ey,x+ex]]
        zw=[p for p in nbz if out[p]==1]; dk=[p for p in nbz if out[p]==out[y,x]]
        if len(zw)>=2 and not dk:
            OMENOM.append((int(x),int(y),int(out[y,x]))); out[y,x]=1
print('om-en-om opgelost:',OMENOM)
# rest (pixels die nergens vielen) melden
rest=(~WIT)&(out==0)
print('niet ingedeeld',int(rest.sum()),list(zip(*np.where(rest)))[:20])
def rgb(o):
    im=P[o].copy(); im[o==0]=255; return im.astype('uint8')
# ---------- opslaan ----------
np.save(S+'gezicht_masker.npy',GEZICHT)
pim=Image.fromarray(out.astype('uint8'),'P')
pal0=[(0x98,0xd0,0xa0)]+PAL[1:]
pim.putpalette([c for p in pal0 for c in p]+[0]*(768-3*len(pal0)))
pim.save(S+'hauntflare_r1.png',transparency=0)
Image.fromarray(rgb(out)).resize((512,512),Image.NEAREST).save(S+'hauntflare_r1_8x.png')
json.dump({'ring_drempels_r4c':RING_T,'gezicht_schaal':SCHAAL,'gezicht_linksboven':[int(dx+gx.min()),int(dy+gy.min())],
           'hand_oranje':HANDORANJE,'buitenrand_selout':SELOUTLOG,'opgeruimd_px':OPGERUIMD,'om_en_om_naar_zwart':OMENOM,
           'kleuren_gebruikt':sorted(int(v) for v in np.unique(out))},open(S+'bouw_log.json','w'))
