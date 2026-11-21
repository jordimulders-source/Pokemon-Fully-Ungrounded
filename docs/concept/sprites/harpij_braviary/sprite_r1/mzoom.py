# mzoom.py out x0 x1 y0 y1 S : model natief uitsnede met coordinaten
import sys; from PIL import Image, ImageDraw
o,x0,x1,y0,y1,S=sys.argv[1],*map(int,sys.argv[2:7])
m=Image.open('../model/model_natief.png').convert('RGB').crop((x0,y0,x1,y1)); c=m.resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST); d=ImageDraw.Draw(c)
for x in range(x0,x1):
    if x%2==0: d.text(((x-x0)*S+1,0),str(x),fill=(255,0,0))
for y in range(y0,y1):
    if y%2==0: d.text((1,(y-y0)*S+2),str(y),fill=(255,0,0))
for x in range(x0,x1,5): d.line([((x-x0)*S,0),((x-x0)*S,c.size[1])],fill=(255,160,160))
for y in range(y0,y1,5): d.line([(0,(y-y0)*S),(c.size[0],(y-y0)*S)],fill=(255,160,160))
c.save(o)
