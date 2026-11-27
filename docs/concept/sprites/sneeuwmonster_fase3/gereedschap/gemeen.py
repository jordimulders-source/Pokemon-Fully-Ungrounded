# Gedeelde hulpjes sauna-yeti (sneeuwmonster fase 3): palet, schaal natief->sprite, opslaan, labels.
# Natief raster 240x130 (natief.py, pitch 5,867). Figuur natief x44-196, y6-127 (153x122 cellen).
# Schaal: 153 cellen -> 62 spritepx (F=2,468 cellen per spritepx); figuur x1-62, onderkant rij 60.
import os, numpy as np; from PIL import Image
D=os.path.dirname(os.path.abspath(__file__)); MODEL=os.path.join(D,'..','model.png'); NATIEF=os.path.join(D,'..','natief.png')
F=153/62.0; MX0=44-1*F; MY0=128-61*F
PAL=[(152,208,160),(24,32,56),
     (62,96,140),(120,156,190),(162,191,222),(208,226,244),(244,250,255),   # 2-6 sneeuw: lijn, schaduw, midden, licht, hoog (= fase 2)
     (132,78,42),(160,104,56),(204,144,88),                                  # 7-9 hout (= fase 2)
     (88,92,104),                                                            # 10 grijs (band, steenfacet; = fase 2)
     (96,140,156),(136,170,180),                                             # 11-12 hand/voet blauwgrijs midden, licht (model)
     (52,50,58),(232,124,44),(244,192,80)]                                   # 13 steen, 14-15 gloed oranje/geel (= fase 2)
SNEEUW={2,3,4,5,6}; HOUT={7,8,9}; HAND={11,12}; STEEN={13,14,15}; GLOED={14,15}
CH='.Klsmhw#dbgaAcoy'
def s2n(X,Y): return MX0+X*F, MY0+Y*F
def rgb(o,bg=None):
    img=np.zeros((64,64,3),'uint8'); img[:]=bg if bg else PAL[0]
    for k in range(1,len(PAL)): img[o==k]=PAL[k]
    return Image.fromarray(img)
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); pl=[v for c in pal for v in c]; p.putpalette(pl+[0]*(768-len(pl))); p.save(path,transparency=0)
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
def toon(o,y0=0,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
K=8   # supersampling van het natieve raster voor oppervlakteweging
def spriteindex():
    """per supersample-cel van het natieve raster: spritepixel-index (of -1)."""
    H,W=130*K,240*K; yy,xx=np.mgrid[0:H,0:W]
    X=np.floor(((xx+0.5)/K-MX0)/F).astype(int); Y=np.floor(((yy+0.5)/K-MY0)/F).astype(int)
    ok=(X>=0)&(X<64)&(Y>=0)&(Y<64); return np.where(ok,Y*64+X,-1)
def up(v): return np.repeat(np.repeat(v,K,0),K,1)
def model_op_schaal():
    a=np.asarray(Image.open(NATIEF).convert('RGB')).astype(float); idx=spriteindex(); ok=idx>=0
    out=np.zeros((4096,3)); n=np.bincount(idx[ok],minlength=4096)
    for ch in range(3): out[:,ch]=np.bincount(idx[ok],up(a[...,ch])[ok],minlength=4096)
    out=out/np.maximum(n,1)[:,None]; out[n==0]=255
    return Image.fromarray(out.reshape(64,64,3).astype('uint8'))
