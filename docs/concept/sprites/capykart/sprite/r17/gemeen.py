# Gedeelde hulpjes Capykart r17 (Dundragoon-methode): schaal, overlap natief->sprite, palet, opslaan, labels.
import numpy as np; from PIL import Image
# natief raster 99x99 (pitch 10,24, fase 9,20), figuur x12-84, y11-82 (73x72). Schaal 62/73: figuur 62 breed op x1-62.
S=62/73; U0,V0=12,11; X0,Y0=1,2
MODEL='referenties/model_r5.png'; NATIEF='sprite/r17/natief.png'
# 0 transp | 1 zwart | 2-6 bruin (lijn, schaduw, midden, licht, hoog) | 7-8 hoepel (licht, donker) | 9 geel | 10-11 rood (licht, donker)
# 12-14 blauw (boven, licht, donker) | 15-16 groen (licht, donker)
PAL=[(152,208,160),(24,17,28),
     (112,53,43),(164,88,56),(183,107,67),(214,125,77),(221,145,95),
     (142,142,146),(76,74,84),
     (240,208,84),
     (246,99,90),(205,61,65),
     (122,172,222),(87,140,202),(76,109,168),
     (92,163,92),(74,135,83)]
BRUIN={2,3,4,5,6}; HOEPEL={7,8}; GEEL={9}; ROOD={10,11}; BLAUW={12,13,14}; GROEN={15,16}
GROEPEN=[BRUIN,HOEPEL,GEEL,ROOD,BLAUW,GROEN]
def groep(k):
    for g in GROEPEN:
        if k in g: return g
    return {k}
SEL={2:2,3:2,4:2,5:2,6:2,7:8,8:8,9:2,10:11,11:11,12:14,13:14,14:14,15:16,16:16}
def overlap(X,Y,W=99,H=99):
    ua=(X-X0)/S+U0; ub=ua+1/S; va=(Y-Y0)/S+V0; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))*S*S
            if w>1e-9 and 0<=u<W and 0<=v<H: yield u,v,w
def model_op_schaal():
    a=np.asarray(Image.open(NATIEF).convert('RGB')).astype(float); out=np.full((64,64,3),255.)
    for Y in range(64):
        for X in range(64):
            acc=np.zeros(3); tw=0
            for u,v,w in overlap(X,Y): acc+=w*a[v,u]; tw+=w
            if tw: out[Y,X]=acc/tw
    return Image.fromarray(out.astype('uint8'))
def rgb(o,bg=None,pal=None):
    pal=pal or PAL; img=np.zeros((64,64,3),'uint8'); img[:]=bg if bg else pal[0]
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); fl=[v for c in pal for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(path,transparency=0)
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
CH='.K23456hHyrRbBLgG'
def toon(o,y0=0,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
