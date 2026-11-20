# Gedeelde hulpjes Gloom: schaal, overlap natief->sprite, palet, model op spriteschaal, opslaan, labels.
import numpy as np; from PIL import Image
# natief figuur x21-126, y20-121 (106x102). Schaal 42/102: hoogte 42 (y11-52, onderkant als de game-Gloom op y52), x vanaf 9.
S=42/102; U0,V0=21,20; X0,Y0=9,11
MODEL='../referenties/gemini_gekozen_gloom.png'; NATIEF='gereedschap/natief.png'
# 0 transp | 1 zwart | 2-4 steen (donker, midden, licht) | 5-8 lijf (selout, schaduw, midden, licht) | 9-11 gloed (diep, oranje, geel) | 12-14 kelp (bruin, olijf, khaki)
PAL=[(152,208,160),(16,12,12),
     (44,42,44),(74,72,74),(116,114,110),
     (88,28,40),(128,48,64),(166,76,88),(198,108,116),
     (204,74,40),(244,124,48),(252,184,80),
     (78,62,40),(116,100,70),(160,148,110)]
STEEN={2,3,4}; LIJF={5,6,7,8}; GLOED={9,10,11}; KELP={12,13,14}
def overlap(X,Y,W=149,H=149):
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
CH='.K012abcdGOYxoq'
def toon(o,y0=8,y1=56,x0=4,x1=60):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
