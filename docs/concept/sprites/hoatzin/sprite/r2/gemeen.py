# Gedeelde hulpjes hoatzin r1: klassen per modelpixel, schaal, overlap model->sprite, palet, opslaan.
# Het model is samengesteld (r6-lijf pitch 10,24; r4-kop x1,1 -> pitch 11,23; teken 75 % + 15 graden, NEAREST),
# dus er is geen enkel natief raster. Verkleinen gebeurt daarom direct per modelpixel (vlakgemiddelde over het
# volle model: elke spritepixel = 16,4 x 16,4 modelpixels), wat voor elk deelraster gelijk is aan via het natieve raster.
import numpy as np; from PIL import Image
import os
HIER=os.path.dirname(os.path.abspath(__file__))
MODEL=os.path.join(HIER,'../../model/model.png')
# figuur in het model: x121-933, y67-1102 (813 x 1036). Hoogte bepaalt de maat: 63 spriterijen (y1-63), voeten onderaan.
MX0,MY0=121,67; MH=1036
S=63/MH            # sprite px per model px (0,0608)
SY0=1
SX0=int(round((64-813*S)/2))
K,D,Y,B,R,W=1,2,3,4,5,6   # klassen: zwart, donker lijf, geelgroen, blauw, rood, wit (glans)
NAMEN={0:'bg',1:'K',2:'D',3:'Y',4:'B',5:'R',6:'W'}
def laad():
    a=np.asarray(Image.open(MODEL).convert('RGB')).astype(float)
    r,g,b=a[...,0],a[...,1],a[...,2]; L=.299*r+.587*g+.114*b
    c=np.zeros(a.shape[:2],int)
    bg=a.min(2)>=225
    sat=a.max(2)-a.min(2)
    c[~bg]=D
    c[(~bg)&(L>=110)]=0   # lichte antialiasrand tegen wit = achtergrond (tenzij hieronder een kleurgroep)
    c[(~bg)&(L<20)]=K
    c[(~bg)&(g-b>30)&(r>55)&(L>=20)]=Y
    c[(~bg)&(b>r+15)&(b>60)]=B
    c[(~bg)&(r>g+60)&(r>90)]=R
    c[(~bg)&(a.min(2)>=150)&(sat<40)&~bg]=W
    return a,c,L
def cel(X,Yy):
    """modelvak (x0,x1,y0,y1) dat spritepixel (X,Yy) bedekt"""
    x0=MX0+(X-SX0)/S; y0=MY0+(Yy-SY0)/S
    return x0,x0+1/S,y0,y0+1/S
def vak(X,Yy,c,L,a=None):
    x0,x1,y0,y1=cel(X,Yy)
    xa,xb=int(np.floor(x0)),int(np.ceil(x1)); ya,yb=int(np.floor(y0)),int(np.ceil(y1))
    xa=max(xa,0); ya=max(ya,0); xb=min(xb,c.shape[1]); yb=min(yb,c.shape[0])
    if xb<=xa or yb<=ya: return None
    wx=np.clip(np.minimum(x1,np.arange(xa,xb)+1)-np.maximum(x0,np.arange(xa,xb)),0,1)
    wy=np.clip(np.minimum(y1,np.arange(ya,yb)+1)-np.maximum(y0,np.arange(ya,yb)),0,1)
    w=wy[:,None]*wx[None,:]
    return c[ya:yb,xa:xb],L[ya:yb,xa:xb],w/w.sum(),(a[ya:yb,xa:xb] if a is not None else None)
# palet: 0 transp | 1 zwart | 2-4 lijf (donker/selout, midden, licht) | 5-7 geelgroen (olijf, midden, licht)
#        8-9 blauw (donker, licht) | 10-11 rood (donker, licht) | 12 wit
PAL=[(152,208,160),(16,16,20),
     (38,44,46),(58,66,66),(90,100,98),
     (96,104,40),(152,168,48),(208,220,84),
     (64,96,160),(116,156,216),
     (136,24,32),(226,58,56),
     (248,248,240)]
LIJF={2,3,4}; GG={5,6,7}; BL={8,9}; RO={10,11}
def opslaan(o,path,pal=None):
    pal=pal or PAL
    p=Image.fromarray(o.astype('uint8'),'P'); fl=[v for c in pal for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(path,transparency=0)
def rgb(o,bg=None,pal=None):
    pal=pal or PAL
    img=np.zeros(o.shape+(3,),'uint8'); img[:]=bg if bg else pal[0]
    for k in range(1,len(pal)): img[o==k]=pal[k]
    return Image.fromarray(img)
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
def model_op_schaal():
    a,c,L=laad(); out=np.full((64,64,3),255.)
    for Yy in range(64):
        for X in range(64):
            v=vak(X,Yy,c,L,a)
            if v is None: continue
            cc,ll,w,aa=v; out[Yy,X]=(aa*w[...,None]).sum((0,1))
    return Image.fromarray(out.astype('uint8'))
CH='.KdmlOgyBbrRW'
def toon(o,y0=0,y1=64,x0=0,x1=64):
    print('   '+''.join(str(x%10) for x in range(x0,x1)))
    for y in range(y0,y1): print('%2d '%y+''.join(CH[v] for v in o[y,x0:x1]))
