# Zonekaart "was groen in het model" (kop en staart) uit het verkleinde model (sprite_r1/model_verkleind63.png),
# gladgestreken met een 3x3-meerderheid binnen het silhouet. Uitvoer: groenzone.npy (63x63 bool) + zones_8x.png.
import numpy as np, colorsys
from PIL import Image
a=np.asarray(Image.open('../sprite_r1/model_verkleind63.png').convert('RGBA')).astype(int)
H,W=63,63
op=a[...,3]>0
g=np.zeros((H,W),bool); dark=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if not op[y,x]: continue
        h,l,s=colorsys.rgb_to_hls(*(a[y,x,:3]/255)); h*=360
        dark[y,x]=l<0.13
        kop=y<=24 and x<=30; staart=x>=44 and y>=29
        if (kop or staart) and 60<=h<=160: g[y,x]=True
# meerderheid over niet-donkere buren (lijnen tellen niet mee)
z=g.copy()
for y in range(H):
    for x in range(W):
        if not op[y,x] or dark[y,x]: continue
        kop=y<=24 and x<=30; staart=x>=44 and y>=29
        if not(kop or staart): continue
        n=[(g[yy,xx]) for yy in range(y-1,y+2) for xx in range(x-1,x+2) if 0<=yy<H and 0<=xx<W and op[yy,xx] and not dark[yy,xx]]
        z[y,x]=sum(n)*2>len(n)
z&=~dark
np.save('groenzone.npy',z)
v=np.zeros((H,W,3),'uint8')+200; v[op]=(240,200,90); v[z]=(90,170,80); v[dark&op]=(30,30,30)
Image.fromarray(v).resize((W*8,H*8),Image.NEAREST).save('zones_8x.png')
print(z.sum())
