"""Schaal het sterhoofd van r5 rond het onderste midden; lijf blijft gelijk. Gebruik: kop_schaal.py uit.png s1 s2 ..."""
import sys; from PIL import Image, ImageDraw; import numpy as np
from scipy import ndimage
a=np.array(Image.open(__file__.rsplit('/',2)[0]+'/r5.png').convert('RGB')).astype(int)
nw=a.sum(2)<720
g=(a[:,:,1]>a[:,:,0]+15)&(a[:,:,1]>a[:,:,2])
head=nw&~g&~((a.sum(2)<150)&ndimage.binary_dilation(g,iterations=4)); head[365:]=False
lab,n=ndimage.label(head); head=lab==(np.argmax(ndimage.sum(head,lab,range(1,n+1)))+1)
head=ndimage.binary_fill_holes(head); body=nw&~head
H,W=a.shape[:2]; out=[]
for s in map(float,sys.argv[2:]):
    off=int(H*(s-1)); C=np.full((H+off,W,3),255,np.uint8); C[off:][body]=a[body]
    ys,xs=np.where(head); cx=(xs.min()+xs.max())/2; by=ys.max()
    sz=(int(W*s),int(H*s))
    hi=np.array(Image.fromarray(a.astype(np.uint8)).resize(sz,Image.NEAREST))
    hm=np.array(Image.fromarray((head*255).astype(np.uint8)).resize(sz,Image.NEAREST))>0
    yy,xx=np.where(hm); ty=yy+int(off+by-by*s); tx=xx+int(cx-cx*s); ok=(ty>=0)&(ty<C.shape[0])&(tx>=0)&(tx<W)
    C[ty[ok],tx[ok]]=hi[yy[ok],xx[ok]]
    m=(255-C).max(2)>30; yy,xx=np.where(m)
    c=Image.fromarray(C[yy.min()-20:yy.max()+20, max(0,xx.min()-20):xx.max()+20])
    ImageDraw.Draw(c).text((5,5),f'{s}x',fill='black'); out.append(c)
h=max(o.height for o in out); v=Image.new('RGB',(sum(o.width for o in out)+30*len(out),h),'white'); x=0
for o in out: v.paste(o,(x,h-o.height)); x+=o.width+30
v.save(sys.argv[1])
