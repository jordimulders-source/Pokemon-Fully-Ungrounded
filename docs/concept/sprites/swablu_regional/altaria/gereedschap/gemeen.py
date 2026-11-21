# Gedeelde hulpjes Altaria (onweerswolk): schaal, overlap natief->sprite, palet, model op spriteschaal, opslaan, labels.
import numpy as np; from PIL import Image
# natief raster 199x199 (pitch 5,12 = 1024/200), figuur x15-188, y14-174 (174x161). Schaal 1/3 (gehele 3x3-blokken):
# sprite x3-61, y9-62; onderkant op y62 zoals de game-Altaria (x4-61, y0-62, 1778 px). Blokfase (u≡1, v≡2 mod 3) = minste spreiding binnen de blokken.
S=1/3; U0,V0=13,14; X0,Y0=3,9
MODEL='altaria_model.png'; NATIEF='gereedschap/natief.png'
PX,PHX,PY,PHY=5.12,4.10,5.12,4.10     # rasterpitch/fase uit natief.py
# 0 transp | 1 zwart | 2-5 wolk (donker, midden, licht, hooglicht) | 6-8 violet (donker, midden, licht) | 9 lavendelwit (kuiflicht, oogglans) | 10 static
# Kleuren = k-means-centra van de modelpixels per klasse (bouw.py rekent ze na).
PAL=[(152,208,160),(6,12,28),
     (28,50,81),(50,83,116),(89,139,170),(144,202,221),
     (56,61,139),(94,98,207),(141,145,237),
     (236,240,251),(188,224,237)]
WOLK={2,3,4,5}; VIOLET={6,7,8}
def blok(X,Y):
    u=U0+3*(X-X0); v=V0+3*(Y-Y0); return u,v
def overlap(X,Y,W=199,H=199):
    u,v=blok(X,Y)
    for vv in range(v,v+3):
        for uu in range(u,u+3):
            if 0<=uu<W and 0<=vv<H: yield uu,vv,1/9
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
CH='.K0123abcWs'
def toon(o,y0=8,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
