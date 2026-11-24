# overlay.py x0 y0 x1 y1 out [z]: sprite (grid.txt) op z x met modelskelet (rood) erover
import sys,numpy as np; from PIL import Image, ImageDraw
import json
x0,y0,x1,y1=map(int,sys.argv[1:5]); out=sys.argv[5]; z=int(sys.argv[6]) if len(sys.argv)>6 else 20
P=8.1; sk=np.load('model_skelet.npy')
pal=json.load(open('palet.json'))
G=[l.rstrip('\n') for l in open('grid.txt') if l.strip()]
im=Image.new('RGB',((x1-x0)*z,(y1-y0)*z),'white'); d=ImageDraw.Draw(im)
for y in range(y0,y1):
    for x in range(x0,x1):
        c=G[y][x]
        if c=='.': continue
        d.rectangle([(x-x0)*z,(y-y0)*z,(x-x0+1)*z-1,(y-y0+1)*z-1],fill=tuple(pal[int(c,16)]))
for i in range(x0,x1+1): d.line([((i-x0)*z,0),((i-x0)*z,im.height)],fill=(200,200,200) if i%5 else (0,160,0))
for j in range(y0,y1+1): d.line([(0,(j-y0)*z),(im.width,(j-y0)*z)],fill=(200,200,200) if j%5 else (0,160,0))
ys,xs=np.nonzero(sk)
for my,mx in zip(ys,xs):
    sx=(mx-512)/P+32; sy=(my-523)/P+60
    if x0<=sx<x1 and y0<=sy<y1:
        px,py=(sx-x0)*z,(sy-y0)*z; d.rectangle([px-1,py-1,px+1,py+1],fill=(255,0,0))
im.save(out)
