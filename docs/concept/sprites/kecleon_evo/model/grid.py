import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGB'); x0,y0,x1,y1=map(int,sys.argv[3:7]); s=12
c=im.crop((x0,y0,x1,y1)).resize(((x1-x0)*s,(y1-y0)*s),Image.NEAREST); d=ImageDraw.Draw(c)
for x in range(x0,x1):
  if x%5==0: d.line([( (x-x0)*s,0),((x-x0)*s,c.height)],fill=(0,160,255) if x%10 else (255,0,255)); d.text(((x-x0)*s+1,1),str(x),fill=(0,0,255))
for y in range(y0,y1):
  if y%5==0: d.line([(0,(y-y0)*s),(c.width,(y-y0)*s)],fill=(0,160,255) if y%10 else (255,0,255)); d.text((1,(y-y0)*s+1),str(y),fill=(0,0,255))
c.save(sys.argv[2])
