# Kale reductie v2: elke modelpixel krijgt een materiaal; per spritecel (vast raster, pitch P, fase met de hoogste zuiverheid)
# wint het meerderheidsmateriaal, tint = gemiddelde helderheid van dat materiaal in de cel -> dichtstbijzijnde paletkleur. Niets getekend.
import numpy as np; from PIL import Image
from palet import PAL
a=np.asarray(Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')).astype(int)
R,G,B=a[...,0],a[...,1],a[...,2]; L=(R*299+G*587+B*114)/1000; sat=a.max(2)-a.min(2)
H0,W0=L.shape
light=(L>=225)&(sat<30)
# lucht = lichte pixels verbonden met de rand (flood fill)
air=np.zeros((H0,W0),bool); st=[(0,0),(0,W0-1),(H0-1,0),(H0-1,W0-1)]
while st:
    j,i=st.pop()
    if j<0 or i<0 or j>=H0 or i>=W0 or air[j,i] or not light[j,i]: continue
    air[j,i]=True; st+=[(j+1,i),(j-1,i),(j,i+1),(j,i-1)]
mat=np.full((H0,W0),4)  # 0 lucht 1 geel 2 rood 3 ijs 4 donker
mat[(B-R>10)&(L>=100)]=3
mat[(L>=200)&(sat<40)]=3
mat[(R>140)&(G>110)&(B<120)&(R-B>50)]=1
mat[(R>130)&(R-G>50)&(R-B>40)]=2
mat[air]=0

P=15.36
def grid(ox,oy):
    xs=np.arange(ox,W0,P); ys=np.arange(oy,H0,P); return xs,ys
def purity(ox,oy):
    xs,ys=grid(ox,oy); s=0;n=0
    for y in ys[:-1]:
        for x in xs[:-1]:
            blk=mat[int(y):int(y+P),int(x):int(x+P)]
            c=np.bincount(blk.ravel(),minlength=5)
            if c[1:].sum()==0: continue
            s+=c.max()/c.sum(); n+=1
    return s/n
best=max(((purity(ox,oy),ox,oy) for ox in np.arange(0,P,1.0) for oy in np.arange(0,P,1.0)))
print('zuiverheid %.3f fase %.1f %.1f'%best)
_,ox,oy=best; xs,ys=grid(ox,oy)
Hc,Wc=len(ys)-1,len(xs)-1
cls=np.zeros((Hc,Wc),int); lum=np.zeros((Hc,Wc)); col=np.zeros((Hc,Wc,3)); frac=np.zeros((Hc,Wc,5))
for j in range(Hc):
    for i in range(Wc):
        sl=(slice(int(ys[j]),int(ys[j+1])),slice(int(xs[i]),int(xs[i+1])))
        blk=mat[sl]; c=np.bincount(blk.ravel(),minlength=5); frac[j,i]=c/c.sum()
        if c[1:].sum()<0.45*c.sum(): continue
        k=1+int(np.argmax(c[1:])); cls[j,i]=k
        m=blk==k; lum[j,i]=L[sl][m].mean(); col[j,i]=a[sl][m].mean(0)
yy,xx=np.where(cls>0); y0,y1,x0,x1=yy.min(),yy.max(),xx.min(),xx.max()
sl=(slice(y0,y1+1),slice(x0,x1+1))
cls,lum,col,frac=cls[sl],lum[sl],col[sl],frac[sl]
np.savez('reductie.npz',cls=cls,lum=lum,col=col,frac=frac,xs=xs[x0:x1+2],ys=ys[y0:y1+2])
grp={1:[5,6,7],2:[12,13,14],3:[8,9,10,11],4:[1,2,3,4]}
out=np.zeros(cls.shape,'uint8')
for j in range(cls.shape[0]):
    for i in range(cls.shape[1]):
        k=cls[j,i]
        if k: out[j,i]=min(grp[k],key=lambda p:((np.array(PAL[p])-col[j,i])**2).sum())
np.save('kaal.npy',out); print('maat',out.shape[1],'x',out.shape[0])
print('   '+''.join(str(i%10) for i in range(out.shape[1])))
for j,r in enumerate(out): print('%2d '%j+''.join('.' if v==0 else '%x'%v for v in r))
