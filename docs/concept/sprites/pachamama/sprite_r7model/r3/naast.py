# hulp: sprite-uitsnede naast model-uitsnede, zelfde raster (1 spritecel = 3x3 natief), 24 px per cel
import sys; sys.path.insert(0,'r2'); from gemeen import *; from PIL import Image,ImageDraw
o=np.load(sys.argv[1]); y0,y1,x0,x1=[int(v) for v in sys.argv[2:6]]; uit=sys.argv[6]; MY,MX=-21,-2; S=24
im=Image.open('natief_g1.png').convert('RGB')
m=im.crop((MX+3*x0,MY+3*y0,MX+3*x1,MY+3*y1)).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST)
s=Image.fromarray(np.array([[(255,255,255) if v==0 else PAL[v] for v in r] for r in o[y0:y1,x0:x1]],np.uint8)).resize(m.size,Image.NEAREST)
def grid(c):
  d=ImageDraw.Draw(c)
  for i in range(x1-x0+1): d.line([(i*S,0),(i*S,c.height)],fill=(255,0,255) if (x0+i)%5==0 else (150,150,255))
  for j in range(y1-y0+1): d.line([(0,j*S),(c.width,j*S)],fill=(255,0,255) if (y0+j)%5==0 else (150,150,255))
  for i in range(x1-x0): d.text((i*S+3,3),str(x0+i),fill=(255,255,0))
  for j in range(y1-y0): d.text((3,j*S+12),str(y0+j),fill=(0,255,0))
grid(m); grid(s)
v=Image.new('RGB',(2*m.width+10,m.height),'gray'); v.paste(s,(0,0)); v.paste(m,(m.width+10,0)); v.save(uit)
