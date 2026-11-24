# skelet2.py: skelet van alleen de dikke (structurele) modellijnen, korte stukjes weg, per spritepixel de lengte
import numpy as np
from PIL import Image, ImageFilter
exec(open('lijnen.py').read().split('sk=zs(lines)')[0])
li=Image.fromarray((lines*255).astype('uint8'))
op=np.asarray(li.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5)))>0
thick=lines&(np.asarray(Image.fromarray((op*255).astype('uint8')).filter(ImageFilter.MaxFilter(3)))>0)
# deur (L<45) telt ook als lijnmassa: niet meenemen; alleen lijnen
sk=zs(thick)
# componenten (8-buren) korter dan 30 px weg
H,W=sk.shape; seen=np.zeros_like(sk); keep=np.zeros_like(sk)
ys,xs=np.where(sk)
for y0,x0 in zip(ys,xs):
    if seen[y0,x0]: continue
    st=[(y0,x0)]; seen[y0,x0]=1; comp=[]
    while st:
        y,x=st.pop(); comp.append((y,x))
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                yy,xx=y+dy,x+dx
                if 0<=yy<H and 0<=xx<W and sk[yy,xx] and not seen[yy,xx]: seen[yy,xx]=1; st.append((yy,xx))
    if len(comp)>=30:
        for p in comp: keep[p]=1
d=np.load('red.npz'); s=float(d['s']); top=int(d['top']); left=int(d['left'])
X0,Y0=46,57
cnt=np.zeros((64,64))
for y,x in zip(*np.where(keep)):
    by=int((y-Y0)/s); bx=int((x-X0)/s)
    if 0<=by<60 and 0<=bx<62: cnt[top+by,left+bx]+=1
np.save('skthick.npy',cnt)
L=np.asarray(Image.open(M).convert('L'))
o=np.stack([L]*3,-1).copy(); o[thick]=[255,150,150]; o[keep]=[255,0,0]
Image.fromarray(o).save('skelet_dik.png')
