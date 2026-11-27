# Gedeelde hulpjes sneeuwmonster fase 2: palet, modelklassen, schaal model->sprite, opslaan, labels.
# Model 1024x559, natief raster 4,27 px (1024/240; pitch.py), stenen geplakt op ±3,7 px. Figuur x290-725, y24-533.
# Schaal: 510 modelrijen -> 56 spriterijen (9,107 modelpx per spritepx); figuur 48x56 op x8-55, y3-58.
import numpy as np; from PIL import Image
import os; MODEL=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','model.png')
F=510/56.0; MX0,MY0=290-8*F+ (0), 24-3*F   # modelcoord van spritepixel (0,0) linksboven
PAL=[(152,208,160),(24,32,56),
     (72,108,136),(118,158,186),(160,194,214),(204,228,240),(240,250,252),   # 2-6 sneeuw: lijn, schaduw, midden, licht, hoog
     (104,60,32),(160,104,56),(204,144,88),                                  # 7-9 hout
     (88,92,104),(160,166,176),                                              # 10-11 grijs (band, ogen)
     (52,50,58),(216,72,32),(240,136,40),(248,208,64)]                       # 12 steen, 13-15 gloed rood/oranje/geel
SNEEUW={2,3,4,5,6}; HOUT={7,8,9}; GRIJS={10,11}; STEEN={12,13,14,15}
CH='.Klsmhw#dbgGcroy'
STEENZONE=(395,300,492,462)   # x0,y0,x1,y1 in het model
def m2s(x,y): return (x-MX0)/F,(y-MY0)/F
def s2m(X,Y): return MX0+X*F, MY0+Y*F
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
def toon(o,y0=0,y1=64,x0=4,x1=60):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
def model_op_schaal():
    a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float)
    H,W=a.shape[:2]; yy,xx=np.mgrid[0:H,0:W]
    X=np.floor((xx-MX0)/F).astype(int); Y=np.floor((yy-MY0)/F).astype(int)
    ok=(X>=0)&(X<64)&(Y>=0)&(Y<64); idx=(Y*64+X)[ok]
    out=np.zeros((4096,3)); n=np.bincount(idx,minlength=4096)
    for c in range(3): out[:,c]=np.bincount(idx,a[...,c][ok],minlength=4096)
    out=out/np.maximum(n,1)[:,None]; out[n==0]=255
    return Image.fromarray(out.reshape(64,64,3).astype('uint8'))
