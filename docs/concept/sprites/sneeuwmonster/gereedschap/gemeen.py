# Gedeelde hulpjes sneeuwmonster (gekopieerd van Dundragoon): schaal, overlap natief->sprite, palet, model op spriteschaal, opslaan, labels.
import numpy as np; from PIL import Image
# natief raster 99x99 (pitch 10,24), figuur x27-70, y16-81 (44x66). Schaal 42/66: figuur 28x42 op x18-45, y11-52 (maat Snorunt/Wynaut).
S=42/66; U0,V0=27,16; X0,Y0=18,11
MODEL='gemini/r1/r1c.png'; NATIEF='gereedschap/natief.png'
# 0 transp | 1 omlijning | 2-5 sneeuw (lijn/selout, schaduw, midden, licht) | 6-8 steen (donker, midden, licht)
PAL=[(152,208,160),(24,32,56),
     (88,124,164),(172,200,228),(214,232,246),(244,250,255),
     (48,50,60),(86,88,102),(130,132,146)]
SNEEUW={2,3,4,5}; STEEN={6,7,8}
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
CH='.Klsmwdpg????????'
def toon(o,y0=8,y1=56,x0=4,x1=60):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
