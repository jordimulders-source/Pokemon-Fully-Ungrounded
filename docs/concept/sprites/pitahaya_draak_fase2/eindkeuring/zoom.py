# zoom.py <png> <schaal> <uit> [x0 y0 x1 y1]: vergroting met raster en coordinaten
import sys; from PIL import Image, ImageDraw
src,s,out=sys.argv[1],int(sys.argv[2]),sys.argv[3]
im=Image.open(src).convert('RGBA')
box=tuple(map(int,sys.argv[4:8])) if len(sys.argv)>4 else (0,0)+im.size
im=im.crop(box); W,H=im.size
bg=Image.new('RGBA',(W*s,H*s),(210,225,235,255)); big=im.resize((W*s,H*s),Image.NEAREST); bg.alpha_composite(big)
d=ImageDraw.Draw(bg)
for x in range(W+1): d.line([(x*s,0),(x*s,H*s)],fill=(255,255,255,90) if (x+box[0])%5 else (0,0,255,160))
for y in range(H+1): d.line([(0,y*s),(W*s,y*s)],fill=(255,255,255,90) if (y+box[1])%5 else (0,0,255,160))
for x in range(W):
  if (x+box[0])%5==0: d.text((x*s+1,1),str(x+box[0]),fill=(0,0,200,255))
for y in range(H):
  if (y+box[1])%5==0: d.text((1,y*s+1),str(y+box[1]),fill=(0,0,200,255))
bg.convert('RGB').save(out)
