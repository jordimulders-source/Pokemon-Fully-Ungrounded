# Stap 1: natief raster (pitch 6,40, fase 5,5) van de samenstelling r7 + r5-staart (sprite_r2/samenstelling_onder.png, = r7 met
# de r5-waaier achter de r7-klauwen). Elke natieve cel = de MEEST VOORKOMENDE modelkleur in de cel (kleuren eerst geclusterd
# tot modelkleuren); geen mediaan, geen menging. Uit: natief.npy (labels), natief_pal.npy (RGB per label), natief.png.
import numpy as np; from PIL import Image
from scipy.cluster.vq import kmeans2
a=np.asarray(Image.open('../sprite_r2/samenstelling_onder.png').convert('RGBA')).astype(float)
rgb,al=a[...,:3],a[...,3]>0
fig=rgb[al]; np.random.seed(1)
cent,_=kmeans2(fig[::7],28,minit='++',seed=1,iter=30)
def lab(px): return np.argmin(((px[:,None,:]-cent[None])**2).sum(2),1)
L=np.full(al.shape,-1); L[al]=lab(fig)
P,E=6.4,5.5; x0=E+1-P*np.ceil((E+1)/P)
gr=[x0+k*P for k in range(170) if x0+k*P<1024]
n=len(gr)-1; out=np.full((n,n),-1)
for j in range(n):
    for i in range(n):
        y0,y1=int(np.ceil(gr[j]+1)),int(np.floor(gr[j+1]-1)); xa,xb=int(np.ceil(gr[i]+1)),int(np.floor(gr[i+1]-1))
        b=L[max(y0,0):y1,max(xa,0):xb].ravel()
        if len(b)==0: continue
        v,c=np.unique(b,return_counts=True); out[j,i]=v[np.argmax(c)]
pal=np.clip(cent,0,255).astype(int)
np.save('natief.npy',out); np.save('natief_pal.npy',pal)
img=np.full(out.shape+(3,),255,'uint8'); img[out>=0]=pal[out[out>=0]]
Image.fromarray(img).save('natief.png')
ys,xs=np.where(out>=0); print('natief',out.shape,'figuur x',xs.min(),xs.max(),'y',ys.min(),ys.max())
for k,c in enumerate(pal): print(k,tuple(c),(out==k).sum())
