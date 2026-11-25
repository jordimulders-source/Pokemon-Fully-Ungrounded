# Schuift de staart (los onderdeel) k natieve px naar links, achter het lijf. Niets hertekend.
# Gebruik: python3 model/compact.py k
import sys, numpy as np, colorsys; from PIL import Image
from scipy import ndimage
k=int(sys.argv[1])
a=np.asarray(Image.open('plak/r10_natief.png').convert('RGB')).copy()
H,W,_=a.shape
def hsv(p): return colorsys.rgb_to_hsv(*(p/255))
bg=a.min(2)>225
xs=np.arange(W)[None,:].repeat(H,0)
core=np.zeros((H,W),bool)
for y in range(H):
    for x in range(64,W):
        if bg[y,x]: continue
        h,s,v=hsv(a[y,x].astype(float))
        core[y,x]=(h<0.065 and s>0.6 and v>0.45) or (s<0.15 and v>0.6)
far=(~bg)&(xs>=77)                      # rechts van x=77 is alles staart
lab,n=ndimage.label(core|far); sz=ndimage.sum(core|far,lab,range(1,n+1)); tail=lab==(1+int(np.argmax(sz)))
dark=(a.max(2)<110)&~bg
edge=ndimage.binary_dilation(tail,iterations=1)&dark   # omlijning van de staart
tail_full=tail|edge
remove=tail_full&~(edge&(xs<77))        # gedeelde lijfrand blijft staan
layer=np.where(tail_full[...,None],a,255)
base=a.copy(); base[remove]=255
shift=np.full_like(a,255); m2=np.zeros((H,W),bool)
shift[:,:W-k]=layer[:,k:]; m2[:,:W-k]=tail_full[:,k:]
out=base.copy(); behind=m2&(base.min(2)>225)
out[behind]=shift[behind]
Image.fromarray(out).save(f'model/r10_k{k}.png')
m=out.min(2)<225; yy,xx=np.where(m); w=xx.max()-xx.min()+1; h=yy.max()-yy.min()+1
print(k,'figuur',w,h,'factor',round(64/max(w,h),3))
crop=Image.fromarray(out[yy.min():yy.max()+1,xx.min():xx.max()+1])
crop.resize((w*6,h*6),Image.NEAREST).save(f'model/r10_k{k}_6x.png')
