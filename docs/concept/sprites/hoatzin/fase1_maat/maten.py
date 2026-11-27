# Kale verkleining van Gemini fase1_r4 naar een paar maten (geen hertekenen).
import sys, numpy as np
from PIL import Image
src = np.array(Image.open('../gemini/fase1_r4.png').convert('RGB')).astype(int)
best=None
for p in np.arange(9.6,10.6,0.01):
  for o in np.arange(0,p,0.5):
    xs=(o+np.arange(int((1024-o)/p))*p).astype(int)
    d=np.abs(np.diff(src.sum(2)[:,xs],axis=1)).sum()
    if best is None or d<best[0]: best=(d,p,o)
_,p,o=best
n=int((1024-o)/p); c=(o+p/2+np.arange(n)*p).astype(int); c=c[c<1024]
nat=src[np.ix_(c,c)]
mask=nat.sum(2)<720
ys,xs=np.nonzero(mask); nat=nat[ys.min():ys.max()+1, xs.min():xs.max()+1]; mask=mask[ys.min():ys.max()+1, xs.min():xs.max()+1]
print('pitch',round(p,2),'natief',nat.shape[1],'x',nat.shape[0],'px',mask.sum())
def red(h):
    H,W=mask.shape; w=round(W*h/H); out=np.zeros((h,w,4),np.uint8)
    for y in range(h):
      for x in range(w):
        y0,y1=int(y*H/h),max(int((y+1)*H/h),int(y*H/h)+1); x0,x1=int(x*W/w),max(int((x+1)*W/w),int(x*W/w)+1)
        mm=mask[y0:y1,x0:x1]
        if mm.mean()>=0.4:
          blk=nat[y0:y1,x0:x1][mm]; v=blk[np.argmin(blk.sum(1))] if (blk.sum(1)<150).mean()>0.3 else np.median(blk,0)
          out[y,x,:3]=v; out[y,x,3]=255
    return out
vel=Image.new('RGBA',(4*64*6+30,64*6),'white'); x=0
imgs=[('natief',np.dstack([nat,np.where(mask,255,0)]).astype(np.uint8))]+[(f'h{h}',red(h)) for h in (56,50,44)]
for nm,im in imgs:
    a=im[...,3]>0; print(nm,im.shape[1],'x',im.shape[0],'px',a.sum())
    I=Image.fromarray(im); Image.fromarray(im).save(f'{nm}.png')
    can=Image.new('RGBA',(64,64),(255,255,255,0)); 
    if im.shape[0]<=64 and im.shape[1]<=64: can.paste(I,((64-im.shape[1])//2,64-im.shape[0]))
    else: can=I.resize((64,64))
    vel.paste(can.resize((384,384),Image.NEAREST),(x,0),can.resize((384,384),Image.NEAREST)); x+=394
vel.save('maten_vel.png')
