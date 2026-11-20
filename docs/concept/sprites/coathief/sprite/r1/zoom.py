# zoom.py png x0 y0 x1 y1 schaal uit.png  (met raster en coordinaten om de 5 px)
import sys; from PIL import Image, ImageDraw
p,x0,y0,x1,y1,s,o=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
im=Image.open(p).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
c=bg.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST); d=ImageDraw.Draw(c)
for x in range(x0,x1):
  if x%5==0: d.line([((x-x0)*s,0),((x-x0)*s,c.size[1])],fill=(0,160,255),width=1); d.text(((x-x0)*s+1,1),str(x),fill=(0,90,200))
for y in range(y0,y1):
  if y%5==0: d.line([(0,(y-y0)*s),(c.size[0],(y-y0)*s)],fill=(0,160,255),width=1); d.text((1,(y-y0)*s+1),str(y),fill=(0,90,200))
c.save(o)
