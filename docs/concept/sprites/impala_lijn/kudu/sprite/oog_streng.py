# Ronde 6, strengere ogen (Jordi: B "veel te lief oog"; "alle 4" (A-D) te lief). Alle varianten zwart, zonder oogwit.
# Start = r6/grid.json (oog B). Eerst alle oogpixels van A-D terug naar het lege oogvlak (zelfde regel als r6.py:
# wit uit het model waar >= 30% wit, anders vachttint uit de modelhelderheid), dan de variant.
# Geen pixel getekend: elke pixel komt uit het model (zwartmeting per cel) of 1-op-1 uit een Gen 3-sprite (alleen omgekleurd).
# Gebruik: python3 oog_streng.py  -> r6/kudu_r6_oogS1..S6.png, r6/oog_streng_varianten.png
import json, numpy as np
from PIL import Image, ImageDraw
import oog4
from oog4 import bron
from reduce import fgmask
H,W=64,51; x0,p=91,16
hx=lambda h: tuple(int(h[i:i+2],16) for i in (1,3,5))
PAL={'.':(0,0,0),'0':hx('#302418'),'L':hx('#F8D888'),'M':hx('#D8A850'),'D':hx('#A07030'),
     'l':hx('#D8AC30'),'m':hx('#B08824'),'d':hx('#7C5A10'),'A':hx('#4A4A52'),'3':hx('#8A8A92'),'4':hx('#C8C8CC'),
     'W':hx('#FFFFFF'),'R':hx('#E0A090'),'r':hx('#B06A58'),'K':hx('#5C4434')}
ORDER=list(PAL)
B=[list(r) for r in json.load(open('r6/grid.json'))['grid']]
Am=np.asarray(Image.open('r3/model_A3.png').convert('RGB')).astype(int)
R_,G_,B_=Am[...,0],Am[...,1],Am[...,2]; lum=Am@[.299,.587,.114]
LIJN=lum<70; HAAR=(B_<R_*0.31)&(R_>=110)&~LIJN&(lum<200); VACHT=(~HAAR)&~LIJN&(lum<200)&(R_-B_>60)
from scipy import ndimage as nd
HALO=nd.binary_dilation(lum>=200,iterations=4)
def cel(x,y): return slice(y*p,(y+1)*p),slice(x0+x*p,x0+(x+1)*p)
def vachttoon(x,y,TD=160):
    s=cel(x,y); m=VACHT[s]&~HALO[s]
    if m.sum()<30: m=VACHT[s]
    l=lum[s][m].mean(); return 'L' if l>=181 else 'M' if l>=TD else 'D'
def zwart(x,y): return (lum[cel(x,y)]<60).mean()
LEEG=[r[:] for r in B]; OOGCEL=set()
for v in 'ABCD':
    for x,y,c,_ in oog4.variant(v):
        OOGCEL.add((x,y)); wf=(lum[cel(x,y)]>=215).mean()
        LEEG[y][x]='W' if wf>=0.3 else vachttoon(x,y)
# ---- bouwstenen (allemaal gemeten of 1-op-1) ----
# modelspleet: elke cel waar het model >= 20% zwart heeft (lum < 60) -> 0. Gemeten: (12,21) 26%, (10..13,22) 22/43/37/18%, (11,23) 21%.
MODEL=[(x,y,'0','model: %d%% zwart in de cel'%round(100*zwart(x,y))) for y in range(20,25) for x in range(8,16) if zwart(x,y)>=0.20]
LID22=[(x,22,'0','lid uit het model (rij 22, x 10-13)') for x in range(10,14)]
LID23=[(x,23,'0','modellid 1 rij lager (rij 23, x 10-13)') for x in range(10,14)]
PON={15:'0',14:'K',1:'W'}   # Ponyta: zwart -> 0, donkergrijs 90,90,90 -> K, glans -> W (zelfde kaart als oog B)
def pony(dy): return bron('ponyta',17,25,19,28,PON,-7,dy,'Ponyta')
# Tauros (rechteroog, x24-27 y30-34): schuin lid 74,49,0 -> 0; donkerbruin 106,82,16 -> K; oogwit lavendel 205,197,255 -> 0
# (omgekleurd naar zwart: "kudu irl heeft een zwart oog"); pupil 16,16,16 -> 0; glans -> W
TAU={10:'0',14:'K',3:'0',15:'0',1:'W'}
def tauros(dx,dy,kaart=TAU): return bron('tauros',24,30,27,34,kaart,dx,dy,'Tauros')
def zonder(px,cs): return [t for t in px if (t[0],t[1]) not in cs]
VAR={}
# S1: alleen het model (zwartmeting per cel), geen pupil, geen glans
VAR['S1']=('Modelspleet: alleen het modellid (zwart >= 20% per cel), geen glans', MODEL)
# S2: Ponyta 1 rij hoger (dy -4): haar bovenste rij (eigen lid + glans) valt onder het modellid op rij 22;
#     zichtbaar blijven haar onderste 2 rijen (K K 0 / 0 0). Plus modelplooi (12,21) en (11,23) uit S1.
s2=pony(-4)+MODEL
VAR['S2']=('Modellid + Ponyta-pupil half onder het lid (bovenrij met glans weg), geen glans', s2)
# S3: als S2 + Ponyta-glans (bronpixel (18,26)) verplaatst naar de onderhoek van de pupil: (10,23)
VAR['S3']=('Als S2 + Ponyta-glans in de onderhoek (10,23)', s2+[(10,23,'W','glans: Ponyta bronpixel (18,26), naar de onderhoek van de pupil')])
# S4: modellid 2 rijen dik (rij 22 + 23) over de Ponyta-pupil op de B-plek (dy -3): bovenrij met glans bedekt
VAR['S4']=('Zwaar lid: modellid rij 22 + 23 (1 rij lager erbij) over de B-pupil, geen glans', pony(-3)+[(12,21,'0','modelplooi (12,21) 26% zwart')]+LID22+LID23)
# S5: Tauros-oog 1-op-1 (schuin lid, oogwit naar zwart), geplaatst met de lidpunt (26,30) op de achterkant van het modellid (13,22)
#     -> dx -13, dy -8; glans van Tauros zelf (26,32) blijft
VAR['S5']=('Tauros 1-op-1 (schuin lid; lavendel oogwit -> zwart), eigen glans', tauros(-13,-8))
# S6: als S5 zonder glans (Tauros-glans -> K, de tint van zijn eigen oogrand)
VAR['S6']=('Tauros 1-op-1 zonder glans (glans -> donkerbruin K)', tauros(-13,-8,{**TAU,1:'K'}))
# ---- uitvoer ----
OX=(64-W)//2
def bouw(px):
    g=[r[:] for r in LEEG]
    for x,y,c,_ in px: g[y][x]=c
    return g
def png(G,pad):
    img=np.zeros((64,64),'uint8')
    for y in range(H):
        for x in range(W): img[y,OX+x]=ORDER.index(G[y][x])
    pal=[v for k in ORDER for v in PAL[k]]; pal+=[0]*(48-len(pal))
    im=Image.fromarray(img,'P'); im.putpalette(pal); im.save(pad,transparency=0)
def rgb(G,bg=(170,200,230)):
    a=np.zeros((H,W,3),'uint8')
    for y in range(H):
        for x in range(W): a[y,x]=bg if G[y][x]=='.' else PAL[G[y][x]]
    return a
items=[('B (huidig, ter vergelijking)',B,[])]
log=open('r6/oog_streng_pixels.txt','w')
for k,(t,px) in VAR.items():
    g=bouw(px); png(g,'r6/kudu_r6_oog%s.png'%k)
    diff=[(x,y) for y in range(H) for x in range(W) if g[y][x]!=B[y][x]]
    buiten=[d for d in diff if d not in OOGCEL and d not in {(a,b) for a,b,*_ in px}]
    log.write('%s: %s\n  anders dan B: %d px, buiten oogvlak A-D + variant: %d\n'%(k,t,len(diff),len(buiten)))
    for x,y,c,w in px: log.write('  (%d,%d) %s  %s\n'%(x,y,c,w))
    items.append((k+': '+t,g,px))
log.close()
# vel: per variant hoofd 8x (raster x 0-24, y 12-32) + hele sprite 1x en 2x
Z=8; HX0,HX1,HY0,HY1=0,24,12,32
cw=(HX1-HX0)*Z+20+W*2+20+W+20; ch=(HY1-HY0)*Z+40
V=Image.new('RGB',(2*cw,((len(items)+1)//2)*ch),(255,255,255)); d=ImageDraw.Draw(V)
for i,(t,g,px) in enumerate(items):
    X=(i%2)*cw; Y=(i//2)*ch; a=rgb(g)
    V.paste(Image.fromarray(a[HY0:HY1,HX0:HX1]).resize(((HX1-HX0)*Z,(HY1-HY0)*Z),Image.NEAREST),(X,Y+30))
    full=Image.fromarray(a); xx=X+(HX1-HX0)*Z+20
    V.paste(full.resize((W*2,H*2),Image.NEAREST),(xx,Y+30)); V.paste(full,(xx+W*2+20,Y+30))
    V.paste(Image.fromarray(rgb(g,(40,44,52))),(xx+W*2+20,Y+30+H+10))
    d.text((X,Y+4),t[:95],fill=(0,0,0)); d.text((xx,Y+18),'2x',fill=(90,90,90)); d.text((xx+W*2+20,Y+18),'1x',fill=(90,90,90))
V.save('r6/oog_streng_varianten.png'); print(open('r6/oog_streng_pixels.txt').read())
