# Gedeelde hulpjes regionale Starmie: schaal, overlap natief->sprite, klassen, palet, opslaan, labels.
import sys, numpy as np; from PIL import Image
sys.path.insert(0,'gereedschap')
from voor import natief, figuur, voor_mask
from gen3 import laad as laad_g3, punt_van, SETB
# Natief raster 99x99 (pitch 10,24, fase 9,25). Voorste ster natief x12-86, y12-84.
# Schaal 0,66 (gekozen uit 0,62-0,70: figuur 54x52 / 1648 px, Gen 3 Starmie 55x51 / 1673 px).
# Juweelmidden model natief (50,49) -> sprite (31,30), kern Gen 3 = (31.5,30).
S=0.66; GEM=(50,49); CX,CY=31.0,30.0
MODEL='referenties/model_r3.png'; NATIEF='gereedschap/natief.png'
# 0 transp | 1 zwart | 2-6 koek (donker lijn/chip, schaduw, oranje, midden, licht) | 7-10 paars (lijn, donker, midden, licht)
# 11 wit | 12 rood 13 groen 14 blauw 15 geel (hagelslag)
PAL=[(152,208,160),(24,16,16),
     (116,58,24),(178,102,40),(214,136,62),(236,182,100),(250,220,152),
     (76,34,92),(132,70,156),(172,112,198),(214,168,232),
     (252,252,252),(228,44,44),(72,196,64),(44,124,220),(250,214,40)]
KOEK={2,3,4,5,6}; PAARS={7,8,9,10}; HAGEL={12,13,14,15}
def overlap(X,Y,W=99,H=99):
    ua=(X-CX)/S+GEM[0]; ub=ua+1/S; va=(Y-CY)/S+GEM[1]; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))*S*S
            if w>1e-9 and 0<=u<W and 0<=v<H: yield u,v,w
def klasse(c):
    r,g,b=[int(v) for v in c]; L=(r+g+b)/3
    if min(r,g,b)>=212: return 'wit'
    if r>200 and g<90 and b<90: return 'rood'
    if g>r+40 and g>b+20: return 'groen'
    if b>r+50 and b>g+30 and r<120: return 'blauw'
    if r>225 and g>190 and b<90: return 'geel'
    if b>g+25 and r>g+10: return 'plijn' if L<85 else 'paars'
    if L<60: return 'zwart'
    return 'koek'
def model_op_schaal():
    a=natief().astype(float); out=np.full((64,64,3),255.)
    for Y in range(64):
        for X in range(64):
            acc=np.zeros(3); tw=0
            for u,v,w in overlap(X,Y): acc+=w*a[v,u]; tw+=w
            if tw: out[Y,X]=acc/tw*min(1,tw)+255*(1-min(1,tw))
    return Image.fromarray(out.astype('uint8'))
def rgb(o,bg=None):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path):
    p=Image.fromarray(o.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; p.putpalette(pal+[0]*(768-len(pal))); p.save(path,transparency=0)
def label(mask,acht=True):
    lab=np.zeros(mask.shape,int); n=0
    nb=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] if acht else [(-1,0),(1,0),(0,-1),(0,1)]
    for y,x in zip(*np.where(mask)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in nb:
                yy,xx=cy+dy,cx+dx
                if 0<=yy<mask.shape[0] and 0<=xx<mask.shape[1] and mask[yy,xx] and not lab[yy,xx]: lab[yy,xx]=n; st.append((yy,xx))
    return lab,n
CH='.#DSOMLpdmlWrgby'
def toon(o,y0=4,y1=60,x0=3,x1=62):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
