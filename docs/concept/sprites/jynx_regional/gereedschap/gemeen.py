# Gedeelde hulpjes regionale Jynx (van Dundragoon): schaal, overlap natief->sprite, palet, model op spriteschaal, opslaan, labels.
import numpy as np; from PIL import Image
# natief raster 99x99 (pitch 10,24), figuur x15-86, y11-87 (72x77). Schaal 58/77: figuur 54x58 op x5-59, y5-62.
S=58/77; U0,V0=15,11; X0,Y0=5,5
MODEL='gemini/r5.png'; NATIEF='gereedschap/natief.png'
# 0 transp | 1 zwart | 2-5 veren (lijn, schaduw, midden, licht) | 6-8 haar (donker/lijn, schaduw, midden)
# 9-10 gezicht (schaduw, wit) | 11-12 lippen (donker, midden) | 13 tong/mondbinnenkant roze | 14 iris | 15 klauwen
PAL=[(152,208,160),(24,16,16),
     (120,48,24),(176,84,40),(216,118,62),(240,152,96),
     (84,50,28),(124,80,46),(164,114,72),
     (208,200,196),(248,248,244),
     (96,28,48),(144,54,74),(216,138,138),
     (160,64,60),(100,80,64)]
VEER={2,3,4,5}; HAAR={6,7,8}; GEZ={9,10}; LIP={11,12,13}; OOG={14}; KLAUW={15}
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
CH='.Klsm+DSHgWMRpeL'
def toon(o,y0=8,y1=56,x0=4,x1=60):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
