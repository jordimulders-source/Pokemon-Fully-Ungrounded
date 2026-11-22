"""Plak het r5-hoofd op het r12-lijf. Gebruik: kop_op_r12.py uit.png schaal1 schaal2 ...
schaal = breedte r5-hoofd / breedte r12-hoofd; gezichtsmiddens vallen samen."""
import sys; from PIL import Image, ImageDraw; import numpy as np
from scipy import ndimage
G=__file__.rsplit('/',2)[0]
a=np.array(Image.open(G+'/r5.png').convert('RGB')).astype(int)
nw=a.sum(2)<720; g=(a[:,:,1]>a[:,:,0]+15)&(a[:,:,1]>a[:,:,2])
head=nw&~g&~((a.sum(2)<150)&ndimage.binary_dilation(g,iterations=4)); head[365:]=False
lab,n=ndimage.label(head); head=lab==(np.argmax(ndimage.sum(head,lab,range(1,n+1)))+1)
head=ndimage.binary_fill_holes(head)
def facec(img,mask):
    f=(img[:,:,0]>230)&(img[:,:,1]>205)&(img[:,:,2]>110)&(img[:,:,2]<215)&mask
    lab,n=ndimage.label(f); f=lab==(np.argmax(ndimage.sum(f,lab,range(1,n+1)))+1)
    ys,xs=np.where(f); return (xs.min()+xs.max())/2,(ys.min()+ys.max())/2
hx0,hy0=facec(a,head); hy,hx=np.where(head); hw=hx.max()-hx.min()
b=np.array(Image.open(G+'/r12.png').convert('RGB')).astype(int)
yel=(b[:,:,0]>150)&(b[:,:,1]>120)&(b[:,:,2]<170)&(b[:,:,0]>b[:,:,1]-10); yel[650:]=False
kop12=ndimage.binary_fill_holes(ndimage.binary_closing(yel,iterations=3))
bx0,by0=facec(b,kop12); ky,kx=np.where(kop12); bw=kx.max()-kx.min()
out=[]
for s in map(float,sys.argv[2:]):
    f=bw*s/hw; H,W=a.shape[:2]; sz=(int(W*f),int(H*f))
    hi=np.array(Image.fromarray(a.astype(np.uint8)).resize(sz,Image.NEAREST))
    hm=np.array(Image.fromarray((head*255).astype(np.uint8)).resize(sz,Image.NEAREST))>0
    pad=400; C=np.full((b.shape[0]+2*pad,b.shape[1]+2*pad,3),255,np.uint8); C[pad:-pad,pad:-pad]=b
    yy,xx=np.where(hm); ty=(yy+by0-hy0*f+pad).astype(int); tx=(xx+bx0-hx0*f+pad).astype(int)
    C[ty,tx]=hi[yy,xx]
    m=(255-C).max(2)>30; yy,xx=np.where(m)
    c=Image.fromarray(C[yy.min()-15:yy.max()+15, xx.min()-15:xx.max()+15]); ImageDraw.Draw(c).text((4,4),f'{s}x',fill='black'); out.append(c)
h=max(o.height for o in out); v=Image.new('RGB',(sum(o.width for o in out)+30*len(out),h),'white'); x=0
for o in out: v.paste(o,(x,h-o.height)); x+=o.width+30
v.save(sys.argv[1])
