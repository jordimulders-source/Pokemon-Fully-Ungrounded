# natief (pitch 8) -> echte Gemini-pixels (2x2, fase 1,1) -> 64x64 onderlaag. Niets getekend.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief.png').convert('RGB')).astype(int)
H,W=a.shape[:2]; h,w=(H-1)//2,(W-1)//2
o=np.zeros((h,w,3),int); bg=np.zeros((h,w),bool)
for j in range(h):
  for i in range(w):
    blk=a[1+2*j:3+2*j,1+2*i:3+2*i].reshape(-1,3)
    nb=blk[blk.min(1)<215]
    if len(nb)<2: bg[j,i]=True; continue
    o[j,i]=np.median(nb,0)
ys,xs=np.where(~bg); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
print('figuur',x1-x0,'x',y1-y0,'px',(~bg).sum())
out=np.zeros((64,64,4),'uint8')
oy=64-(y1-y0); ox=(64-(x1-x0))//2
sub=o[y0:y1,x0:x1]; sb=bg[y0:y1,x0:x1]
out[oy:oy+y1-y0,ox:ox+x1-x0,:3]=sub; out[oy:oy+y1-y0,ox:ox+x1-x0,3]=np.where(sb,0,255)
im=Image.fromarray(out,'RGBA'); im.save('onderlaag_rgb.png')
q=im.convert('RGB').quantize(15,method=Image.Quantize.MEDIANCUT)
p=np.array(q)+1; p[out[...,3]==0]=0
pal=[255,0,255]+q.getpalette()[:45]
r=Image.fromarray(p.astype('uint8'),'P'); r.putpalette(pal); r.save('onderlaag_q16.png',transparency=0)
r2=Image.open('onderlaag_q16.png').convert('RGBA'); bgw=Image.new('RGBA',(64,64),'white'); bgw.alpha_composite(r2); bgw.resize((512,512),Image.NEAREST).save('onderlaag_q16_8x.png')
