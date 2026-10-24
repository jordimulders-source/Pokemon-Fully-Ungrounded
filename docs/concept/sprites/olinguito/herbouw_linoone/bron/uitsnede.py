"""Uitsnede op 8x/16x met raster en coordinaten: uitsnede.py raster.txt x0 y0 x1 y1 zoom uit.png"""
import sys
sys.path.insert(0,'/home/user/projectgrounded/docs/concept/sprites/olinguito/herbouw_linoone/bron')
from render import load,to_img,zoom
from PIL import Image,ImageDraw
rows=load(sys.argv[1]); x0,y0,x1,y1,z=map(int,sys.argv[2:7])
im=to_img(rows).crop((x0,y0,x1,y1)); Z=zoom(im,z)
d=ImageDraw.Draw(Z)
for x in range(x1-x0):
    if (x+x0)%2==0: d.line([(x*z,0),(x*z,4)],fill=(255,0,0))
    if (x+x0)%5==0: d.text((x*z+2,0),str(x+x0),fill=(255,0,0))
for y in range(y1-y0):
    if (y+y0)%5==0: d.text((0,y*z+2),str(y+y0),fill=(0,0,255))
    d.line([(0,y*z),(3,y*z)],fill=(0,0,255))
Z.save(sys.argv[7])
