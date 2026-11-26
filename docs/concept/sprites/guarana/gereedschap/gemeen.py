# Gedeelde hulpjes guarana fase 1: schaal, overlap natief->sprite, palet, model op spriteschaal, opslaan, labels.
import numpy as np; from PIL import Image
# natief raster 99x99 (pitch 10,24; fase x 9,25 / y 9,35), figuur x14-84, y19-78 (71x60).
# Schaal 44/71 (0,620): figuur 44 breed op x10-53 (gecentreerd zoals Bellsprout/Ekans/Hoppip, midden x 31-32), onderkant y51 (Ekans 51).
S=44/71; U0,V0=14,19; X0,Y0=10,15
MODEL='model.png'; NATIEF='gereedschap/natief.png'; FX,FY,P=9.25,9.35,10.24
# 0 transp | 1 zwart | 2-5 rood (donker lijn/selout, schaduw, midden, licht) | 6-9 groen (donker lijn/selout, schaduw, midden, licht) | 10 oogwit 11 oogwit-schaduw
PAL=[(152,208,160),(16,16,16),
     (112,32,32),(176,56,48),(224,80,56),(240,136,104),
     (48,72,48),(96,124,72),(122,154,88),(150,182,108),
     (248,248,248),(196,200,204)]
ROOD={2,3,4,5}; GROEN={6,7,8,9}; WIT={10,11}
def overlap(X,Y,W=99,H=99):
    ua=(X-X0)/S+U0; ub=ua+1/S; va=(Y-Y0)/S+V0; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))*S*S
            if w>1e-9 and 0<=u<W and 0<=v<H: yield u,v,w
def model_op_schaal(bg=(255,255,255)):
    a=np.asarray(Image.open(NATIEF).convert('RGB')).astype(float); out=np.full((64,64,3),255.)
    for Y in range(64):
        for X in range(64):
            acc=np.zeros(3); tw=0
            for u,v,w in overlap(X,Y): acc+=w*a[v,u]; tw+=w
            if tw: out[Y,X]=acc/tw
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
CH='.Krsml6gGhWw?????'
def toon(o,y0=12,y1=54,x0=6,x1=58):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
