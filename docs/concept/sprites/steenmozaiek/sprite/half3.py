# natief -> 2x2-reductie: omlijning alleen op de buitenrand, voegen als 1 px in een eigen donkere voegkleur,
# vulling = meest voorkomende paletkleur in het blok (geen gemiddelde). Niets getekend.
import sys; from PIL import Image; import numpy as np
from scipy import ndimage as nd
IN,UIT=sys.argv[1],sys.argv[2]; OY=int(sys.argv[3]); OX=int(sys.argv[4]); NF=int(sys.argv[5]) if len(sys.argv)>5 else 11
a=np.asarray(Image.open(IN).convert('RGB')).astype(int); H,W=a.shape[:2]
bg=a.min(axis=2)>=215
bg=~nd.binary_fill_holes(~bg)|bg&False
bg=a.min(axis=2)>=215
lum=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
drk=(lum<62)&~bg
body=nd.binary_fill_holes(~bg)
near_bg=nd.binary_dilation(~body,iterations=2)
outl=drk&near_bg; seam=drk&~near_bg
fillm=~bg&~drk
q=Image.fromarray(a[fillm].reshape(1,-1,3).astype('uint8')).quantize(NF,method=Image.Quantize.MAXCOVERAGE,kmeans=4)
pal=np.array(q.getpalette()[:NF*3]).reshape(-1,3)
order=np.argsort(0.299*pal[:,0]+0.587*pal[:,1]+0.114*pal[:,2]); pal=pal[order]
lab=np.full((H,W),-1)
d=((a[fillm][:,None,:]-pal[None])**2).sum(2); lab[fillm]=np.argmin(d,1)
h=(H-OY)//2; w=(W-OX)//2; o=np.zeros((h,w),int)
bodyS=np.zeros((h,w),bool)
for j in range(h):
    for i in range(w):
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2))
        if body[sl].sum()>=2: bodyS[j,i]=True
edgeS=bodyS&~nd.binary_erosion(bodyS)
for j in range(h):
    for i in range(w):
        if not bodyS[j,i]: continue
        sl=(slice(OY+2*j,OY+2*j+2),slice(OX+2*i,OX+2*i+2))
        if edgeS[j,i]: o[j,i]=1; continue
        L=lab[sl]; L=L[L>=0]
        if seam[sl].sum()>=2 or L.size==0: o[j,i]=2; continue
        v,c=np.unique(L,return_counts=True); o[j,i]=3+v[np.argmax(c)]
ys,xs=np.where(o>0); o2=o[ys.min():ys.max()+1,xs.min():xs.max()+1]; hh,ww=o2.shape
full=np.zeros((64,64),int); x0=(64-ww)//2; full[63-hh:63,x0:x0+ww]=o2
PAL=[(255,0,255),(20,14,22),(58,40,52)]+[tuple(int(v) for v in c) for c in pal]
p=Image.fromarray(full.astype('uint8'),'P'); fl=[v for c in PAL for v in c]; p.putpalette(fl+[0]*(768-len(fl))); p.save(UIT,transparency=0)
tot=(full>0).sum(); print(UIT,ww,hh,tot,'omlijning %.1f%% voeg %.1f%%'%(100*(full==1).sum()/tot,100*(full==2).sum()/tot),'kleuren',len(set(full.ravel()))-1)
