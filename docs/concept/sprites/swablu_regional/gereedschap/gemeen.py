# Gedeelde hulpjes Swablu (onweerswolk): schaal, overlap natief->sprite, palet, model op spriteschaal, opslaan, labels.
import numpy as np; from PIL import Image
# natief figuur x74-163, y24-104 (90x81). Schaal 34/81: hoogte 34 (y16-49, onderkant als de game-Swablu op y49), x vanaf 13.
S=34/81; U0,V0=74,24; X0,Y0=13,16
MODEL='model/swablu_model.png'; NATIEF='gereedschap/natief.png'
PX,PHX,PY,PHY=4.267,3.25,4.270,3.00     # rasterpitch/fase uit natief.py
# 0 transp | 1 zwart | 2-7 wolk (selout, donker, midden, licht, lichter, wit) | 8-10 vogel (donker, midden, licht) | 11-13 geel (oker, geel, licht) | 14-15 wit (snavel, glans)
# Alle kleuren = k-means-centra van de modelpixels per klasse (gereedschap/klassen.py).
PAL=[(152,208,160),(13,17,24),
     (56,70,84),(74,87,103),(109,121,137),(138,151,167),(156,169,184),(194,202,214),
     (72,93,111),(107,130,150),(137,159,175),
     (188,166,61),(221,199,90),(252,242,162),
     (211,216,225),(250,251,253)]
WOLK={2,3,4,5,6,7}; VOGEL={8,9,10}; GEEL={11,12,13}; WIT={14,15}
def overlap(X,Y,W=239,H=130):
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
CH='.K012345abcoyYwW'
def toon(o,y0=12,y1=52,x0=8,x1=56):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
