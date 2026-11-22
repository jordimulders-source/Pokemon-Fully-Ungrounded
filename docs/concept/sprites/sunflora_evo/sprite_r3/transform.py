# Herhaalt kop_op_r12.py (schaal 1.6) en bewaart de exacte afbeelding r5 -> model_16 en r12 -> model_16.
import numpy as np, json; from PIL import Image; from scipy import ndimage
G='../gemini'
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
s=1.6; f=bw*s/hw; H,W=a.shape[:2]; sz=(int(W*f),int(H*f))
hm=np.array(Image.fromarray((head*255).astype(np.uint8)).resize(sz,Image.NEAREST))>0
hi=np.array(Image.fromarray(a.astype(np.uint8)).resize(sz,Image.NEAREST))
pad=400; C=np.full((b.shape[0]+2*pad,b.shape[1]+2*pad,3),255,np.uint8); C[pad:-pad,pad:-pad]=b
yy,xx=np.where(hm); ty=(yy+by0-hy0*f+pad).astype(int); tx=(xx+bx0-hx0*f+pad).astype(int); C[ty,tx]=hi[yy,xx]
m=(255-C).max(2)>30; Y,X=np.where(m); cy,cx=Y.min()-15,X.min()-15
crop=C[cy:Y.max()+15, cx:X.max()+15]
ref=np.array(Image.open(G+'/model_16.png').convert('RGB'))
d=(crop!=ref[:,:866]).any(2); print('f',f,'afwijkend',d.sum(),np.argwhere(d)[:5])
# r5 (x,y) -> model16: x*f + (bx0-hx0*f+pad-cx) (NEAREST-resize: pixel x_r5 -> [x*f, (x+1)*f))
T={k:float(v) for k,v in dict(f=f,ox=bx0-hx0*f+pad-cx,oy=by0-hy0*f+pad-cy,r12x=pad-cx,r12y=pad-cy).items()}
json.dump(T,open('transform.json','w')); print(T)
np.save('kopmasker_m16.npy',np.pad(np.zeros(1),0)) if False else None
