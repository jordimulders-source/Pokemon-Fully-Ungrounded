# zoom.py IN y0 y1 x0 x1 UIT : sprite-uitsnede 16x naast model (natief) op dezelfde schaal, met raster
import sys; from PIL import Image, ImageDraw
im=Image.open(sys.argv[1]).convert('RGBA'); y0,y1,x0,x1=map(int,sys.argv[2:6]); Z=16
b=Image.new('RGBA',(64,64),(200,230,200,255)); b.alpha_composite(im)
c=b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
n=Image.open('../natief.png').convert('RGB').crop((3*x0+3,3*y0-9,3*x1+3,3*y1-9)).resize(c.size,Image.NEAREST)
for img in (c,n):
  d=ImageDraw.Draw(img)
  for k in range(x1-x0+1): d.line([(k*Z,0),(k*Z,img.size[1])],fill=(255,0,0) if (x0+k)%5==0 else (120,120,120))
  for k in range(y1-y0+1): d.line([(0,k*Z),(img.size[0],k*Z)],fill=(255,0,0) if (y0+k)%5==0 else (120,120,120))
sh=Image.new('RGB',(c.size[0]*2+10,c.size[1]),'white'); sh.paste(c,(0,0)); sh.paste(n,(c.size[0]+10,0)); sh.save(sys.argv[6])
