import sys
from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('P'); x0,y0,x1,y1=map(int,sys.argv[2:6]); S=int(sys.argv[7]) if len(sys.argv)>7 else 20
pal=im.getpalette(); px=im.load()
W=(x1-x0)*S+30; H=(y1-y0)*S+20
c=Image.new('RGB',(W,H),(255,255,255)); d=ImageDraw.Draw(c)
for y in range(y0,y1):
  for x in range(x0,x1):
    i=px[x,y]; col=(230,230,230) if i==0 else tuple(pal[3*i:3*i+3])
    X=30+(x-x0)*S; Y=20+(y-y0)*S
    d.rectangle([X,Y,X+S-1,Y+S-1],fill=col,outline=(200,200,200) if i==0 else None)
for x in range(x0,x1): d.text((30+(x-x0)*S+3,4),str(x%100),fill=(0,0,0))
for y in range(y0,y1): d.text((2,20+(y-y0)*S+4),str(y),fill=(0,0,0))
c.save(sys.argv[6])
