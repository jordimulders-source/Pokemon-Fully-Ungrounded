# vel.png r2: r2 | r1 | model op 8x; benen en armen op 12x: r2 | r1 | model
import numpy as np; from PIL import Image, ImageDraw
from palet import PAL
z=np.load('reductie.npz'); xs,ys=z['xs'],z['ys']
r2=np.load('r2_a1.npy'); r1=np.load('../sprite_r1/r1_a1.npy'); H,W=r2.shape
mod=Image.open('../referenties/gemini_gekozen_v1.png').convert('RGB')
def rgb(a):
    o=np.zeros(a.shape+(3,),'uint8'); o[:]=255
    for k in range(1,16): o[a==k]=PAL[k]
    return Image.fromarray(o)
def mc(c0,c1,r0,r1_,w,h): return mod.crop((int(xs[c0]),int(ys[r0]),int(xs[c1+1]),int(ys[r1_+1]))).resize((w,h),Image.LANCZOS)
def rij(ims,gap=16):
    c=Image.new('RGB',(sum(i.size[0]+gap for i in ims),max(i.size[1] for i in ims)),'white'); x=0
    for i in ims: c.paste(i,(x,0)); x+=i.size[0]+gap
    return c
def drie(c0,c1,r0,r1_,s):
    w,h=(c1-c0+1)*s,(r1_-r0+1)*s
    return rij([rgb(a[r0:r1_+1,c0:c1+1]).resize((w,h),Image.NEAREST) for a in (r2,r1)]+[mc(c0,c1,r0,r1_,w,h)])
rows=[('8x: r2 | r1 | model',drie(0,W-1,0,H-1,8)),
      ('benen 12x: r2 | r1 | model',drie(6,44,28,46,12)),
      ('armen/schouders 12x: r2 | r1 | model',drie(4,49,11,31,12))]
Wt=max(i.size[0] for _,i in rows); Ht=sum(i.size[1]+30 for _,i in rows)
v=Image.new('RGB',(Wt,Ht),'white'); d=ImageDraw.Draw(v); y=0
for t,i in rows: d.text((4,y+8),t,fill=0); v.paste(i,(0,y+26)); y+=i.size[1]+30
v.save('vel.png'); print(v.size)
