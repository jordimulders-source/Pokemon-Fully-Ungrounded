# Maattest: r1_B (64 natief) verkleind met vlakgemiddelde (poedelmot sil.py: alpha >= 0.45), daarna elke pixel naar de dichtstbijzijnde B-paletkleur. Alleen om de maat te kiezen; geen eindsprite.
from PIL import Image; import numpy as np
src=Image.open('sprite/r1_B.png'); o=np.array(src); pal=np.array(src.getpalette()[:48]).reshape(16,3).astype(float)
rgb=pal[o]; alpha=(o!=0).astype(float)
ys,xs=np.where(o!=0); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
rgb=rgb[y0:y1,x0:x1]; alpha=alpha[y0:y1,x0:x1]; w0,h0=x1-x0,y1-y0
def verklein(w):
    h=round(h0*w/w0)
    pre=Image.fromarray((rgb*alpha[...,None]).astype(np.float32).mean(2)) # dummy
    R=np.stack([np.array(Image.fromarray((rgb[...,c]*alpha).astype(np.float32)).resize((w,h),Image.BOX)) for c in range(3)],-1)
    A=np.array(Image.fromarray(alpha.astype(np.float32)).resize((w,h),Image.BOX))
    C=R/np.maximum(A,1e-6)[...,None]
    d=((C[:,:,None,:]-pal[None,None,1:])**2).sum(-1); idx=d.argmin(-1)+1
    idx[A<0.45]=0
    out=np.zeros((64,64),np.uint8); ox=(64-w)//2; oy=64-h-4
    out[oy:oy+h,ox:ox+w]=idx
    return out,w,h
vel=Image.new('RGB',(3*528,600),'white')
for k,w in enumerate((40,46,52)):
    out,w,h=verklein(w)
    im=Image.fromarray(pal.astype(np.uint8)[out]); a=np.array(im); a[out==0]=255; im=Image.fromarray(a)
    vel.paste(im.resize((512,512),Image.NEAREST),(k*528,0)); vel.paste(im,(k*528,525))
    print(w,h,'px',int((out!=0).sum()))
vel.save('sprite/maattest_vel.png')
